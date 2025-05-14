"""
Sistema Experto Difuso para determinar el perfil de un inversor
Punto de entrada principal del programa
"""

import traceback
from utils import clear_screen
from sistema_experto import SistemaExpertoDifusoInversorFCL
from visualizacion import VisualizadorSistemaExperto


def ejecutar_sistema():
    """
    Función principal para ejecutar el sistema experto difuso.

    Esta función maneja la interacción con el usuario, capturando los datos de entrada,
    validándolos, procesándolos a través del sistema experto difuso y presentando
    los resultados al usuario de manera clara y comprensible.
    """
    try:
        # Inicializar el sistema experto de inferencia difusa
        sed = SistemaExpertoDifusoInversorFCL()
        visualizador = VisualizadorSistemaExperto()

        # Configurar interfaz de usuario por consola
        clear_screen()
        print("\n" + "=" * 70)
        print("   SISTEMA EXPERTO BASADO EN LÓGICA DIFUSA PARA PERFILES DE INVERSIÓN")
        print("   Implementación Avanzada en Python con Scikit-Fuzzy")
        print("=" * 70)

        while True:
            try:
                print("\n╔" + "═" * 66 + "╗")
                print(
                    "║  Ingrese los datos del inversor (o escriba 'salir' para terminar)  ║"
                )
                print("╚" + "═" * 66 + "╝")

                # Validación de edad con interfaz mejorada
                while True:
                    entrada = input("\n➤ Edad del inversor (20-100 años): ")

                    if entrada.lower() in ["salir", "exit", "q"]:
                        break

                    try:
                        edad = int(entrada)
                        if 20 <= edad <= 100:
                            break
                        else:
                            print("⚠️  Error: La edad debe estar entre 20 y 100 años.")
                    except ValueError:
                        print("Error: Por favor, ingrese un número entero válido.")

                if entrada.lower() in ["salir", "exit", "q"]:
                    break

                # Validación de ingresos con interfaz mejorada
                while True:
                    try:
                        ingresos_str = input("➤ Ingresos mensuales (1-15,000): ")
                        ingresos = int(ingresos_str)
                        if 1 <= ingresos <= 15000:
                            break
                        else:
                            print(
                                "⚠️  Error: Los ingresos deben estar entre 1 y 15,000."
                            )
                    except ValueError:
                        print("⚠️  Error: Por favor, ingrese un número entero válido.")

                # Validación de conocimiento financiero con interfaz mejorada
                while True:
                    try:
                        print("\nEscala de conocimiento financiero:")
                        print("  1-3: Conocimiento básico")
                        print("  4-7: Conocimiento intermedio")
                        print("  8-10: Conocimiento avanzado")
                        conocimiento_str = input(
                            "➤ Nivel de conocimiento financiero (1-10): "
                        )
                        conocimiento = float(conocimiento_str)
                        if 1 <= conocimiento <= 10:
                            break
                        else:
                            print(
                                "⚠️  Error: El nivel de conocimiento debe estar entre 1 y 10."
                            )
                    except ValueError:
                        print("⚠️  Error: Por favor, ingrese un número válido.")

                # Validación de tolerancia al riesgo con interfaz mejorada
                while True:
                    try:
                        print("\nEscala de tolerancia al riesgo:")
                        print("  1-3: Baja tolerancia (prefiere seguridad)")
                        print("  4-7: Tolerancia media (acepta cierto riesgo)")
                        print(
                            "  8-10: Alta tolerancia (asume riesgos por mayor rentabilidad)"
                        )
                        tolerancia_str = input("➤ Tolerancia al riesgo (1-10): ")
                        tolerancia = float(tolerancia_str)
                        if 1 <= tolerancia <= 10:
                            break
                        else:
                            print(
                                "⚠️  Error: La tolerancia al riesgo debe estar entre 1 y 10."
                            )
                    except ValueError:
                        print("⚠️  Error: Por favor, ingrese un número válido.")

                # Evaluar perfil mediante el sistema de inferencia difusa
                print("\n⏳ Procesando mediante inferencia difusa...")
                resultado = sed.evaluar(edad, ingresos, conocimiento, tolerancia)

                # Presentación visual de resultados
                print("\n" + "┌" + "─" * 68 + "┐")
                print(
                    "│"
                    + " RESULTADO DEL ANÁLISIS DE PERFIL DE INVERSIÓN ".center(68)
                    + "│"
                )
                print("└" + "─" * 68 + "┘")

                # Sección de parámetros de entrada
                print("\n🔹 PARÁMETROS DE ENTRADA:")
                print("  • Edad: " + str(edad) + " años")
                print("  • Ingresos mensuales: $" + str(ingresos))
                print("  • Conocimiento financiero: " + str(conocimiento) + "/10")
                print("  • Tolerancia al riesgo: " + str(tolerancia) + "/10")

                # Sección de resultados de la inferencia
                print("\n🔹 RESULTADOS DE LA INFERENCIA DIFUSA:")
                print(
                    "  • Potencial de inversión: " + f"{resultado['potencial']:.2f}/10"
                )
                print("  • Nivel de riesgo: " + f"{resultado['riesgo']:.2f}/10")

                # Sección de perfil resultante
                print("\n🔹 PERFIL DE INVERSIÓN RECOMENDADO:")

                # Personalización del mensaje según el perfil (5 perfiles)
                if resultado["perfil"] == "Muy Conservador":
                    print(
                        "  • Perfil: \033[94mMUY CONSERVADOR\033[0m"
                    )  # Azul para muy conservador
                    print(
                        "  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10"
                    )
                    print(
                        "  • Recomendación: Inversiones de mínimo riesgo principalmente en"
                    )
                    print(
                        "    depósitos a plazo fijo, cuentas de ahorro y bonos gubernamentales."
                    )
                    print("    Máxima prioridad a la preservación del capital.")
                elif resultado["perfil"] == "Conservador":
                    print(
                        "  • Perfil: \033[96mCONSERVADOR\033[0m"
                    )  # Cyan para conservador
                    print(
                        "  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10"
                    )
                    print(
                        "  • Recomendación: Inversiones de bajo riesgo como bonos de alta calidad,"
                    )
                    print(
                        "    fondos de renta fija y una pequeña parte (10-20%) en renta variable."
                    )
                elif resultado["perfil"] == "Moderado":
                    print(
                        "  • Perfil: \033[93mMODERADO\033[0m"
                    )  # Amarillo para moderado
                    print(
                        "  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10"
                    )
                    print(
                        "  • Recomendación: Cartera equilibrada con aproximadamente 40-60% en"
                    )
                    print("    renta fija y 40-60% en renta variable diversificada.")
                elif resultado["perfil"] == "Agresivo":
                    print(
                        "  • Perfil: \033[91mAGRESIVO\033[0m"
                    )  # Rojo claro para agresivo
                    print(
                        "  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10"
                    )
                    print(
                        "  • Recomendación: Mayor proporción (70-80%) en renta variable,"
                    )
                    print(
                        "    fondos de inversión de alto rendimiento y menor parte en renta fija."
                    )
                else:  # Muy Agresivo
                    print(
                        "  • Perfil: \033[31;1mMUY AGRESIVO\033[0m"
                    )  # Rojo intenso para muy agresivo
                    print(
                        "  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10"
                    )
                    print(
                        "  • Recomendación: Cartera principalmente en activos de alto riesgo/rendimiento,"
                    )
                    print(
                        "    como acciones de mercados emergentes, capital privado, derivados y"
                    )
                    print(
                        "    criptomonedas. Máxima prioridad al crecimiento del capital."
                    )

                print("\n" + "─" * 70)

                # Opciones de visualización con instrucciones mejoradas
                ver_graficas = input(
                    "\n¿Desea ver las gráficas de las funciones de membresía? (s/n): "
                )
                if ver_graficas.lower() in ["s", "si", "sí", "y", "yes"]:
                    visualizador.visualizar_variables(sed)

                ver_resultado = input(
                    "\n¿Desea ver la gráfica del proceso de inferencia? (s/n): "
                )
                if ver_resultado.lower() in ["s", "si", "sí", "y", "yes"]:
                    visualizador.visualizar_resultado(sed)

                print("\n" + "═" * 70)

            except ValueError as e:
                print(f"\n❌ Error de validación: {e}")
                print("   Por favor, corrija los valores e intente nuevamente.")
            except Exception as e:
                print(f"\n❌ Error inesperado: {str(e)}")

        print("\n" + "╔" + "═" * 68 + "╗")
        print(
            "║"
            + " ¡Gracias por utilizar el Sistema Experto de Perfiles de Inversión! ".center(
                68
            )
            + "║"
        )
        print("╚" + "═" * 68 + "╝")
        print("\nDesarrollado con tecnología de Lógica Difusa (Fuzzy Logic)")
        print("© Sistema Experto Profesional v2.0\n")

    except Exception as e:
        print(f"\n❌ ERROR FATAL EN EL SISTEMA: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        print("Detalles técnicos:")

        traceback.print_exc()
        print("\nEl sistema no puede continuar. Por favor, reinicie la aplicación.")


if __name__ == "__main__":
    ejecutar_sistema()
