#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test del Sistema Experto Difuso para perfiles de inversores
Este script ejecuta pruebas predefinidas para verificar los diferentes perfiles de inversores
"""

import sys
from sistema_experto_inversor import SistemaExpertoDifusoInversor


def imprimir_resultado(nombre_test, datos, resultado):
    """Imprime el resultado de un test de forma clara y legible"""
    print("\n" + "=" * 65)
    print(f" TEST: {nombre_test}")
    print("=" * 65)
    print(f"- Edad: {datos['edad']} años")
    print(f"- Ingresos mensuales: ${datos['ingresos']}")
    print(f"- Tolerancia al riesgo: {datos['tolerancia']}/10")
    print(f"- Horizonte de inversión: {datos['horizonte']} años")
    print("-" * 65)
    print(
        f"RESULTADO: Perfil {resultado['perfil']} ({resultado['valor_numerico']:.2f}/100)"
    )
    print("=" * 65)


def ejecutar_tests():
    """Ejecuta una serie de tests predefinidos para diferentes perfiles de inversores"""

    # Inicializar el sistema experto
    try:
        sed = SistemaExpertoDifusoInversor()
    except Exception as e:
        print(f"Error al inicializar el sistema experto: {e}")
        sys.exit(1)

    print("\n\n" + "*" * 80)
    print("*" + " " * 30 + "TESTS DEL SISTEMA EXPERTO" + " " * 29 + "*")
    print("*" + " " * 78 + "*")
    print(
        "* Este script prueba diferentes combinaciones de valores para obtener distintos"
        + " " * 7
        + "*"
    )
    print(
        "* perfiles de inversores (conservador, moderado y arriesgado)."
        + " " * 21
        + "*"
    )
    print("*" * 80 + "\n")

    # TEST 1: Perfil Conservador Típico
    datos_test1 = {"edad": 70, "ingresos": 30000, "tolerancia": 2, "horizonte": 3}
    try:
        resultado1 = sed.evaluar(**datos_test1)
        imprimir_resultado("PERFIL CONSERVADOR TÍPICO", datos_test1, resultado1)
    except Exception as e:
        print(f"Error en test 1: {e}")

    # TEST 2: Perfil Moderado Típico
    datos_test2 = {"edad": 45, "ingresos": 60000, "tolerancia": 6, "horizonte": 10}
    try:
        resultado2 = sed.evaluar(**datos_test2)
        imprimir_resultado("PERFIL MODERADO TÍPICO", datos_test2, resultado2)
    except Exception as e:
        print(f"Error en test 2: {e}")

    # TEST 3: Perfil Arriesgado Típico
    datos_test3 = {"edad": 25, "ingresos": 100000, "tolerancia": 9, "horizonte": 30}
    try:
        resultado3 = sed.evaluar(**datos_test3)
        imprimir_resultado("PERFIL ARRIESGADO TÍPICO", datos_test3, resultado3)
    except Exception as e:
        print(f"Error en test 3: {e}")

    # TEST 4: Caso Extremo - Muy Conservador
    datos_test4 = {"edad": 85, "ingresos": 15000, "tolerancia": 1, "horizonte": 2}
    try:
        resultado4 = sed.evaluar(**datos_test4)
        imprimir_resultado("CASO EXTREMO - MUY CONSERVADOR", datos_test4, resultado4)
    except Exception as e:
        print(f"Error en test 4: {e}")

    # TEST 5: Caso Extremo - Muy Arriesgado
    datos_test5 = {"edad": 22, "ingresos": 120000, "tolerancia": 10, "horizonte": 40}
    try:
        resultado5 = sed.evaluar(**datos_test5)
        imprimir_resultado("CASO EXTREMO - MUY ARRIESGADO", datos_test5, resultado5)
    except Exception as e:
        print(f"Error en test 5: {e}")

    # TEST 6: Caso Mixto 1 (Joven con perfil conservador)
    datos_test6 = {"edad": 25, "ingresos": 20000, "tolerancia": 2, "horizonte": 3}
    try:
        resultado6 = sed.evaluar(**datos_test6)
        imprimir_resultado("CASO MIXTO - JOVEN CONSERVADOR", datos_test6, resultado6)
    except Exception as e:
        print(f"Error en test 6: {e}")

    # TEST 7: Caso Mixto 2 (Mayor con perfil arriesgado)
    datos_test7 = {"edad": 65, "ingresos": 120000, "tolerancia": 8, "horizonte": 20}
    try:
        resultado7 = sed.evaluar(**datos_test7)
        imprimir_resultado(
            "CASO MIXTO - MAYOR CON TENDENCIA ARRIESGADA", datos_test7, resultado7
        )
    except Exception as e:
        print(f"Error en test 7: {e}")

    # TEST 8: Caso Valores Medios (cerca al límite moderado-arriesgado)
    datos_test8 = {"edad": 40, "ingresos": 75000, "tolerancia": 7, "horizonte": 15}
    try:
        resultado8 = sed.evaluar(**datos_test8)
        imprimir_resultado(
            "VALORES MEDIOS (MODERADO-ARRIESGADO)", datos_test8, resultado8
        )
    except Exception as e:
        print(f"Error en test 8: {e}")

    # TEST 9: Caso Valores Medios (cerca al límite conservador-moderado)
    datos_test9 = {"edad": 55, "ingresos": 45000, "tolerancia": 4, "horizonte": 8}
    try:
        resultado9 = sed.evaluar(**datos_test9)
        imprimir_resultado(
            "VALORES MEDIOS (CONSERVADOR-MODERADO)", datos_test9, resultado9
        )
    except Exception as e:
        print(f"Error en test 9: {e}")

    # TEST 10: Valores que podrían causar conflicto
    datos_test10 = {"edad": 30, "ingresos": 5000, "tolerancia": 9, "horizonte": 25}
    try:
        resultado10 = sed.evaluar(**datos_test10)
        imprimir_resultado(
            "VALORES CONFLICTIVOS (INGRESOS BAJOS CON ALTA TOLERANCIA)",
            datos_test10,
            resultado10,
        )
    except Exception as e:
        print(f"Error en test 10: {e}")

    print("\n\nResumen de los perfiles de prueba:")
    print("-" * 65)
    print(
        "1. Perfil Conservador Típico:        Persona mayor, ingresos moderados/bajos, baja tolerancia al riesgo, horizonte corto"
    )
    print(
        "2. Perfil Moderado Típico:           Persona de mediana edad, ingresos medios, tolerancia media, horizonte medio"
    )
    print(
        "3. Perfil Arriesgado Típico:         Persona joven, ingresos altos, alta tolerancia al riesgo, horizonte largo"
    )
    print(
        "4. Caso Extremo (Muy Conservador):   Persona muy mayor, ingresos bajos, mínima tolerancia al riesgo, horizonte muy corto"
    )
    print(
        "5. Caso Extremo (Muy Arriesgado):    Persona muy joven, ingresos muy altos, máxima tolerancia al riesgo, horizonte máximo"
    )
    print(
        "6. Caso Mixto (Joven Conservador):   Joven con características conservadoras"
    )
    print("7. Caso Mixto (Mayor Arriesgado):    Mayor con características arriesgadas")
    print(
        "8. Valores Medios (Mod-Arr):         Cerca del límite entre moderado y arriesgado"
    )
    print(
        "9. Valores Medios (Con-Mod):         Cerca del límite entre conservador y moderado"
    )
    print(
        "10. Valores Conflictivos:            Combinación de valores que pueden entrar en conflicto"
    )
    print("-" * 65)


if __name__ == "__main__":
    ejecutar_tests()
