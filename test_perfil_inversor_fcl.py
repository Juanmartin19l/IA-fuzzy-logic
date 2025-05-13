#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test del Sistema Experto Difuso para perfiles de inversores (versión FCL)
Este script ejecuta pruebas predefinidas para verificar los diferentes perfiles de inversores
basado en la implementación Python del archivo FCL.

Tests realizados (ordenados por edad de menor a mayor):
1. Joven Emprendedor: Persona muy joven con ingresos medios-bajos, alto conocimiento y alta tolerancia al riesgo
2. Perfil Agresivo Típico: Persona joven con altos ingresos, alta tolerancia al riesgo y alto conocimiento
3. Joven Conservador: Persona joven con buenos ingresos pero perfil conservador por baja tolerancia
4. Alto Potencial y Bajo Riesgo: Persona joven con altos ingresos y conocimiento pero baja tolerancia
5. Caso Límite Moderado-Agresivo: Verificación de valores en el límite entre perfiles
6. Adulto Digital: Persona de mediana edad con alto conocimiento tecnológico y financiero
7. Perfil Moderado Típico: Persona adulta con ingresos medios, tolerancia al riesgo media y conocimiento medio
8. Adulto Diversificador: Persona adulta con ingresos altos y moderada tolerancia
9. Caso Límite Conservador-Moderado: Verificación de valores en el límite entre perfiles
10. Adulto Pre-Jubilación: Persona cerca de jubilarse con buenos ahorros e ingresos
11. Bajo Potencial y Alto Riesgo: Persona mayor con bajos ingresos pero alta tolerancia al riesgo
12. Perfil Conservador Típico: Persona mayor con bajos ingresos, baja tolerancia al riesgo y bajo conocimiento
13. Senior Inversionista: Persona mayor con altos ingresos y alto conocimiento financiero

Tests adicionales basados en la tabla de ejemplos:
14. Joven con Ingreso Bajo: Persona joven con bajos ingresos y bajo conocimiento - Perfil Conservador
15. Joven con Ingreso Alto: Persona joven con altos ingresos, bajo conocimiento pero alta tolerancia - Perfil Agresivo
16. Joven con Ingreso Medio: Persona joven con ingresos medios, alto conocimiento - Perfil Moderado
17. Adulto con Ingreso Medio: Persona adulta con ingresos medios y alta tolerancia - Perfil Agresivo
18. Mayor con Ingreso Bajo: Persona mayor con bajos ingresos, bajo conocimiento pero alta tolerancia - Perfil Conservador
"""

import sys
import os
from perfil_inversor import SistemaExpertoDifusoInversorFCL


def imprimir_resultado(nombre_test, datos, resultado, num_test):
    """Imprime el resultado de un test de forma clara y legible"""
    print("\n" + "=" * 70)
    print(f" TEST {num_test}: {nombre_test}")
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


def ejecutar_tests():
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

    # TEST 1: Joven Emprendedor
    datos_test1 = {"edad": 21, "ingresos": 2000, "conocimiento": 7, "tolerancia": 8}
    try:
        resultado1 = sed.evaluar(**datos_test1)
        imprimir_resultado("JOVEN EMPRENDEDOR", datos_test1, resultado1, 1)
        resultados.append(
            {
                "nombre": "Joven Emprendedor",
                "datos": datos_test1,
                "resultado": resultado1,
            }
        )
    except Exception as e:
        print(f"Error en test 1: {e}")

    # TEST 2: Perfil Agresivo Típico
    datos_test2 = {"edad": 25, "ingresos": 6000, "conocimiento": 8, "tolerancia": 9}
    try:
        resultado2 = sed.evaluar(**datos_test2)
        imprimir_resultado("PERFIL AGRESIVO TÍPICO", datos_test2, resultado2, 2)
        resultados.append(
            {"nombre": "Agresivo Típico", "datos": datos_test2, "resultado": resultado2}
        )
    except Exception as e:
        print(f"Error en test 2: {e}")

    # TEST 3: Joven Conservador
    datos_test3 = {"edad": 28, "ingresos": 5000, "conocimiento": 6, "tolerancia": 3}
    try:
        resultado3 = sed.evaluar(**datos_test3)
        imprimir_resultado("JOVEN CONSERVADOR", datos_test3, resultado3, 3)
        resultados.append(
            {
                "nombre": "Joven Conservador",
                "datos": datos_test3,
                "resultado": resultado3,
            }
        )
    except Exception as e:
        print(f"Error en test 3: {e}")

    # TEST 4: Alto Potencial y Bajo Riesgo
    datos_test4 = {"edad": 30, "ingresos": 8000, "conocimiento": 9, "tolerancia": 2}
    try:
        resultado4 = sed.evaluar(**datos_test4)
        imprimir_resultado("ALTO POTENCIAL Y BAJO RIESGO", datos_test4, resultado4, 4)
        resultados.append(
            {
                "nombre": "Alto Pot, Bajo Riesgo",
                "datos": datos_test4,
                "resultado": resultado4,
            }
        )
    except Exception as e:
        print(f"Error en test 4: {e}")

    # TEST 5: Caso Límite Moderado-Agresivo
    datos_test5 = {"edad": 35, "ingresos": 4500, "conocimiento": 7, "tolerancia": 7}
    try:
        resultado5 = sed.evaluar(**datos_test5)
        imprimir_resultado("CASO LÍMITE MODERADO-AGRESIVO", datos_test5, resultado5, 5)
        resultados.append(
            {"nombre": "Límite Mod-Agr", "datos": datos_test5, "resultado": resultado5}
        )
    except Exception as e:
        print(f"Error en test 5: {e}")

    # TEST 6: Adulto Digital
    datos_test6 = {"edad": 40, "ingresos": 7000, "conocimiento": 9, "tolerancia": 8}
    try:
        resultado6 = sed.evaluar(**datos_test6)
        imprimir_resultado("ADULTO DIGITAL", datos_test6, resultado6, 6)
        resultados.append(
            {
                "nombre": "Adulto Digital",
                "datos": datos_test6,
                "resultado": resultado6,
            }
        )
    except Exception as e:
        print(f"Error en test 6: {e}")

    # TEST 7: Perfil Moderado Típico
    datos_test7 = {"edad": 45, "ingresos": 3000, "conocimiento": 5, "tolerancia": 5}
    try:
        resultado7 = sed.evaluar(**datos_test7)
        imprimir_resultado("PERFIL MODERADO TÍPICO", datos_test7, resultado7, 7)
        resultados.append(
            {"nombre": "Moderado Típico", "datos": datos_test7, "resultado": resultado7}
        )
    except Exception as e:
        print(f"Error en test 7: {e}")

    # TEST 8: Adulto Diversificador
    datos_test8 = {"edad": 50, "ingresos": 9000, "conocimiento": 7, "tolerancia": 6}
    try:
        resultado8 = sed.evaluar(**datos_test8)
        imprimir_resultado("ADULTO DIVERSIFICADOR", datos_test8, resultado8, 8)
        resultados.append(
            {
                "nombre": "Adulto Diversificador",
                "datos": datos_test8,
                "resultado": resultado8,
            }
        )
    except Exception as e:
        print(f"Error en test 8: {e}")

    # TEST 9: Caso Límite Conservador-Moderado
    datos_test9 = {"edad": 55, "ingresos": 2500, "conocimiento": 4, "tolerancia": 3}
    try:
        resultado9 = sed.evaluar(**datos_test9)
        imprimir_resultado("CASO LÍMITE CONSERVADOR-MODERADO", datos_test9, resultado9, 9)
        resultados.append(
            {"nombre": "Límite Cons-Mod", "datos": datos_test9, "resultado": resultado9}
        )
    except Exception as e:
        print(f"Error en test 9: {e}")

    # TEST 10: Adulto Pre-Jubilación
    datos_test10 = {"edad": 60, "ingresos": 4000, "conocimiento": 6, "tolerancia": 4}
    try:
        resultado10 = sed.evaluar(**datos_test10)
        imprimir_resultado("ADULTO PRE-JUBILACIÓN", datos_test10, resultado10, 10)
        resultados.append(
            {
                "nombre": "Adulto Pre-Jubilación",
                "datos": datos_test10,
                "resultado": resultado10,
            }
        )
    except Exception as e:
        print(f"Error en test 10: {e}")

    # TEST 11: Bajo Potencial y Alto Riesgo
    datos_test11 = {"edad": 65, "ingresos": 1500, "conocimiento": 3, "tolerancia": 9}
    try:
        resultado11 = sed.evaluar(**datos_test11)
        imprimir_resultado("BAJO POTENCIAL Y ALTO RIESGO", datos_test11, resultado11, 11)
        resultados.append(
            {
                "nombre": "Bajo Pot, Alto Riesgo",
                "datos": datos_test11,
                "resultado": resultado11,
            }
        )
    except Exception as e:
        print(f"Error en test 11: {e}")

    # TEST 12: Perfil Conservador Típico
    datos_test12 = {"edad": 70, "ingresos": 1000, "conocimiento": 2, "tolerancia": 2}
    try:
        resultado12 = sed.evaluar(**datos_test12)
        imprimir_resultado("PERFIL CONSERVADOR TÍPICO", datos_test12, resultado12, 12)
        resultados.append(
            {
                "nombre": "Conservador Típico",
                "datos": datos_test12,
                "resultado": resultado12,
            }
        )
    except Exception as e:
        print(f"Error en test 12: {e}")

    # TEST 13: Senior Inversionista
    datos_test13 = {"edad": 75, "ingresos": 7500, "conocimiento": 8, "tolerancia": 4}
    try:
        resultado13 = sed.evaluar(**datos_test13)
        imprimir_resultado("SENIOR INVERSIONISTA", datos_test13, resultado13, 13)
        resultados.append(
            {
                "nombre": "Senior Inversionista",
                "datos": datos_test13,
                "resultado": resultado13,
            }
        )
    except Exception as e:
        print(f"Error en test 13: {e}")
        
    # TEST 14: Joven con Ingreso Bajo y Bajo Conocimiento
    datos_test14 = {"edad": 24, "ingresos": 1500, "conocimiento": 2, "tolerancia": 2}
    try:
        resultado14 = sed.evaluar(**datos_test14)
        imprimir_resultado("JOVEN INGRESO BAJO - PERFIL CONSERVADOR", datos_test14, resultado14, 14)
        resultados.append(
            {
                "nombre": "Joven Bajo Ing/Conoc",
                "datos": datos_test14,
                "resultado": resultado14,
            }
        )
    except Exception as e:
        print(f"Error en test 14: {e}")
    
    # TEST 15: Joven con Ingreso Alto y Bajo Conocimiento pero Alta Tolerancia
    datos_test15 = {"edad": 27, "ingresos": 8000, "conocimiento": 2, "tolerancia": 9}
    try:
        resultado15 = sed.evaluar(**datos_test15)
        imprimir_resultado("JOVEN INGRESO ALTO - PERFIL AGRESIVO", datos_test15, resultado15, 15)
        resultados.append(
            {
                "nombre": "Joven Alto Ing/Tol",
                "datos": datos_test15,
                "resultado": resultado15,
            }
        )
    except Exception as e:
        print(f"Error en test 15: {e}")
    
    # TEST 16: Joven con Ingreso Medio y Alto Conocimiento
    datos_test16 = {"edad": 29, "ingresos": 3500, "conocimiento": 8, "tolerancia": 5}
    try:
        resultado16 = sed.evaluar(**datos_test16)
        imprimir_resultado("JOVEN INGRESO MEDIO - PERFIL MODERADO", datos_test16, resultado16, 16)
        resultados.append(
            {
                "nombre": "Joven Med Ing/Alto Conoc",
                "datos": datos_test16,
                "resultado": resultado16,
            }
        )
    except Exception as e:
        print(f"Error en test 16: {e}")
    
    # TEST 17: Adulto con Ingreso Medio y Alta Tolerancia
    datos_test17 = {"edad": 42, "ingresos": 3800, "conocimiento": 5, "tolerancia": 8}
    try:
        resultado17 = sed.evaluar(**datos_test17)
        imprimir_resultado("ADULTO INGRESO MEDIO - PERFIL AGRESIVO", datos_test17, resultado17, 17)
        resultados.append(
            {
                "nombre": "Adulto Med Ing/Alta Tol",
                "datos": datos_test17,
                "resultado": resultado17,
            }
        )
    except Exception as e:
        print(f"Error en test 17: {e}")
    
    # TEST 18: Mayor con Ingreso Bajo y Alta Tolerancia
    datos_test18 = {"edad": 68, "ingresos": 1200, "conocimiento": 2, "tolerancia": 8}
    try:
        resultado18 = sed.evaluar(**datos_test18)
        imprimir_resultado("MAYOR INGRESO BAJO - PERFIL CONSERVADOR", datos_test18, resultado18, 18)
        resultados.append(
            {
                "nombre": "Mayor Bajo Ing/Alta Tol",
                "datos": datos_test18,
                "resultado": resultado18,
            }
        )
    except Exception as e:
        print(f"Error en test 18: {e}")


if __name__ == "__main__":
    ejecutar_tests()
