"""
Etapa 5 - Experimento de Granularidade
Computação Paralela e Distribuída - Atividade Prática 01

Investiga como a quantidade total de tarefas influencia o aproveitamento
dos núcleos e o overhead de gerenciamento e comunicação.
- Experimento A: 20 tarefas (range(1, 21))
- Experimento B: 100 tarefas (range(1, 101))
- Experimento C: 500 tarefas (range(1, 501))
"""

import time
import statistics
from concurrent.futures import ProcessPoolExecutor


def tarefa(numero: int) -> int:
    """Executa um cálculo aritmético intensivo para um determinado número."""
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


def rodar_experimento_granularidade():
    experimentos = {
        "A (20 tarefas)": list(range(1, 21)),
        "B (100 tarefas)": list(range(1, 101)),
        "C (500 tarefas)": list(range(1, 501)),
    }
    workers_lista = [1, 2, 4, 8]
    repeticoes = 3

    print("=" * 75)
    print("ETAPA 5: EXPERIMENTO DE GRANULARIDADE")
    print("=" * 75)

    resultados_gerais = {}

    for nome_exp, dados in experimentos.items():
        print(f"\n>>> Executando {nome_exp} | Total de Tarefas: {len(dados)}...")
        tempos_seq = [executar_sequencial(dados)[1] for _ in range(repeticoes)]
        t1 = statistics.mean(tempos_seq)

        resultados_exp = []
        for workers in workers_lista:
            tempos = [executar_paralelo(dados, workers)[1] for _ in range(repeticoes)]
            tempo_medio = statistics.mean(tempos)
            speedup = t1 / tempo_medio
            eficiencia = speedup / workers
            resultados_exp.append({
                "processos": workers,
                "tempo": tempo_medio,
                "speedup": speedup,
                "eficiencia": eficiencia
            })

        resultados_gerais[nome_exp] = {
            "t1": t1,
            "tabela": resultados_exp
        }

        print(f"{'Processos (N)':<15} | {'Tempo Médio (s)':<15} | {'Speedup':<12} | {'Eficiência':<12}")
        print("-" * 65)
        for r in resultados_exp:
            print(f"{r['processos']:<15} | {r['tempo']:<15.4f} | {r['speedup']:<12.2f} | {r['eficiencia']:<12.2f}")

    print("\n" + "=" * 75)
    return resultados_gerais


if __name__ == "__main__":
    rodar_experimento_granularidade()
