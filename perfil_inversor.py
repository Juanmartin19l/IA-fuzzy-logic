#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema Experto Difuso para determinar el perfil de un inversor
Implementación en Python del archivo FCL (Fuzzy Control Language)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os


def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system("cls" if os.name == "nt" else "clear")


class SistemaExpertoDifusoInversorFCL:
    """
    Sistema Experto Difuso para determinar el perfil de un inversor basado en:
    - Edad del inversor
    - Nivel de ingresos
    - Conocimiento financiero
    - Tolerancia al riesgo

    Implementación basada en el archivo FCL 'inv.fcl'
    """

    def __init__(self):
        """Inicializa el sistema experto difuso"""
        # Definir variables de entrada (universos de discurso)
        self.edad = ctrl.Antecedent(np.arange(18, 101, 1), "edad")
        self.ingresos = ctrl.Antecedent(np.arange(0, 15001, 100), "ingresos")
        self.conocimiento = ctrl.Antecedent(np.arange(0, 11, 1), "conocimiento")
        self.tolerancia = ctrl.Antecedent(np.arange(0, 11, 1), "tolerancia")

        # Definir variables de salida
        self.potencial = ctrl.Consequent(np.arange(0, 11, 0.1), "potencial")
        self.riesgo = ctrl.Consequent(np.arange(0, 11, 0.1), "riesgo")
        self.perfil_inversor = ctrl.Consequent(
            np.arange(0, 3.1, 0.1), "perfil_inversor"
        )

        # Definir las funciones de pertenencia para cada variable
        self.definir_funciones_membresia()

        # Definir reglas del sistema
        self.reglas = self.definir_reglas()

        # Crear sistemas de control para cada bloque de reglas
        try:
            self.sistema_ctrl = ctrl.ControlSystem(self.reglas)
            self.simulacion = ctrl.ControlSystemSimulation(self.sistema_ctrl)
        except Exception as e:
            print(f"Error al crear el sistema de control: {e}")

    def definir_funciones_membresia(self):
        """Define las funciones de membresía para todas las variables"""
        # Funciones de membresía para EDAD
        # TERM joven := (18, 1) (27, 1) (35, 0);
        self.edad["joven"] = fuzz.trimf(self.edad.universe, [18, 27, 35])
        # TERM adulto := (30, 0) (42, 1) (55, 0);
        self.edad["adulto"] = fuzz.trimf(self.edad.universe, [30, 42, 55])
        # TERM mayor := (50, 0) (65, 1) (100, 1);
        self.edad["mayor"] = fuzz.trapmf(self.edad.universe, [50, 65, 100, 100])

        # Funciones de membresía para INGRESOS
        # TERM bajo := (0, 1) (1000, 1) (2000, 0);
        self.ingresos["bajo"] = fuzz.trimf(self.ingresos.universe, [0, 1000, 2000])
        # TERM medio := (1500, 0) (3000, 1) (4500, 0);
        self.ingresos["medio"] = fuzz.trimf(self.ingresos.universe, [1500, 3000, 4500])
        # TERM alto := (4000, 0) (6000, 1) (15000, 1);
        self.ingresos["alto"] = fuzz.trapmf(
            self.ingresos.universe, [4000, 6000, 15000, 15000]
        )

        # Funciones de membresía para CONOCIMIENTO
        # TERM bajo := (0, 1) (2, 1) (4, 0);
        self.conocimiento["bajo"] = fuzz.trimf(self.conocimiento.universe, [0, 2, 4])
        # TERM medio := (2, 0) (4, 1) (5, 1) (8, 0);
        self.conocimiento["medio"] = fuzz.trapmf(
            self.conocimiento.universe, [2, 4, 5, 8]
        )
        # TERM alto := (6, 0) (8, 1) (10, 1);
        self.conocimiento["alto"] = fuzz.trapmf(
            self.conocimiento.universe, [6, 8, 10, 10]
        )

        # Funciones de membresía para TOLERANCIA
        # TERM bajo := (0, 1) (2, 1) (4, 0);
        self.tolerancia["baja"] = fuzz.trimf(self.tolerancia.universe, [0, 2, 4])
        # TERM medio := (2, 0) (4, 1) (5, 1) (8, 0);
        self.tolerancia["media"] = fuzz.trapmf(self.tolerancia.universe, [2, 4, 5, 8])
        # TERM alto := (6, 0) (8, 1) (10, 1);
        self.tolerancia["alta"] = fuzz.trapmf(self.tolerancia.universe, [6, 8, 10, 10])

        # Funciones de membresía para POTENCIAL (salida)
        # TERM bajo := (0, 1) (4, 0);
        self.potencial["bajo"] = fuzz.trimf(self.potencial.universe, [0, 0, 4])
        # TERM medio := (3, 0) (5, 1) (8, 0);
        self.potencial["medio"] = fuzz.trimf(self.potencial.universe, [3, 5, 8])
        # TERM alto := (7, 0) (10, 1);
        self.potencial["alto"] = fuzz.trimf(self.potencial.universe, [7, 10, 10])

        # Funciones de membresía para RIESGO (salida)
        # TERM bajo := (0, 1) (4, 0);
        self.riesgo["bajo"] = fuzz.trimf(self.riesgo.universe, [0, 0, 4])
        # TERM medio := (3, 0) (5, 1) (8, 0);
        self.riesgo["medio"] = fuzz.trimf(self.riesgo.universe, [3, 5, 8])
        # TERM alto := (7, 0) (10, 1);
        self.riesgo["alto"] = fuzz.trimf(self.riesgo.universe, [7, 10, 10])

        # Funciones de membresía para PERFIL INVERSOR (salida)
        # TERM conservador := (0, 1) (1, 0);
        self.perfil_inversor["conservador"] = fuzz.trimf(
            self.perfil_inversor.universe, [0, 0, 1]
        )
        # TERM moderado := (0.5, 0) (1.5, 1) (2.5, 0);
        self.perfil_inversor["moderado"] = fuzz.trimf(
            self.perfil_inversor.universe, [0.5, 1.5, 2.5]
        )
        # TERM agresivo := (2, 0) (3, 1);
        self.perfil_inversor["agresivo"] = fuzz.trimf(
            self.perfil_inversor.universe, [2, 3, 3]
        )

    def definir_reglas(self):
        """Define el conjunto de reglas difusas para el sistema"""
        reglas = []

        # -------- Reglas para potencial --------
        # RULE 1 : IF edad IS joven AND ingresos IS bajo THEN potencial IS bajo;
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["bajo"], self.potencial["bajo"]
            )
        )
        # RULE 2 : IF edad IS joven AND ingresos IS medio THEN potencial IS medio;
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["medio"], self.potencial["medio"]
            )
        )
        # RULE 3 : IF edad IS joven AND ingresos IS alto THEN potencial IS alto;
        reglas.append(
            ctrl.Rule(
                self.edad["joven"] & self.ingresos["alto"], self.potencial["alto"]
            )
        )
        # RULE 4 : IF edad IS adulto AND ingresos IS bajo THEN potencial IS bajo;
        reglas.append(
            ctrl.Rule(
                self.edad["adulto"] & self.ingresos["bajo"], self.potencial["bajo"]
            )
        )
        # RULE 5 : IF edad IS adulto AND ingresos IS medio THEN potencial IS medio;
        reglas.append(
            ctrl.Rule(
                self.edad["adulto"] & self.ingresos["medio"], self.potencial["medio"]
            )
        )
        # RULE 6 : IF edad IS adulto AND ingresos IS alto THEN potencial IS alto;
        reglas.append(
            ctrl.Rule(
                self.edad["adulto"] & self.ingresos["alto"], self.potencial["alto"]
            )
        )
        # RULE 7 : IF edad IS mayor AND ingresos IS bajo THEN potencial IS bajo;
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["bajo"], self.potencial["bajo"]
            )
        )
        # RULE 8 : IF edad IS mayor AND ingresos IS medio THEN potencial IS bajo;
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["medio"], self.potencial["bajo"]
            )
        )
        # RULE 9 : IF edad IS mayor AND ingresos IS alto THEN potencial IS medio;
        reglas.append(
            ctrl.Rule(
                self.edad["mayor"] & self.ingresos["alto"], self.potencial["medio"]
            )
        )

        # -------- Reglas para riesgo --------
        # RULE 10 : IF conocimiento IS bajo AND tolerancia IS bajo THEN riesgo IS medio;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["bajo"] & self.tolerancia["baja"],
                self.riesgo["medio"],
            )
        )
        # RULE 11 : IF conocimiento IS bajo AND tolerancia IS medio THEN riesgo IS alto;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["bajo"] & self.tolerancia["media"],
                self.riesgo["alto"],
            )
        )
        # RULE 12 : IF conocimiento IS bajo AND tolerancia IS alto THEN riesgo IS alto;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["bajo"] & self.tolerancia["alta"], self.riesgo["alto"]
            )
        )
        # RULE 13 : IF conocimiento IS medio AND tolerancia IS bajo THEN riesgo IS bajo;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["medio"] & self.tolerancia["baja"],
                self.riesgo["bajo"],
            )
        )
        # RULE 14 : IF conocimiento IS medio AND tolerancia IS medio THEN riesgo IS medio;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["medio"] & self.tolerancia["media"],
                self.riesgo["medio"],
            )
        )
        # RULE 15 : IF conocimiento IS medio AND tolerancia IS alto THEN riesgo IS alto;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["medio"] & self.tolerancia["alta"],
                self.riesgo["alto"],
            )
        )
        # RULE 16 : IF conocimiento IS alto AND tolerancia IS bajo THEN riesgo IS bajo;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["alto"] & self.tolerancia["baja"], self.riesgo["bajo"]
            )
        )
        # RULE 17 : IF conocimiento IS alto AND tolerancia IS medio THEN riesgo IS medio;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["alto"] & self.tolerancia["media"],
                self.riesgo["medio"],
            )
        )
        # RULE 18 : IF conocimiento IS alto AND tolerancia IS alto THEN riesgo IS medio;
        reglas.append(
            ctrl.Rule(
                self.conocimiento["alto"] & self.tolerancia["alta"],
                self.riesgo["medio"],
            )
        )

        # -------- Reglas finales para perfil inversor --------
        # RULE 19 : IF potencial IS bajo AND riesgo IS bajo THEN perfil_inversor IS conservador;
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["bajo"],
                self.perfil_inversor["conservador"],
            )
        )
        # RULE 20 : IF potencial IS bajo AND riesgo IS medio THEN perfil_inversor IS conservador;
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["medio"],
                self.perfil_inversor["conservador"],
            )
        )
        # RULE 21 : IF potencial IS bajo AND riesgo IS alto THEN perfil_inversor IS conservador;
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["alto"],
                self.perfil_inversor["conservador"],
            )
        )
        # RULE 22 : IF potencial IS medio AND riesgo IS bajo THEN perfil_inversor IS moderado;
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["bajo"],
                self.perfil_inversor["moderado"],
            )
        )
        # RULE 23 : IF potencial IS medio AND riesgo IS medio THEN perfil_inversor IS moderado;
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["medio"],
                self.perfil_inversor["moderado"],
            )
        )
        # RULE 24 : IF potencial IS medio AND riesgo IS alto THEN perfil_inversor IS agresivo;
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["alto"],
                self.perfil_inversor["agresivo"],
            )
        )
        # RULE 25 : IF potencial IS alto AND riesgo IS bajo THEN perfil_inversor IS agresivo;
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["bajo"],
                self.perfil_inversor["agresivo"],
            )
        )
        # RULE 26 : IF potencial IS alto AND riesgo IS medio THEN perfil_inversor IS agresivo;
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["medio"],
                self.perfil_inversor["agresivo"],
            )
        )
        # RULE 27 : IF potencial IS alto AND riesgo IS alto THEN perfil_inversor IS agresivo;
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["alto"],
                self.perfil_inversor["agresivo"],
            )
        )

        return reglas

    def evaluar(self, edad, ingresos, conocimiento, tolerancia):
        """
        Evalúa el perfil de inversión con los valores dados

        Args:
            edad (int): Edad del inversor (18-100)
            ingresos (int): Ingresos mensuales (0-15,000)
            conocimiento (int): Nivel de conocimiento financiero (0-10)
            tolerancia (int): Tolerancia al riesgo (0-10)

        Returns:
            dict: Resultado con el perfil, potencial y riesgo
        """
        # Validar entradas
        if not (18 <= edad <= 100):
            raise ValueError("La edad debe estar entre 18 y 100 años")
        if not (0 <= ingresos <= 15000):
            raise ValueError("Los ingresos deben estar entre 0 y 15,000")
        if not (0 <= conocimiento <= 10):
            raise ValueError("El conocimiento debe estar entre 0 y 10")
        if not (0 <= tolerancia <= 10):
            raise ValueError("La tolerancia al riesgo debe estar entre 0 y 10")

        try:
            # Resetear la simulación
            self.simulacion.reset()

            # Asignar valores de entrada
            self.simulacion.input["edad"] = edad
            self.simulacion.input["ingresos"] = ingresos
            self.simulacion.input["conocimiento"] = conocimiento
            self.simulacion.input["tolerancia"] = tolerancia

            # Calcular resultado
            self.simulacion.compute()

            # Obtener valores numéricos de los resultados
            valor_potencial = self.simulacion.output["potencial"]
            valor_riesgo = self.simulacion.output["riesgo"]
            valor_perfil = self.simulacion.output["perfil_inversor"]

            # Determinar perfil lingüístico según el valor numérico
            if valor_perfil <= 1.0:
                perfil_texto = "Conservador"
            elif valor_perfil <= 2.0:
                perfil_texto = "Moderado"
            else:
                perfil_texto = "Agresivo"

            return {
                "perfil": perfil_texto,
                "valor_perfil": valor_perfil,
                "potencial": valor_potencial,
                "riesgo": valor_riesgo,
            }

        except Exception as e:
            print(f"\nError en la evaluación del perfil: {e}")
            # Si hay un error, devolvemos un perfil por defecto basado en reglas simples
            if edad >= 60:
                perfil_defecto = "Conservador"
                valor_defecto = 0.5
            elif ingresos < 1000:
                perfil_defecto = "Conservador"
                valor_defecto = 0.7
            elif tolerancia >= 8:
                perfil_defecto = "Agresivo"
                valor_defecto = 2.5
            else:
                perfil_defecto = "Moderado"
                valor_defecto = 1.5

            return {
                "perfil": perfil_defecto,
                "valor_perfil": valor_defecto,
                "potencial": 5.0,  # valor medio por defecto
                "riesgo": 5.0,  # valor medio por defecto
            }

    def visualizar_variables(self):
        """Visualiza las funciones de membresía de todas las variables"""
        try:
            # Crear una figura con 7 subplots (4 entradas + 3 salidas)
            fig, axs = plt.subplots(nrows=7, figsize=(10, 14))

            # Graficar cada variable
            self.edad.view(sim=self.simulacion, ax=axs[0])
            axs[0].set_title("Edad del inversor")
            axs[0].legend()

            self.ingresos.view(sim=self.simulacion, ax=axs[1])
            axs[1].set_title("Ingresos mensuales")
            axs[1].legend()

            self.conocimiento.view(sim=self.simulacion, ax=axs[2])
            axs[2].set_title("Nivel de conocimiento financiero")
            axs[2].legend()

            self.tolerancia.view(sim=self.simulacion, ax=axs[3])
            axs[3].set_title("Tolerancia al riesgo")
            axs[3].legend()

            self.potencial.view(sim=self.simulacion, ax=axs[4])
            axs[4].set_title("Potencial de inversión")
            axs[4].legend()

            self.riesgo.view(sim=self.simulacion, ax=axs[5])
            axs[5].set_title("Nivel de riesgo")
            axs[5].legend()

            self.perfil_inversor.view(sim=self.simulacion, ax=axs[6])
            axs[6].set_title("Perfil de inversor")
            axs[6].legend()

            # Ajustar layout
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar las variables: {e}")

    def visualizar_resultado(self):
        """Visualiza el resultado de la inferencia difusa"""
        try:
            # Crear una figura con 3 subplots (3 salidas)
            fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))

            # Graficar cada salida
            self.potencial.view(sim=self.simulacion, ax=ax0)
            ax0.set_title("Potencial de inversión resultante")
            ax0.legend()

            self.riesgo.view(sim=self.simulacion, ax=ax1)
            ax1.set_title("Nivel de riesgo resultante")
            ax1.legend()

            self.perfil_inversor.view(sim=self.simulacion, ax=ax2)
            ax2.set_title("Perfil de inversor resultante")
            ax2.legend()

            # Ajustar layout
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar el resultado: {e}")


def ejecutar_sistema():
    """Función principal para ejecutar el sistema experto"""
    try:
        sed = SistemaExpertoDifusoInversorFCL()

        clear_screen()
        print("\n" + "=" * 60)
        print("   SISTEMA EXPERTO DIFUSO PARA PERFILES DE INVERSIÓN")
        print("   Implementación Python del archivo FCL")
        print("=" * 60)

        while True:
            try:
                print("\nIngrese los datos del inversor (o 'salir' para terminar):")
                entrada = input("\n- Edad (18-100 años): ")

                if entrada.lower() in ["salir", "exit", "q"]:
                    break

                edad = int(entrada)
                ingresos = int(input("- Ingresos mensuales (0-15,000): "))
                conocimiento = float(input("- Conocimiento financiero (0-10): "))
                tolerancia = float(input("- Tolerancia al riesgo (0-10): "))

                # Evaluar perfil
                resultado = sed.evaluar(edad, ingresos, conocimiento, tolerancia)

                print("\n" + "-" * 60)
                print(f"Resultado del análisis para el inversor:")
                print("-" * 60)
                print(f"Edad: {edad} años")
                print(f"Ingresos mensuales: ${ingresos}")
                print(f"Conocimiento financiero: {conocimiento}/10")
                print(f"Tolerancia al riesgo: {tolerancia}/10")
                print("-" * 60)
                print(f"Potencial de inversión: {resultado['potencial']:.2f}/10")
                print(f"Nivel de riesgo: {resultado['riesgo']:.2f}/10")
                print(f"Perfil del inversor: {resultado['perfil']}")
                print(f"Valor numérico: {resultado['valor_perfil']:.2f}/3")

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
