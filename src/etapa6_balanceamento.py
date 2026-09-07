"""
Etapa 6 - Desafio de Balanceamento de Carga
Computação Paralela e Distribuída - Atividade Prática 01

Avalia o impacto de tarefas heterogêneas (carga desbalanceada) no desempenho,
analisando ociosidade de núcleos (idle time) e comparando a divisão estática
versus estratégias dinâmicas (chunksize=1).
"""

import time
import os
import statistics
from concurrent.futures import ProcessPoolExecutor, as_completed


def tarefa_desbalanceada(numero: int) -> int:
    """Tarefa com carga assimétrica: números múltiplos de 10 exigem 5x mais iterações."""
    if numero % 10 == 0:
        limite = 1_500_000
    else:
        limite = 300_000

    resultado = 0
    for i in range(1, limite):
        resultado += (numero * i) % 97

    return resultado


def tarefa_com_telemetria(numero: int) -> tuple[int, int, float, float]:
    """Executa a tarefa registrando PID do processo, tempo de início e término."""
    inicio = time.perf_counter()
    res = tarefa_desbalanceada(numero)
    fim = time.perf_counter()
    pid = os.getpid()
    return numero, pid, inicio, fim


def executar_sequencial(dados: list[int]) -> tuple[list[int], float]:
    inicio = time.perf_counter()
    resultados = [tarefa_desbalanceada(n) for n in dados]
    fim = time.perf_counter()
    return resultados, fim - inicio


def executar_paralelo_padrao(dados: list[int], workers: int) -> tuple[list[int], float]:
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        resultados = list(executor.map(tarefa_desbalanceada, dados))
    fim = time.perf_counter()
    return resultados, fim - inicio


def executar_paralelo_dinamico(dados: list[int], workers: int, chunksize: int = 1) -> tuple[list[int], float]:
    """Distribuição dinâmica com chunksize unitário para mitigar ociosidade."""
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        resultados = list(executor.map(tarefa_desbalanceada, dados, chunksize=chunksize))
    fim = time.perf_counter()
    return resultados, fim - inicio


def analisar_desbalanceamento_workers(dados: list[int], workers: int = 4):
    """Mede o tempo total ativo de cada processo (worker) para evidenciar a ociosidade."""
    print(f"\n--- Análise de Carga por Processo Individual ({workers} Workers) ---")
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(tarefa_com_telemetria, n) for n in dados]
        telemetria = [f.result() for f in as_completed(futures)]

    # Agrupar tempos por PID
    tempo_por_pid = {}
    inicio_global = min(t[2] for t in telemetria)
    fim_global = max(t[3] for t in telemetria)
    tempo_total_pool = fim_global - inicio_global

    for _, pid, ini, fim in telemetria:
        duracao = fim - ini
        tempo_por_pid[pid] = tempo_por_pid.get(pid, 0.0) + duracao

    print(f"Tempo total de execução do Pool: {tempo_total_pool:.4f} s")
    print(f"{'PID do Processo':<18} | {'Tempo Ativo (s)':<18} | {'Ociosidade (%)':<15}")
    print("-" * 57)
    for idx, (pid, tempo_ativo) in enumerate(tempo_por_pid.items(), 1):
        ociosidade = max(0.0, (1.0 - (tempo_ativo / tempo_total_pool)) * 100)
        print(f"Worker {idx} (PID {pid:<5}) | {tempo_ativo:<18.4f} | {ociosidade:<14.2f}%")

    return tempo_total_pool, tempo_por_pid


if __name__ == "__main__":
    dados = list(range(1, 101))
    repeticoes = 3
    workers_lista = [1, 2, 4, 8]

    print("=" * 70)
    print("ETAPA 6: DESAFIO DE BALANCEAMENTO DE CARGA (TAREFAS HETEROGÊNEAS)")
    print("=" * 70)

    # 1. Sequencial
    tempos_seq = [executar_sequencial(dados)[1] for _ in range(repeticoes)]
    t1 = statistics.mean(tempos_seq)
    print(f"Tempo Sequencial Médio (T1): {t1:.4f} s\n")

    # 2. Paralelo Padrão vs Dinâmico
    print(f"{'Processos':<10} | {'Tempo Padrão':<14} | {'Speedup Pad':<12} | {'Tempo Dinâmico':<16} | {'Speedup Din':<12}")
    print("-" * 70)

    for workers in workers_lista:
        t_padrao = statistics.mean([executar_paralelo_padrao(dados, workers)[1] for _ in range(repeticoes)])
        t_dinamico = statistics.mean([executar_paralelo_dinamico(dados, workers, chunksize=1)[1] for _ in range(repeticoes)])

        sp_padrao = t1 / t_padrao
        sp_dinamico = t1 / t_dinamico

        print(f"{workers:<10} | {t_padrao:<14.4f} | {sp_padrao:<12.2f} | {t_dinamico:<16.4f} | {sp_dinamico:<12.2f}")

    # 3. Análise detalhada de telemetria com 4 processos
    analisar_desbalanceamento_workers(dados, workers=4)
    print("=" * 70)
