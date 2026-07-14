import json
import os
from evaluator.metrics import (
    llamar_llm, evaluar_keywords, evaluar_longitud,
    evaluar_seguridad, evaluar_claridad_con_llm, calcular_score_final
)
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import print as rprint

console = Console()

def cargar_config():
    """Carga los prompts y casos de prueba desde los archivos JSON."""
    with open("prompts/prompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)["prompts"]
    
    with open("config/test_cases.json", "r", encoding="utf-8") as f:
        casos = json.load(f)["test_cases"]
    
    return prompts, casos


def evaluar_prompt_en_caso(prompt_config: dict, caso: dict) -> dict:
    """
    Ejecuta un prompt sobre un caso de prueba y calcula todas las métricas.
    Esta es la función central del framework.
    """
    # 1. Llamar al LLM
    resultado_llm = llamar_llm(
        system_prompt=prompt_config["system_prompt"],
        user_message=caso["pregunta"],
        temperatura=prompt_config["temperatura"]
    )
    
    respuesta = resultado_llm["respuesta"]
    
    # 2. Calcular métricas
    metricas = {
        "keywords": evaluar_keywords(respuesta, caso["respuesta_esperada_keywords"]),
        "longitud": evaluar_longitud(respuesta, caso["categoria"]),
        "seguridad": evaluar_seguridad(respuesta),
        "claridad_llm": evaluar_claridad_con_llm(respuesta, caso["pregunta"])
    }
    
    # 3. Score final ponderado
    score_final = calcular_score_final(metricas)
    
    return {
        "prompt_id": prompt_config["id"],
        "prompt_nombre": prompt_config["nombre"],
        "caso_id": caso["id"],
        "categoria": caso["categoria"],
        "pregunta": caso["pregunta"],
        "respuesta": respuesta,
        "tiempo_segundos": resultado_llm["tiempo_segundos"],
        "tokens_usados": resultado_llm["tokens_usados"],
        "metricas": metricas,
        "score_final": score_final
    }


def correr_evaluacion():
    """Función principal que corre toda la evaluación."""
    console.print("\n[bold blue]🏦 PROMPT EVALUATION FRAMEWORK — INTERBANK BANKING COPILOT[/bold blue]")
    console.print("[dim]Evaluando prompts para un asistente bancario inteligente...[/dim]\n")
    
    prompts, casos = cargar_config()
    
    todos_resultados = []
    
    # Para cada prompt, probar todos los casos de prueba
    for prompt in prompts:
        console.print(f"[yellow]▶ Evaluando: {prompt['nombre']}[/yellow]")
        
        for caso in track(casos, description=f"  Casos de prueba..."):
            resultado = evaluar_prompt_en_caso(prompt, caso)
            todos_resultados.append(resultado)
    
    return todos_resultados, prompts, casos


def mostrar_tabla_resumen(resultados: list, prompts: list):
    """Muestra una tabla comparativa en la terminal."""
    
    # Calcular scores promedio por prompt
    scores_por_prompt = {}
    for resultado in resultados:
        pid = resultado["prompt_id"]
        if pid not in scores_por_prompt:
            scores_por_prompt[pid] = {
                "nombre": resultado["prompt_nombre"],
                "scores": [],
                "tiempos": [],
                "tokens": []
            }
        scores_por_prompt[pid]["scores"].append(resultado["score_final"])
        scores_por_prompt[pid]["tiempos"].append(resultado["tiempo_segundos"])
        scores_por_prompt[pid]["tokens"].append(resultado["tokens_usados"])
    
    # Tabla principal
    tabla = Table(title="📊 Resumen Comparativo de Prompts", show_header=True, header_style="bold blue")
    tabla.add_column("Prompt", style="bold")
    tabla.add_column("Score Promedio", justify="center")
    tabla.add_column("Seguridad", justify="center")
    tabla.add_column("Keywords", justify="center")
    tabla.add_column("Tiempo Prom (s)", justify="center")
    tabla.add_column("Tokens Prom", justify="center")
    
    for pid, datos in scores_por_prompt.items():
        score_prom = sum(datos["scores"]) / len(datos["scores"])
        tiempo_prom = sum(datos["tiempos"]) / len(datos["tiempos"])
        tokens_prom = sum(datos["tokens"]) / len(datos["tokens"])
        
        # Scores por categoría de métrica
        resultados_prompt = [r for r in resultados if r["prompt_id"] == pid]
        seg_prom = sum(r["metricas"]["seguridad"]["score"] for r in resultados_prompt) / len(resultados_prompt)
        kw_prom = sum(r["metricas"]["keywords"]["score"] for r in resultados_prompt) / len(resultados_prompt)
        
        # Color según score
        color = "green" if score_prom >= 0.75 else "yellow" if score_prom >= 0.5 else "red"
        
        tabla.add_row(
            datos["nombre"],
            f"[{color}]{score_prom:.1%}[/{color}]",
            f"{seg_prom:.1%}",
            f"{kw_prom:.1%}",
            f"{tiempo_prom:.2f}s",
            f"{int(tokens_prom)}"
        )
    
    console.print(tabla)
    
    # Guardar resultados en JSON para el reporte
    import json
    with open("resultados_evaluacion.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    console.print("\n[green]✅ Resultados guardados en resultados_evaluacion.json[/green]")
    console.print("[dim]Ejecuta python report.py para generar el reporte HTML completo[/dim]\n")


if __name__ == "__main__":
    resultados, prompts, casos = correr_evaluacion()
    mostrar_tabla_resumen(resultados, prompts)