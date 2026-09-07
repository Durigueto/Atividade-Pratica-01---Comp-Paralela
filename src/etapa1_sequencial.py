"""
Etapa 1 - Implementação Sequencial
Computação Paralela e Distribuída - Atividade Prática 01

Execução sequencial de uma tarefa computacionalmente intensiva para medir o tempo T1 de referência.
"""

import time
import statistics


def tarefa(numero: int) -> int:
    """Executa um cálculo aritmético intensivo para um determinado número."""
    resultado = 0
    for i in range(1, 300_000):
        resultado += (numero * i) % 97
    return resultado


def executar_sequencial(dados: list[int]) -> tuple[list[int], float]:
    """Executa a tarefa para cada elemento da lista sequencialmente."""
    inicio = time.perf_counter()
    resultados = []

    for numero in dados:
        resultados.append(tarefa(numero))

    fim = time.perf_counter()
    return resultados, fim - inicio


if __name__ == "__main__":
    dados = list(range(1, 101))
    repeticoes = 3
    tempos = []

    print("=" * 50)
    print("ETAPA 1: EXECUÇÃO SEQUENCIAL (100 tarefas)")
    print("=" * 50)

    for execucao in range(1, repeticoes + 1):
        _, tempo = executar_sequencial(dados)
        tempos.append(tempo)
        print(f"Execução {execucao}: {tempo:.4f} segundos")

    tempo_medio = statistics.mean(tempos)
    desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0.0

    print("-" * 50)
    print(f"Tempo Sequencial Médio (T1): {tempo_medio:.4f} s (± {desvio:.4f} s)")
    print("=" * 50)
