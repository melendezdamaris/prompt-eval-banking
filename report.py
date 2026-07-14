import json
from datetime import datetime

def generar_reporte_html(archivo_resultados: str = "resultados_evaluacion.json"):
    with open(archivo_resultados, "r", encoding="utf-8") as f:
        resultados = json.load(f)
    
    # Agrupar por prompt
    prompts_data = {}
    for r in resultados:
        pid = r["prompt_id"]
        if pid not in prompts_data:
            prompts_data[pid] = {"nombre": r["prompt_nombre"], "resultados": []}
        prompts_data[pid]["resultados"].append(r)
    
    # Calcular promedios
    resumen = []
    for pid, data in prompts_data.items():
        scores = [r["score_final"] for r in data["resultados"]]
        resumen.append({
            "id": pid,
            "nombre": data["nombre"],
            "score_promedio": round(sum(scores) / len(scores), 3),
            "n_casos": len(scores)
        })
    
    resumen.sort(key=lambda x: x["score_promedio"], reverse=True)
    ganador = resumen[0]["nombre"]
    
    # Generar filas de la tabla de resultados
    filas_html = ""
    for r in resultados:
        score_color = "#27ae60" if r["score_final"] >= 0.75 else "#f39c12" if r["score_final"] >= 0.5 else "#e74c3c"
        seg_ok = "✅" if r["metricas"]["seguridad"]["es_segura"] else "⚠️"
        alertas = "<br>".join(r["metricas"]["seguridad"]["alertas"])
        
        filas_html += f"""
        <tr>
            <td><span class="badge">{r['caso_id']}</span></td>
            <td>{r['categoria']}</td>
            <td class="prompt-name">{r['prompt_nombre']}</td>
            <td style="max-width:300px;font-size:0.85em;color:#555">{r['respuesta'][:150]}...</td>
            <td style="font-weight:bold;color:{score_color}">{r['score_final']:.1%}</td>
            <td>{r['metricas']['keywords']['score']:.1%}</td>
            <td>{seg_ok}<br><small style="color:#888">{alertas}</small></td>
            <td>{r['tiempo_segundos']}s</td>
        </tr>"""
    
    # Barras del resumen
    barras_html = ""
    for item in resumen:
        pct = item["score_promedio"] * 100
        color = "#27ae60" if pct >= 75 else "#f39c12" if pct >= 50 else "#e74c3c"
        barras_html += f"""
        <div class="bar-row">
            <div class="bar-label">{item['nombre']}</div>
            <div class="bar-container">
                <div class="bar" style="width:{pct}%;background:{color}"></div>
            </div>
            <div class="bar-score">{pct:.1f}%</div>
        </div>"""
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Prompt Evaluation Report — Interbank Banking Copilot</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7fa; color: #333; }}
        .header {{ background: linear-gradient(135deg, #1A3C5E, #2980b9); color: white; padding: 40px; }}
        .header h1 {{ font-size: 2em; margin-bottom: 8px; }}
        .header p {{ opacity: 0.8; }}
        .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; }}
        .card {{ background: white; border-radius: 12px; padding: 30px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); }}
        .winner {{ border-left: 5px solid #27ae60; }}
        h2 {{ color: #1A3C5E; margin-bottom: 20px; font-size: 1.3em; }}
        .bar-row {{ display: flex; align-items: center; margin-bottom: 14px; }}
        .bar-label {{ width: 220px; font-size: 0.9em; font-weight: 600; }}
        .bar-container {{ flex: 1; background: #ecf0f1; border-radius: 6px; height: 28px; overflow: hidden; }}
        .bar {{ height: 100%; border-radius: 6px; transition: width 0.8s ease; }}
        .bar-score {{ width: 60px; text-align: right; font-weight: bold; font-size: 0.95em; padding-left: 12px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.88em; }}
        th {{ background: #1A3C5E; color: white; padding: 12px 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; vertical-align: top; }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{ background: #e8f4f8; color: #1A3C5E; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }}
        .prompt-name {{ font-weight: 600; color: #1A3C5E; }}
        .tag {{ display: inline-block; background: #E8761A; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin-right: 8px; }}
        .meta {{ color: #888; font-size: 0.85em; margin-top: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 Prompt Evaluation Report</h1>
        <p>Interbank Banking Copilot — Comparativa de versiones de prompts</p>
        <p class="meta">Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Modelo: llama-3.1-8b-instant | Casos evaluados: {len(resultados)}</p>
    </div>
    <div class="container">
        <div class="card winner">
            <h2>🏆 Mejor Prompt: {ganador}</h2>
            <p>Basado en score ponderado (Seguridad 35% · Claridad LLM 30% · Keywords 20% · Longitud 15%)</p>
        </div>
        <div class="card">
            <h2>📊 Score Promedio por Versión de Prompt</h2>
            {barras_html}
        </div>
        <div class="card">
            <h2>🔍 Resultados Detallados por Caso de Prueba</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th><th>Categoría</th><th>Prompt</th>
                        <th>Respuesta (preview)</th><th>Score Final</th>
                        <th>Keywords</th><th>Seguridad</th><th>Tiempo</th>
                    </tr>
                </thead>
                <tbody>{filas_html}</tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    with open("reporte_evaluacion.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ Reporte generado: reporte_evaluacion.html")
    print(f"🏆 Mejor prompt: {ganador}")

if __name__ == "__main__":
    generar_reporte_html()