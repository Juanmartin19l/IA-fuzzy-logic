#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema Experto Difuso para determinar el perfil de un inversor
Utiliza scikit-fuzzy para implementar un sistema de inferencia Mamdani
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os
import sys


def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system("cls" if os.name == "nt" else "clear")


class SistemaExpertoDifusoInversor:
    """
    Sistema Experto Difuso para determinar el perfil de un inversor basado en:
    - Edad del inversor
    - Nivel de ingresos mensuales
    - Tolerancia al riesgo
    - Horizonte de inversión
    """

    def __init__(self):
        """Inicializa el sistema experto difuso"""
        # Definir variables de entrada (universos de discurso)
        self.edad = ctrl.Antecedent(np.arange(18, 91, 1), "edad")
        # Ajustamos el rango de ingresos para evitar problemas con valores bajos
        self.ingresos = ctrl.Antecedent(np.arange(0, 150001, 1000), "ingresos")
        self.tolerancia = ctrl.Antecedent(np.arange(0, 11, 1), "tolerancia")
        self.horizonte = ctrl.Antecedent(np.arange(1, 41, 1), "horizonte")

        # Definir variables de salida
        self.perfil = ctrl.Consequent(np.arange(0, 101, 1), "perfil")

        # Definir las funciones de pertenencia para cada variable
        self.definir_funciones_membresia()

        # Definir reglas del sistema
        self.reglas = self.definir_reglas()

        # Crear el sistema de control
        try:
            self.sistema_ctrl = ctrl.ControlSystem(self.reglas)
            self.simulacion = ctrl.ControlSystemSimulation(self.sistema_ctrl)
        except Exception as e:
            print(f"Error al crear el sistema de control: {e}")
            sys.exit(1)

    def definir_funciones_membresia(self):
        """Define las funciones de membresía para todas las variables"""
        # Funciones de membresía para EDAD
        self.edad["joven"] = fuzz.trapmf(self.edad.universe, [18, 18, 30, 40])
        self.edad["medio"] = fuzz.trapmf(self.edad.universe, [35, 45, 55, 65])
        self.edad["mayor"] = fuzz.trapmf(self.edad.universe, [60, 70, 90, 90])

        # Funciones de membresía para INGRESOS - Ampliamos el rango "bajo" para incluir valores muy pequeños
        self.ingresos["bajo"] = fuzz.trapmf(
            self.ingresos.universe, [0, 0, 30000, 50000]
        )
        self.ingresos["medio"] = fuzz.trapmf(
            self.ingresos.universe, [40000, 60000, 80000, 100000]
        )
        self.ingresos["alto"] = fuzz.trapmf(
            self.ingresos.universe, [90000, 120000, 150000, 150000]
        )

        # Funciones de membresía para TOLERANCIA AL RIESGO (escala 0-10)
        self.tolerancia["baja"] = fuzz.trapmf(self.tolerancia.universe, [0, 0, 3, 5])
        self.tolerancia["media"] = fuzz.trimf(self.tolerancia.universe, [4, 6, 8])
        self.tolerancia["alta"] = fuzz.trapmf(self.tolerancia.universe, [7, 9, 10, 10])

        # Funciones de membresía para HORIZONTE DE INVERSIÓN (en años)
        self.horizonte["corto"] = fuzz.trapmf(self.horizonte.universe, [1, 1, 3, 5])
        self.horizonte["medio"] = fuzz.trapmf(self.horizonte.universe, [4, 7, 12, 15])
        self.horizonte["largo"] = fuzz.trapmf(self.horizonte.universe, [12, 20, 40, 40])

        # Funciones de membresía para PERFIL DE INVERSOR (salida)
        self.perfil["conservador"] = fuzz.trapmf(self.perfil.universe, [0, 0, 30, 50])
        self.perfil["moderado"] = fuzz.trapmf(self.perfil.universe, [40, 50, 60, 70])
        self.perfil["arriesgado"] = fuzz.trapmf(
            self.perfil.universe, [60, 80, 100, 100]
        )

    def definir_reglas(self):
        """Define el conjunto de reglas difusas para el sistema"""
        reglas = []

        # Agregamos reglas más simples para manejar valores extremos

        # Regla para ingresos muy bajos
        reglas.append(ctrl.Rule(self.ingresos["bajo"], self.perfil["conservador"]))

        # Regla para determinar el perfil basado solo en la edad
        reglas.append(ctrl.Rule(self.edad["mayor"], self.perfil["conservador"]))

        reglas.append(ctrl.Rule(self.edad["joven"], self.perfil["moderado"]))

        # Regla para horizonte largo
        reglas.append(ctrl.Rule(self.horizonte["largo"], self.perfil["moderado"]))

        # REGLA 1: Si es joven, ingresos altos, tolerancia alta y horizonte largo, entonces perfil arriesgado
        reglas.append(
            ctrl.Rule(
                self.edad["joven"]
                & self.ingresos["alto"]
                & self.tolerancia["alta"]
                & self.horizonte["largo"],
                self.perfil["arriesgado"],
            )
        )

        # REGLA 2: Si es mayor, ingresos bajos y tolerancia baja, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["bajo"] & self.tolerancia["baja"],
                self.perfil["conservador"],
            )
        )

        # REGLA 3: Si es medio, ingresos medios y tolerancia media, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.ingresos["medio"] & self.tolerancia["media"],
                self.perfil["moderado"],
            )
        )

        # REGLA 4: Si es joven, ingresos bajos, tolerancia alta y horizonte largo, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["joven"]
                & self.ingresos["bajo"]
                & self.tolerancia["alta"]
                & self.horizonte["largo"],
                self.perfil["moderado"],
            )
        )

        # REGLA 5: Si es mayor, ingresos altos y tolerancia baja, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["alto"] & self.tolerancia["baja"],
                self.perfil["conservador"],
            )
        )

        # REGLA 6: Si es joven, ingresos medios, tolerancia media y horizonte medio, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["joven"]
                & self.ingresos["medio"]
                & self.tolerancia["media"]
                & self.horizonte["medio"],
                self.perfil["moderado"],
            )
        )

        # REGLA 7: Si es joven, tolerancia alta y horizonte largo, entonces perfil arriesgado
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.tolerancia["alta"] & self.horizonte["largo"],
                self.perfil["arriesgado"],
            )
        )

        # REGLA 8: Si es mayor, tolerancia baja y horizonte corto, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.tolerancia["baja"] & self.horizonte["corto"],
                self.perfil["conservador"],
            )
        )

        # REGLA 9: Si es medio, ingresos altos, tolerancia alta, entonces perfil arriesgado
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.ingresos["alto"] & self.tolerancia["alta"],
                self.perfil["arriesgado"],
            )
        )

        # REGLA 10: Si ingresos bajos, tolerancia baja y horizonte corto, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.ingresos["bajo"]
                & self.tolerancia["baja"]
                & self.horizonte["corto"],
                self.perfil["conservador"],
            )
        )

        # REGLA 11: Si es joven, ingresos altos y horizonte medio, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["alto"] & self.horizonte["medio"],
                self.perfil["moderado"],
            )
        )

        # REGLA 12: Si es medio, ingresos medios, tolerancia media y horizonte medio, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["medio"]
                & self.ingresos["medio"]
                & self.tolerancia["media"]
                & self.horizonte["medio"],
                self.perfil["moderado"],
            )
        )

        # REGLA 13: Si es medio, tolerancia baja, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.tolerancia["baja"], self.perfil["conservador"]
            )
        )

        # REGLA 14: Si es joven, ingresos bajos y horizonte corto, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["bajo"] & self.horizonte["corto"],
                self.perfil["conservador"],
            )
        )

        # REGLA 15: Si es mayor, ingresos medios, tolerancia media, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["medio"] & self.tolerancia["media"],
                self.perfil["moderado"],
            )
        )

        # REGLA 16: Si es mayor, ingresos altos, tolerancia alta y horizonte largo, entonces perfil moderado
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"]
                & self.ingresos["alto"]
                & self.tolerancia["alta"]
                & self.horizonte["largo"],
                self.perfil["moderado"],
            )
        )

        # REGLA 17: Si ingresos altos, tolerancia alta, horizonte largo, entonces perfil arriesgado
        reglas.append(
            ctrl.Rule(
                self.ingresos["alto"]
                & self.tolerancia["alta"]
                & self.horizonte["largo"],
                self.perfil["arriesgado"],
            )
        )

        # REGLA 18: Si es medio, ingresos bajos, tolerancia baja, entonces perfil conservador
        reglas.append(
            ctrl.Rule(
                self.edad["medio"] & self.ingresos["bajo"] & self.tolerancia["baja"],
                self.perfil["conservador"],
            )
        )

        # REGLA 19: Si es joven, ingresos medios, tolerancia alta, entonces perfil arriesgado
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["medio"] & self.tolerancia["alta"],
                self.perfil["arriesgado"],
            )
        )

        # REGLA 20: Si horizonte corto, entonces perfil conservador
        reglas.append(ctrl.Rule(self.horizonte["corto"], self.perfil["conservador"]))

        # Regla para tolerancia alta
        reglas.append(ctrl.Rule(self.tolerancia["alta"], self.perfil["moderado"]))

        return reglas

    def evaluar(self, edad, ingresos, tolerancia, horizonte):
        """
        Evalúa el perfil de inversión con los valores dados

        Args:
            edad (int): Edad del inversor (18-90)
            ingresos (int): Ingresos mensuales (0-150,000)
            tolerancia (int): Tolerancia al riesgo (0-10)
            horizonte (int): Horizonte de inversión en años (1-40)

        Returns:
            dict: Resultado con el perfil numérico y lingüístico
        """
        # Validar entradas
        if not (18 <= edad <= 90):
            raise ValueError("La edad debe estar entre 18 y 90 años")
        if not (0 <= ingresos <= 150000):
            raise ValueError("Los ingresos deben estar entre 0 y 150,000")
        if not (0 <= tolerancia <= 10):
            raise ValueError("La tolerancia al riesgo debe estar entre 0 y 10")
        if not (1 <= horizonte <= 40):
            raise ValueError("El horizonte debe estar entre 1 y 40 años")

        try:
            # Resetear la simulación
            self.simulacion.reset()

            # Asignar valores de entrada
            self.simulacion.input["edad"] = edad
            self.simulacion.input["ingresos"] = ingresos
            self.simulacion.input["tolerancia"] = tolerancia
            self.simulacion.input["horizonte"] = horizonte

            # Calcular resultado
            self.simulacion.compute()

            # Obtener valor numérico del resultado
            valor_perfil = self.simulacion.output["perfil"]

            # Determinar perfil lingüístico según el valor numérico
            if valor_perfil <= 40:
                perfil_texto = "Conservador"
            elif valor_perfil <= 65:
                perfil_texto = "Moderado"
            else:
                perfil_texto = "Arriesgado"

            return {"valor_numerico": valor_perfil, "perfil": perfil_texto}

        except Exception as e:
            print(f"\nError en la evaluación del perfil: {e}")
            # Si hay un error, devolvemos un perfil por defecto basado en reglas simples
            if edad >= 60:
                perfil_defecto = "Conservador"
                valor_defecto = 30.0
            elif ingresos < 10000:
                perfil_defecto = "Conservador"
                valor_defecto = 25.0
            elif tolerancia >= 8:
                perfil_defecto = "Arriesgado"
                valor_defecto = 80.0
            else:
                perfil_defecto = "Moderado"
                valor_defecto = 50.0

            return {"valor_numerico": valor_defecto, "perfil": perfil_defecto}

    def visualizar_variables(self):
        """Visualiza las funciones de membresía de todas las variables"""
        try:
            # Crear una figura con 5 subplots (4 entradas + 1 salida)
            fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(nrows=5, figsize=(8, 10))

            # Graficar cada variable
            self.edad.view(sim=self.simulacion, ax=ax0)
            ax0.set_title("Edad del inversor")
            ax0.legend()

            self.ingresos.view(sim=self.simulacion, ax=ax1)
            ax1.set_title("Ingresos mensuales")
            ax1.legend()

            self.tolerancia.view(sim=self.simulacion, ax=ax2)
            ax2.set_title("Tolerancia al riesgo")
            ax2.legend()

            self.horizonte.view(sim=self.simulacion, ax=ax3)
            ax3.set_title("Horizonte de inversión (años)")
            ax3.legend()

            self.perfil.view(sim=self.simulacion, ax=ax4)
            ax4.set_title("Perfil de inversor")
            ax4.legend()

            # Ajustar layout
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar las variables: {e}")

    def visualizar_resultado(self):
        """Visualiza el resultado de la inferencia difusa"""
        try:
            self.perfil.view(sim=self.simulacion)
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar el resultado: {e}")


def ejecutar_sistema():
    """Función principal para ejecutar el sistema experto"""
    try:
        sed = SistemaExpertoDifusoInversor()

        clear_screen()
        print("\n" + "=" * 60)
        print("   SISTEMA EXPERTO DIFUSO PARA PERFILES DE INVERSIÓN")
        print("=" * 60)

        while True:
            try:
                print("\nIngrese los datos del inversor (o 'salir' para terminar):")
                entrada = input("\n- Edad (18-90 años): ")

                if entrada.lower() in ["salir", "exit", "q"]:
                    break

                edad = int(entrada)
                ingresos = int(input("- Ingresos mensuales (0-150,000): "))
                tolerancia = float(input("- Tolerancia al riesgo (0-10): "))
                horizonte = int(input("- Horizonte de inversión (1-40 años): "))

                # Evaluar perfil
                resultado = sed.evaluar(edad, ingresos, tolerancia, horizonte)

                print("\n" + "-" * 60)
                print(f"Resultado del análisis para el inversor:")
                print("-" * 60)
                print(f"Edad: {edad} años")
                print(f"Ingresos mensuales: ${ingresos}")
                print(f"Tolerancia al riesgo: {tolerancia}/10")
                print(f"Horizonte de inversión: {horizonte} años")
                print("-" * 60)
                print(f"Perfil del inversor: {resultado['perfil']}")
                print(f"Valor numérico: {resultado['valor_numerico']:.2f}/100")

                # Preguntar si desea ver las gráficas
                ver_graficas = input(
                    "\n¿Desea ver las gráficas de las variables? (s/n): "
                )
                if ver_graficas.lower() == "s":
                    sed.visualizar_variables()

                ver_resultado = input("\n¿Desea ver la gráfica del resultado? (s/n): ")
                if ver_resultado.lower() == "s":
                    sed.visualizar_resultado()

                print("\n" + "=" * 60)

            except ValueError as e:
                print(f"\nError: {e}")
            except Exception as e:
                print(f"\nError inesperado: {str(e)}")

        print("\n¡Gracias por utilizar el Sistema Experto Difuso!")

    except Exception as e:
        print(f"\nError fatal en el sistema: {str(e)}")


if __name__ == "__main__":
    ejecutar_sistema()
