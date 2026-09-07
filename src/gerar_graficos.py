"""
Geração de Gráficos em SVG Puro - Computação Paralela e Distribuída
Atividade Prática 01

Lê os dados experimentais coletados de resultados_experimentais.json e gera gráficos
vetoriais profissionais em formato SVG (sem necessidade de bibliotecas externas como
numpy ou matplotlib), garantindo 100% de portabilidade e renderização nativa no GitHub.
"""

import os
import json


def criar_svg_speedup_eficiencia(dados, output_path="assets/speedup_eficiencia.svg"):
    paralelo = dados["etapa2_3_paralelo"]
    proc = [item["processos"] for item in paralelo]  # [1, 2, 4, 8]
    speedup = [item["speedup"] for item in paralelo]
    eficiencia = [item["eficiencia"] * 100 for item in paralelo]

    width, height = 900, 420
    pad_left, pad_right, pad_top, pad_bot = 60, 40, 60, 50
    chart_w = 360
    chart_h = 280

    # Layout de dois gráficos:
    # Grafico 1 (Speedup): x de pad_left a pad_left + chart_w (60 a 420)
    # Grafico 2 (Eficiência): x de 500 a 860
    x_max = 8.5
    y_max_sp = 8.5
    y_max_ef = 115.0

    def map_pt(p_x, p_y, orig_x, orig_y, max_x, max_y, h):
        cx = orig_x + (p_x / max_x) * chart_w
        cy = (orig_y + h) - (p_y / max_y) * h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('<defs>')
    svg.append('  <linearGradient id="gradBg" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('    <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('    <stop offset="100%" stop-color="#f8fafc"/>')
    svg.append('  </linearGradient>')
    svg.append('  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">')
    svg.append('    <feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity="0.1"/>')
    svg.append('  </filter>')
    svg.append('</defs>')

    # Fundo
    svg.append(f'<rect width="{width}" height="{height}" rx="12" fill="url(#gradBg)" stroke="#e2e8f0" stroke-width="1.5"/>')

    # ==========================
    # Painel 1: Speedup
    # ==========================
    orig_x1, orig_y1 = 60, 70
    svg.append(f'<text x="{orig_x1 + chart_w/2}" y="40" font-family="Segoe UI, -apple-system, sans-serif" font-size="16" font-weight="700" text-anchor="middle" fill="#0f172a">Speedup vs. Número de Processos</text>')

    # Grid e Eixos Speedup
    for v in [0, 2, 4, 6, 8]:
        _, gy = map_pt(0, v, orig_x1, orig_y1, x_max, y_max_sp, chart_h)
        svg.append(f'<line x1="{orig_x1}" y1="{gy}" x2="{orig_x1 + chart_w}" y2="{gy}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{orig_x1 - 10}" y="{gy + 4}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="end">{v}</text>')

    for p in [1, 2, 4, 8]:
        gx, _ = map_pt(p, 0, orig_x1, orig_y1, x_max, y_max_sp, chart_h)
        svg.append(f'<line x1="{gx}" y1="{orig_y1}" x2="{gx}" y2="{orig_y1 + chart_h}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{gx}" y="{orig_y1 + chart_h + 20}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">{p}</text>')

    # Linha Ideal S = N
    id_x1, id_y1 = map_pt(0, 0, orig_x1, orig_y1, x_max, y_max_sp, chart_h)
    id_x2, id_y2 = map_pt(8, 8, orig_x1, orig_y1, x_max, y_max_sp, chart_h)
    svg.append(f'<line x1="{id_x1}" y1="{id_y1}" x2="{id_x2}" y2="{id_y2}" stroke="#ef4444" stroke-width="2" stroke-dasharray="5,5"/>')

    # Curva Real Speedup
    pontos_sp = [map_pt(x, y, orig_x1, orig_y1, x_max, y_max_sp, chart_h) for x, y in zip(proc, speedup)]
    polyline_sp = " ".join([f"{px:.1f},{py:.1f}" for px, py in pontos_sp])
    svg.append(f'<polyline points="{polyline_sp}" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

    for (px, py), sp, p in zip(pontos_sp, speedup, proc):
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#2563eb" stroke="#ffffff" stroke-width="2"/>')
        svg.append(f'<rect x="{px - 22}" y="{py - 24}" width="44" height="18" rx="4" fill="#1e293b" opacity="0.9"/>')
        svg.append(f'<text x="{px}" y="{py - 11}" font-family="Segoe UI, sans-serif" font-size="11" font-weight="600" fill="#ffffff" text-anchor="middle">{sp:.2f}x</text>')

    # Legenda Speedup
    svg.append(f'<circle cx="{orig_x1 + 20}" cy="{orig_y1 + 25}" r="4" fill="#2563eb"/>')
    svg.append(f'<text x="{orig_x1 + 30}" y="{orig_y1 + 29}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">Experimental</text>')
    svg.append(f'<line x1="{orig_x1 + 120}" y1="{orig_y1 + 25}" x2="{orig_x1 + 145}" y2="{orig_y1 + 25}" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,3"/>')
    svg.append(f'<text x="{orig_x1 + 155}" y="{orig_y1 + 29}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">Ideal (S = N)</text>')

    # ==========================
    # Painel 2: Eficiência
    # ==========================
    orig_x2, orig_y2 = 500, 70
    svg.append(f'<text x="{orig_x2 + chart_w/2}" y="40" font-family="Segoe UI, -apple-system, sans-serif" font-size="16" font-weight="700" text-anchor="middle" fill="#0f172a">Eficiência vs. Processos (%)</text>')

    # Grid e Eixos Eficiência
    for v in [0, 25, 50, 75, 100]:
        _, gy = map_pt(0, v, orig_x2, orig_y2, x_max, y_max_ef, chart_h)
        svg.append(f'<line x1="{orig_x2}" y1="{gy}" x2="{orig_x2 + chart_w}" y2="{gy}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{orig_x2 - 10}" y="{gy + 4}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="end">{v}%</text>')

    for p in [1, 2, 4, 8]:
        gx, _ = map_pt(p, 0, orig_x2, orig_y2, x_max, y_max_ef, chart_h)
        svg.append(f'<line x1="{gx}" y1="{orig_y2}" x2="{gx}" y2="{orig_y2 + chart_h}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{gx}" y="{orig_y2 + chart_h + 20}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">{p}</text>')

    # Linha Ideal Eficiência 100%
    _, ef_100_y = map_pt(0, 100, orig_x2, orig_y2, x_max, y_max_ef, chart_h)
    svg.append(f'<line x1="{orig_x2}" y1="{ef_100_y}" x2="{orig_x2 + chart_w}" y2="{ef_100_y}" stroke="#ef4444" stroke-width="2" stroke-dasharray="5,5"/>')

    # Curva Real Eficiência
    pontos_ef = [map_pt(x, y, orig_x2, orig_y2, x_max, y_max_ef, chart_h) for x, y in zip(proc, eficiencia)]
    polyline_ef = " ".join([f"{px:.1f},{py:.1f}" for px, py in pontos_ef])
    svg.append(f'<polyline points="{polyline_ef}" fill="none" stroke="#16a34a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

    for (px, py), ef in zip(pontos_ef, eficiencia):
        svg.append(f'<rect x="{px - 5}" y="{py - 5}" width="10" height="10" rx="2" fill="#16a34a" stroke="#ffffff" stroke-width="2"/>')
        svg.append(f'<rect x="{px - 25}" y="{py - 24}" width="50" height="18" rx="4" fill="#1e293b" opacity="0.9"/>')
        svg.append(f'<text x="{px}" y="{py - 11}" font-family="Segoe UI, sans-serif" font-size="11" font-weight="600" fill="#ffffff" text-anchor="middle">{ef:.1f}%</text>')

    # Legenda Eficiência
    svg.append(f'<rect x="{orig_x2 + 20}" y="{orig_y2 + 21}" width="8" height="8" rx="2" fill="#16a34a"/>')
    svg.append(f'<text x="{orig_x2 + 35}" y="{orig_y2 + 29}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">Experimental</text>')
    svg.append(f'<line x1="{orig_x2 + 130}" y1="{orig_y2 + 25}" x2="{orig_x2 + 155}" y2="{orig_y2 + 25}" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,3"/>')
    svg.append(f'<text x="{orig_x2 + 165}" y="{orig_y2 + 29}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">Ideal (100%)</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Gráfico gerado com sucesso: {output_path}")


def criar_svg_granularidade(dados, output_path="assets/granularidade_comparacao.svg"):
    gran_data = dados["etapa5_granularidade"]
    width, height = 700, 420
    orig_x, orig_y = 70, 70
    chart_w, chart_h = 560, 280

    x_max = 8.5
    y_max = 5.8

    def map_pt(p_x, p_y):
        cx = orig_x + (p_x / x_max) * chart_w
        cy = (orig_y + chart_h) - (p_y / y_max) * chart_h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('<defs>')
    svg.append('  <linearGradient id="gradGran" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('    <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('    <stop offset="100%" stop-color="#f8fafc"/>')
    svg.append('  </linearGradient>')
    svg.append('</defs>')
    svg.append(f'<rect width="{width}" height="{height}" rx="12" fill="url(#gradGran)" stroke="#e2e8f0" stroke-width="1.5"/>')

    svg.append(f'<text x="{width/2}" y="40" font-family="Segoe UI, -apple-system, sans-serif" font-size="16" font-weight="700" text-anchor="middle" fill="#0f172a">Efeito da Granularidade no Speedup ($S = T_1 / T_p$)</text>')

    # Grid
    for v in [0, 1, 2, 3, 4, 5]:
        _, gy = map_pt(0, v)
        svg.append(f'<line x1="{orig_x}" y1="{gy}" x2="{orig_x + chart_w}" y2="{gy}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{orig_x - 10}" y="{gy + 4}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="end">{v}x</text>')

    for p in [1, 2, 4, 8]:
        gx, _ = map_pt(p, 0)
        svg.append(f'<line x1="{gx}" y1="{orig_y}" x2="{gx}" y2="{orig_y + chart_h}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{gx}" y="{orig_y + chart_h + 20}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">{p} Processos</text>')

    # Curvas dos Experimentos
    config_exp = [
        ("Exp_A_20", "#f97316", "Exp A: 20 tarefas (Granularidade Pequena)"),
        ("Exp_B_100", "#2563eb", "Exp B: 100 tarefas (Granularidade Média)"),
        ("Exp_C_500", "#16a34a", "Exp C: 500 tarefas (Granularidade Grande)")
    ]

    for idx, (chave, cor, rotulo) in enumerate(config_exp):
        info = gran_data[chave]
        w_list = [item["processos"] for item in info["resultados"]]
        sp_list = [item["speedup"] for item in info["resultados"]]

        pts = [map_pt(x, y) for x, y in zip(w_list, sp_list)]
        poly = " ".join([f"{px:.1f},{py:.1f}" for px, py in pts])
        svg.append(f'<polyline points="{poly}" fill="none" stroke="{cor}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

        for (px, py), sp in zip(pts, sp_list):
            svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{cor}" stroke="#ffffff" stroke-width="2"/>')
            svg.append(f'<text x="{px}" y="{py - 10}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="600" fill="{cor}" text-anchor="middle">{sp:.2f}x</text>')

        # Legenda
        leg_y = orig_y + 15 + (idx * 20)
        svg.append(f'<circle cx="{orig_x + 15}" cy="{leg_y}" r="4" fill="{cor}"/>')
        svg.append(f'<text x="{orig_x + 26}" y="{leg_y + 4}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">{rotulo}</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Gráfico gerado com sucesso: {output_path}")


def criar_svg_balanceamento(dados, output_path="assets/balanceamento_carga.svg"):
    bal_data = dados["etapa6_balanceamento"]
    width, height = 900, 420
    orig_x1, orig_y1 = 60, 70
    chart_w, chart_h = 360, 280

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('<defs>')
    svg.append('  <linearGradient id="gradBal" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('    <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('    <stop offset="100%" stop-color="#f8fafc"/>')
    svg.append('  </linearGradient>')
    svg.append('</defs>')
    svg.append(f'<rect width="{width}" height="{height}" rx="12" fill="url(#gradBal)" stroke="#e2e8f0" stroke-width="1.5"/>')

    # ==========================
    # Painel 1: Comparativo de Speedup (Padrão vs Dinâmico)
    # ==========================
    svg.append(f'<text x="{orig_x1 + chart_w/2}" y="40" font-family="Segoe UI, -apple-system, sans-serif" font-size="16" font-weight="700" text-anchor="middle" fill="#0f172a">Speedup: Estático vs. Dinâmico</text>')

    comp = bal_data["comparativo"]
    max_sp = 4.2
    for v in [0, 1, 2, 3, 4]:
        gy = (orig_y1 + chart_h) - (v / max_sp) * chart_h
        svg.append(f'<line x1="{orig_x1}" y1="{gy}" x2="{orig_x1 + chart_w}" y2="{gy}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{orig_x1 - 10}" y="{gy + 4}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="end">{v}x</text>')

    grupo_w = chart_w / len(comp)
    bar_w = 28
    for i, item in enumerate(comp):
        w_proc = item["processos"]
        sp_pad = item["speedup_padrao"]
        sp_din = item["speedup_dinamico"]

        cx = orig_x1 + (i + 0.5) * grupo_w
        h_pad = (sp_pad / max_sp) * chart_h
        h_din = (sp_din / max_sp) * chart_h

        y_pad = (orig_y1 + chart_h) - h_pad
        y_din = (orig_y1 + chart_h) - h_din

        # Barra Padrão
        svg.append(f'<rect x="{cx - bar_w - 2}" y="{y_pad}" width="{bar_w}" height="{h_pad}" rx="3" fill="#60a5fa"/>')
        svg.append(f'<text x="{cx - bar_w/2 - 2}" y="{y_pad - 6}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="600" fill="#2563eb" text-anchor="middle">{sp_pad:.2f}x</text>')

        # Barra Dinâmica
        svg.append(f'<rect x="{cx + 2}" y="{y_din}" width="{bar_w}" height="{h_din}" rx="3" fill="#f59e0b"/>')
        svg.append(f'<text x="{cx + bar_w/2 + 2}" y="{y_din - 6}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="600" fill="#b45309" text-anchor="middle">{sp_din:.2f}x</text>')

        # Rótulo Eixo X
        svg.append(f'<text x="{cx}" y="{orig_y1 + chart_h + 20}" font-family="Segoe UI, sans-serif" font-size="11" fill="#475569" text-anchor="middle">{w_proc} Workers</text>')

    # Legenda Painel 1
    svg.append(f'<rect x="{orig_x1 + 15}" y="{orig_y1 + 15}" width="12" height="12" rx="2" fill="#60a5fa"/>')
    svg.append(f'<text x="{orig_x1 + 33}" y="{orig_y1 + 25}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">Padrão (Estático)</text>')
    svg.append(f'<rect x="{orig_x1 + 155}" y="{orig_y1 + 15}" width="12" height="12" rx="2" fill="#f59e0b"/>')
    svg.append(f'<text x="{orig_x1 + 173}" y="{orig_y1 + 25}" font-family="Segoe UI, sans-serif" font-size="11" fill="#334155">Dinâmico (chunk=1)</text>')

    # ==========================
    # Painel 2: Ociosidade dos Workers (4 Workers)
    # ==========================
    orig_x2, orig_y2 = 500, 70
    svg.append(f'<text x="{orig_x2 + chart_w/2}" y="40" font-family="Segoe UI, -apple-system, sans-serif" font-size="16" font-weight="700" text-anchor="middle" fill="#0f172a">Tempo Ativo e Ociosidade (4 Workers)</text>')

    telemetria = bal_data.get("telemetria_workers", {}).get("workers", [])
    dur_total = bal_data.get("telemetria_workers", {}).get("duracao_total_pool", 1.5)
    max_tempo = dur_total * 1.25

    for v in [0, 0.4, 0.8, 1.2, 1.6]:
        gy = (orig_y2 + chart_h) - (v / max_tempo) * chart_h
        svg.append(f'<line x1="{orig_x2}" y1="{gy}" x2="{orig_x2 + chart_w}" y2="{gy}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{orig_x2 - 10}" y="{gy + 4}" font-family="Segoe UI, sans-serif" font-size="11" fill="#64748b" text-anchor="end">{v:.1f}s</text>')

    # Linha de Término Global
    y_fim_global = (orig_y2 + chart_h) - (dur_total / max_tempo) * chart_h
    svg.append(f'<line x1="{orig_x2}" y1="{y_fim_global}" x2="{orig_x2 + chart_w}" y2="{y_fim_global}" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,4"/>')
    svg.append(f'<text x="{orig_x2 + chart_w - 5}" y="{y_fim_global - 6}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="600" fill="#ef4444" text-anchor="end">Fim Global: {dur_total:.2f}s</text>')

    # Barras de cada worker
    w_bar_gap = chart_w / len(telemetria)
    w_bar_w = 45
    for i, w_item in enumerate(telemetria):
        cx = orig_x2 + (i + 0.5) * w_bar_gap
        t_atv = w_item["tempo_ativo"]
        oci = w_item["ociosidade_percentual"]

        h_bar = (t_atv / max_tempo) * chart_h
        y_bar = (orig_y2 + chart_h) - h_bar

        cor_bar = "#10b981" if oci < 2.0 else "#f87171"
        svg.append(f'<rect x="{cx - w_bar_w/2}" y="{y_bar}" width="{w_bar_w}" height="{h_bar}" rx="4" fill="{cor_bar}"/>')
        svg.append(f'<text x="{cx}" y="{y_bar - 8}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle">{t_atv:.2f}s</text>')
        svg.append(f'<text x="{cx}" y="{y_bar + 18}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="600" fill="#ffffff" text-anchor="middle">Ocioso</text>')
        svg.append(f'<text x="{cx}" y="{y_bar + 30}" font-family="Segoe UI, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">{oci:.1f}%</text>')

        svg.append(f'<text x="{cx}" y="{orig_y2 + chart_h + 20}" font-family="Segoe UI, sans-serif" font-size="11" fill="#475569" text-anchor="middle">Worker {w_item["worker_idx"]}</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Gráfico gerado com sucesso: {output_path}")


def gerar_todos_os_graficos(json_path="resultados_experimentais.json", output_dir="assets"):
    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    criar_svg_speedup_eficiencia(dados, os.path.join(output_dir, "speedup_eficiencia.svg"))
    criar_svg_granularidade(dados, os.path.join(output_dir, "granularidade_comparacao.svg"))
    criar_svg_balanceamento(dados, os.path.join(output_dir, "balanceamento_carga.svg"))


if __name__ == "__main__":
    gerar_todos_os_graficos()
