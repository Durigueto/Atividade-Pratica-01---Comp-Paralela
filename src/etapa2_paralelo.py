import time
import statistics
from concurrent.futures import ProcessPoolExecutor


def tarefa(numero: int) -> int:
    resultado = 0
    for i in range(1, 300_000):
        resultado += (numero * i) % 97
    return resultado


def executar_sequencial(dados: list[int]) -> tuple[list[int], float]:
    inicio = time.perf_counter()
    resultados = [tarefa(num) for num in dados]
    fim = time.perf_counter()
    return resultados, fim - inicio


def executar_paralelo(dados: list[int], workers: int) -> tuple[list[int], float]:
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        resultados = list(executor.map(tarefa, dados))
    fim = time.perf_counter()
    return resultados, fim - inicio


if __name__ == "__main__":
    dados = list(range(1, 101))
    repeticoes = 3
    workers_lista = [1, 2, 4, 8]

    print("=" * 65)
    print("ETAPA 2 e 3: EXECUÇÃO PARALELA E CÁLCULO DE MÉTRICAS")
    print(f"Número de tarefas: {len(dados)} | Repetições por configuração: {repeticoes}")
    print("=" * 65)

    print("Calculando tempo sequencial T1 de referência...")
    tempos_seq = [executar_sequencial(dados)[1] for _ in range(repeticoes)]
    t1_referencia = statistics.mean(tempos_seq)
    print(f"T1 Sequencial Médio: {t1_referencia:.4f} s\n")

    tabela_resultados = []

    for workers in workers_lista:
        tempos = []
        for rep in range(repeticoes):
            _, duracao = executar_paralelo(dados, workers)
            tempos.append(duracao)

        tempo_medio = statistics.mean(tempos)
        speedup = t1_referencia / tempo_medio
        eficiencia = speedup / workers

        tabela_resultados.append({
            "processos": workers,
            "tempo": tempo_medio,
            "speedup": speedup,
            "eficiencia": eficiencia
        })

    print(f"{'Processos (N)':<15} | {'Tempo Médio (s)':<15} | {'Speedup':<12} | {'Eficiência':<12}")
    print("-" * 65)
    for r in tabela_resultados:
        print(f"{r['processos']:<15} | {r['tempo']:<15.4f} | {r['speedup']:<12.2f} | {r['eficiencia']:<12.2f}")
    print("=" * 65)
