import os
import sys
import time
import json
import platform
import statistics
from concurrent.futures import ProcessPoolExecutor, as_completed


def tarefa_homogenea(numero: int) -> int:
    resultado = 0
    for i in range(1, 300_000):
        resultado += (numero * i) % 97
    return resultado


def tarefa_heterogenea(numero: int) -> int:
    limite = 1_500_000 if (numero % 10 == 0) else 300_000
    resultado = 0
    for i in range(1, limite):
        resultado += (numero * i) % 97
    return resultado


def tarefa_telemetria(numero: int) -> tuple[int, int, float, float]:
    inicio = time.perf_counter()
    res = tarefa_heterogenea(numero)
    fim = time.perf_counter()
    return numero, os.getpid(), inicio, fim


def executar_seq(func, dados: list[int]) -> float:
    inicio = time.perf_counter()
    _ = [func(n) for n in dados]
    fim = time.perf_counter()
    return fim - inicio


def executar_par(func, dados: list[int], workers: int, chunksize: int | None = None) -> float:
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        if chunksize is not None:
            _ = list(executor.map(func, dados, chunksize=chunksize))
        else:
            _ = list(executor.map(func, dados))
    fim = time.perf_counter()
    return fim - inicio


def rodar_benchmark(repeticoes: int = 3):
    print("=" * 80)
    print("INICIANDO BENCHMARK COMPLETO - ATIVIDADE PRÁTICA 01")
    print(f"Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"Processador: {platform.processor()}")
    print(f"CPUs Lógicas Detectadas: {os.cpu_count()}")
    print(f"Repetições por medição: {repeticoes}")
    print("=" * 80)

    workers_lista = [1, 2, 4, 8]
    dados_100 = list(range(1, 101))

    resultados = {
        "metadados": {
            "os": platform.platform(),
            "cpu": platform.processor(),
            "cpus_logicas": os.cpu_count(),
            "python_versao": platform.python_version(),
            "repeticoes": repeticoes,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "etapa1_sequencial": {},
        "etapa2_3_paralelo": [],
        "etapa5_granularidade": {},
        "etapa6_balanceamento": {
            "comparativo": [],
            "telemetria_workers": {}
        }
    }

    print("\n>>> Executando ETAPAS 1, 2 e 3 (100 tarefas homogêneas)...")
    tempos_seq_100 = [executar_seq(tarefa_homogenea, dados_100) for _ in range(repeticoes)]
    t1_100 = statistics.mean(tempos_seq_100)
    desv_100 = statistics.stdev(tempos_seq_100) if repeticoes > 1 else 0.0

    resultados["etapa1_sequencial"] = {
        "tempos": tempos_seq_100,
        "media": t1_100,
        "desvio_padrao": desv_100
    }
    print(f"Tempo Sequencial Médio T1: {t1_100:.4f} s (± {desv_100:.4f} s)")

    for w in workers_lista:
        tempos = [executar_par(tarefa_homogenea, dados_100, w) for _ in range(repeticoes)]
        t_medio = statistics.mean(tempos)
        desv = statistics.stdev(tempos) if repeticoes > 1 else 0.0
        speedup = t1_100 / t_medio
        eficiencia = speedup / w

        item = {
            "processos": w,
            "tempos": tempos,
            "tempo_medio": t_medio,
            "desvio_padrao": desv,
            "speedup": speedup,
            "eficiencia": eficiencia
        }
        resultados["etapa2_3_paralelo"].append(item)
        print(f"Workers: {w:<2} | Tempo: {t_medio:.4f} s | Speedup: {speedup:.2f}x | Eficiência: {eficiencia:.2%}")

    print("\n>>> Executando ETAPA 5 (Granularidade: 20, 100, 500 tarefas)...")
    experimentos_gran = {
        "Exp_A_20": list(range(1, 21)),
        "Exp_B_100": list(range(1, 101)),
        "Exp_C_500": list(range(1, 501))
    }

    for chave, dataset in experimentos_gran.items():
        print(f"Testando {chave} ({len(dataset)} tarefas)...")
        tempos_seq = [executar_seq(tarefa_homogenea, dataset) for _ in range(repeticoes)]
        t1_gran = statistics.mean(tempos_seq)

        tabela_gran = []
        for w in workers_lista:
            tempos = [executar_par(tarefa_homogenea, dataset, w) for _ in range(repeticoes)]
            t_medio = statistics.mean(tempos)
            sp = t1_gran / t_medio
            ef = sp / w
            tabela_gran.append({
                "processos": w,
                "tempo_medio": t_medio,
                "speedup": sp,
                "eficiencia": ef
            })
            print(f"  [{chave}] Workers: {w} | Tempo: {t_medio:.4f} s | Speedup: {sp:.2f}x | Efic: {ef:.2%}")

        resultados["etapa5_granularidade"][chave] = {
            "qtd_tarefas": len(dataset),
            "t1_sequencial": t1_gran,
            "resultados": tabela_gran
        }

    print("\n>>> Executando ETAPA 6 (Balanceamento de Carga Heterogêneo)...")
    tempos_seq_het = [executar_seq(tarefa_heterogenea, dados_100) for _ in range(repeticoes)]
    t1_het = statistics.mean(tempos_seq_het)
    print(f"Tempo Sequencial Heterogêneo T1: {t1_het:.4f} s")

    for w in workers_lista:
        t_pad = statistics.mean([executar_par(tarefa_heterogenea, dados_100, w) for _ in range(repeticoes)])
        t_din = statistics.mean([executar_par(tarefa_heterogenea, dados_100, w, chunksize=1) for _ in range(repeticoes)])

        sp_pad = t1_het / t_pad
        sp_din = t1_het / t_din
        ef_pad = sp_pad / w
        ef_din = sp_din / w

        item = {
            "processos": w,
            "tempo_padrao": t_pad,
            "speedup_padrao": sp_pad,
            "eficiencia_padrao": ef_pad,
            "tempo_dinamico": t_din,
            "speedup_dinamico": sp_din,
            "eficiencia_dinamica": ef_din
        }
        resultados["etapa6_balanceamento"]["comparativo"].append(item)
        print(f"Workers: {w} | Padrão: {t_pad:.4f}s (Sp: {sp_pad:.2f}x) | Dinâmico (chunk=1): {t_din:.4f}s (Sp: {sp_din:.2f}x)")

    print("\n>>> Coletando telemetria individual de workers (4 processos)...")
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(tarefa_telemetria, n) for n in dados_100]
        telemetria = [f.result() for f in as_completed(futures)]

    t_ini = min(t[2] for t in telemetria)
    t_fim = max(t[3] for t in telemetria)
    duracao_total = t_fim - t_ini

    tempo_ativo = {}
    for _, pid, ini, fim in telemetria:
        tempo_ativo[str(pid)] = tempo_ativo.get(str(pid), 0.0) + (fim - ini)

    dados_telemetria = {
        "duracao_total_pool": duracao_total,
        "workers": []
    }
    for idx, (pid, t_atv) in enumerate(tempo_ativo.items(), 1):
        ociosidade = max(0.0, (1.0 - (t_atv / duracao_total)) * 100)
        dados_telemetria["workers"].append({
            "worker_idx": idx,
            "pid": pid,
            "tempo_ativo": t_atv,
            "ociosidade_percentual": ociosidade
        })
        print(f"Worker {idx} (PID {pid}): Ativo {t_atv:.4f} s | Ociosidade: {ociosidade:.2f}%")

    resultados["etapa6_balanceamento"]["telemetria_workers"] = dados_telemetria

    arquivo_saida = "resultados_experimentais.json"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"BENCHMARK CONCLUÍDO COM SUCESSO! Dados salvos em '{arquivo_saida}'.")
    print("=" * 80)
    return resultados


if __name__ == "__main__":
    rodar_benchmark(repeticoes=3)
