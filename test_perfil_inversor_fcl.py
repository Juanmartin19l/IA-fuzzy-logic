#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test del Sistema Experto Difuso para perfiles de inversores (versión FCL)
Este script ejecuta pruebas predefinidas para verificar los diferentes perfiles de inversores
basado en la implementación Python del archivo FCL.

Tests realizados:
1. Perfil Conservador Típico: Persona mayor con bajos ingresos, baja tolerancia al riesgo y bajo conocimiento
2. Perfil Moderado Típico: Persona adulta con ingresos medios, tolerancia al riesgo media y conocimiento medio
3. Perfil Agresivo Típico: Persona joven con altos ingresos, alta tolerancia al riesgo y alto conocimiento
4. Caso Límite Conservador-Moderado: Verificación de valores en el límite entre perfiles
5. Caso Límite Moderado-Agresivo: Verificación de valores en el límite entre perfiles
6. Alto Potencial y Bajo Riesgo: Casos donde el potencial y riesgo no correlacionan
7. Bajo Potencial y Alto Riesgo: Casos donde el potencial y riesgo no correlacionan
"""

import sys
import os
import matplotlib.pyplot as plt
from perfil_inversor import SistemaExpertoDifusoInversorFCL


def imprimir_resultado(nombre_test, datos, resultado):
    """Imprime el resultado de un test de forma clara y legible"""
    print("\n" + "=" * 70)
    print(f" TEST: {nombre_test}")
    print("=" * 70)
    print(f"- Edad: {datos['edad']} años")
    print(f"- Ingresos mensuales: ${datos['ingresos']}")
    print(f"- Conocimiento financiero: {datos['conocimiento']}/10")
    print(f"- Tolerancia al riesgo: {datos['tolerancia']}/10")
    print("-" * 70)
    print(f"- Potencial de inversión: {resultado['potencial']:.2f}/10")
    print(f"- Nivel de riesgo: {resultado['riesgo']:.2f}/10")
    print(
        f"RESULTADO: Perfil {resultado['perfil']} ({resultado['valor_perfil']:.2f}/3)"
    )
    print("=" * 70)


def ejecutar_tests(mostrar_graficas=False):
    """
    Ejecuta una serie de tests predefinidos para diferentes perfiles de inversores

    Args:
        mostrar_graficas (bool): Si es True, muestra gráficas de los resultados
    """
    # Limpiar pantalla
    os.system("cls" if os.name == "nt" else "clear")

    # Inicializar el sistema experto
    try:
        sed = SistemaExpertoDifusoInversorFCL()
    except Exception as e:
        print(f"Error al inicializar el sistema experto: {e}")
        sys.exit(1)

    print("\n\n" + "*" * 80)
    print("*" + " " * 24 + "TESTS DEL SISTEMA EXPERTO FCL" + " " * 25 + "*")
    print("*" + " " * 78 + "*")
    print(
        "* Este script prueba diferentes combinaciones de valores para obtener distintos"
        + " " * 7
        + "*"
    )
    print(
        "* perfiles de inversores (conservador, moderado y agresivo)." + " " * 21 + "*"
    )
    print("*" * 80 + "\n")

    # Almacenar resultados para gráfica
    resultados = []

    # TEST 1: Perfil Conservador Típico
    datos_test1 = {"edad": 70, "ingresos": 1000, "conocimiento": 2, "tolerancia": 2}
    try:
        resultado1 = sed.evaluar(**datos_test1)
        imprimir_resultado("PERFIL CONSERVADOR TÍPICO", datos_test1, resultado1)
        resultados.append(
            {
                "nombre": "Conservador Típico",
                "datos": datos_test1,
                "resultado": resultado1,
            }
        )
    except Exception as e:
        print(f"Error en test 1: {e}")

    # TEST 2: Perfil Moderado Típico
    datos_test2 = {"edad": 45, "ingresos": 3000, "conocimiento": 5, "tolerancia": 5}
    try:
        resultado2 = sed.evaluar(**datos_test2)
        imprimir_resultado("PERFIL MODERADO TÍPICO", datos_test2, resultado2)
        resultados.append(
            {"nombre": "Moderado Típico", "datos": datos_test2, "resultado": resultado2}
        )
    except Exception as e:
        print(f"Error en test 2: {e}")

    # TEST 3: Perfil Agresivo Típico
    datos_test3 = {"edad": 25, "ingresos": 6000, "conocimiento": 8, "tolerancia": 9}
    try:
        resultado3 = sed.evaluar(**datos_test3)
        imprimir_resultado("PERFIL AGRESIVO TÍPICO", datos_test3, resultado3)
        resultados.append(
            {"nombre": "Agresivo Típico", "datos": datos_test3, "resultado": resultado3}
        )
    except Exception as e:
        print(f"Error en test 3: {e}")

    # TEST 4: Caso Límite Conservador-Moderado
    datos_test4 = {"edad": 55, "ingresos": 2500, "conocimiento": 4, "tolerancia": 3}
    try:
        resultado4 = sed.evaluar(**datos_test4)
        imprimir_resultado("CASO LÍMITE CONSERVADOR-MODERADO", datos_test4, resultado4)
        resultados.append(
            {"nombre": "Límite Cons-Mod", "datos": datos_test4, "resultado": resultado4}
        )
    except Exception as e:
        print(f"Error en test 4: {e}")

    # TEST 5: Caso Límite Moderado-Agresivo
    datos_test5 = {"edad": 35, "ingresos": 4500, "conocimiento": 7, "tolerancia": 7}
    try:
        resultado5 = sed.evaluar(**datos_test5)
        imprimir_resultado("CASO LÍMITE MODERADO-AGRESIVO", datos_test5, resultado5)
        resultados.append(
            {"nombre": "Límite Mod-Agr", "datos": datos_test5, "resultado": resultado5}
        )
    except Exception as e:
        print(f"Error en test 5: {e}")

    # TEST 6: Alto Potencial y Bajo Riesgo
    datos_test6 = {"edad": 30, "ingresos": 8000, "conocimiento": 9, "tolerancia": 2}
    try:
        resultado6 = sed.evaluar(**datos_test6)
        imprimir_resultado("ALTO POTENCIAL Y BAJO RIESGO", datos_test6, resultado6)
        resultados.append(
            {
                "nombre": "Alto Pot, Bajo Riesgo",
                "datos": datos_test6,
                "resultado": resultado6,
            }
        )
    except Exception as e:
        print(f"Error en test 6: {e}")

    # TEST 7: Bajo Potencial y Alto Riesgo
    datos_test7 = {"edad": 65, "ingresos": 1500, "conocimiento": 3, "tolerancia": 9}
    try:
        resultado7 = sed.evaluar(**datos_test7)
        imprimir_resultado("BAJO POTENCIAL Y ALTO RIESGO", datos_test7, resultado7)
        resultados.append(
            {
                "nombre": "Bajo Pot, Alto Riesgo",
                "datos": datos_test7,
                "resultado": resultado7,
            }
        )
    except Exception as e:
        print(f"Error en test 7: {e}")

    # Mostrar gráficas de resultados si se solicita
    if mostrar_graficas and resultados:
        visualizar_comparacion(resultados)


def visualizar_comparacion(resultados):
    """
    Visualiza una comparación gráfica de los resultados de los tests

    Args:
        resultados (list): Lista de resultados de los tests
    """
    # Extraer datos para gráficas
    nombres = [r["nombre"] for r in resultados]
    perfiles = [r["resultado"]["valor_perfil"] for r in resultados]
    potenciales = [r["resultado"]["potencial"] for r in resultados]
    riesgos = [r["resultado"]["riesgo"] for r in resultados]

    # Crear figura con 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(12, 15))

    # Gráfica 1: Valor del Perfil
    bars1 = ax1.bar(nombres, perfiles, color="darkblue", alpha=0.7)
    ax1.set_title("Comparación de Perfiles de Inversión", fontsize=14)
    ax1.set_ylabel("Valor del Perfil (0-3)")
    ax1.set_ylim(0, 3)
    ax1.axhline(
        y=1.0, color="r", linestyle="--", alpha=0.5
    )  # Línea para el límite Conservador-Moderado
    ax1.axhline(
        y=2.0, color="r", linestyle="--", alpha=0.5
    )  # Línea para el límite Moderado-Agresivo
    ax1.text(
        ax1.get_xlim()[1], 0.5, "Conservador", ha="right", va="center", color="darkred"
    )
    ax1.text(
        ax1.get_xlim()[1], 1.5, "Moderado", ha="right", va="center", color="darkred"
    )
    ax1.text(
        ax1.get_xlim()[1], 2.5, "Agresivo", ha="right", va="center", color="darkred"
    )

    # Rotar etiquetas del eje x para mejor legibilidad
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Mostrar valores en las barras
    for bar in bars1:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.1,
            f"{height:.2f}",
            ha="center",
            va="bottom",
        )

    # Gráfica 2: Potencial de Inversión
    bars2 = ax2.bar(nombres, potenciales, color="darkgreen", alpha=0.7)
    ax2.set_title("Comparación de Potencial de Inversión", fontsize=14)
    ax2.set_ylabel("Potencial (0-10)")
    ax2.set_ylim(0, 10)

    # Mostrar valores en las barras
    for bar in bars2:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.2,
            f"{height:.2f}",
            ha="center",
            va="bottom",
        )

    # Rotar etiquetas del eje x para mejor legibilidad
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Gráfica 3: Nivel de Riesgo
    bars3 = ax3.bar(nombres, riesgos, color="darkred", alpha=0.7)
    ax3.set_title("Comparación de Nivel de Riesgo", fontsize=14)
    ax3.set_ylabel("Riesgo (0-10)")
    ax3.set_ylim(0, 10)

    # Mostrar valores en las barras
    for bar in bars3:
        height = bar.get_height()
        ax3.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.2,
            f"{height:.2f}",
            ha="center",
            va="bottom",
        )

    # Rotar etiquetas del eje x para mejor legibilidad
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Ajustar layout y mostrar
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Determinar si mostrar gráficas basado en argumentos de línea de comandos
    import argparse

    parser = argparse.ArgumentParser(
        description="Tests del Sistema Experto Difuso para perfiles de inversores (FCL)"
    )
    parser.add_argument(
        "-g",
        "--graficas",
        action="store_true",
        help="Mostrar gráficas comparativas de los resultados",
    )
    args = parser.parse_args()

    ejecutar_tests(mostrar_graficas=args.graficas)
