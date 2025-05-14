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
        """Inicializa el sistema experto difuso con todas las variables y reglas necesarias."""
        # Definir variables de entrada (universos de discurso)
        self.edad = ctrl.Antecedent(np.arange(20, 101, 1), "edad")
        self.ingresos = ctrl.Antecedent(np.arange(0, 15001, 100), "ingresos")
        self.conocimiento = ctrl.Antecedent(np.arange(0, 11, 1), "conocimiento")
        self.tolerancia = ctrl.Antecedent(np.arange(0, 11, 1), "tolerancia")

        # Definir variables de salida
        self.potencial = ctrl.Consequent(np.arange(0, 11, 0.1), "potencial")
        self.riesgo = ctrl.Consequent(np.arange(0, 11, 0.1), "riesgo")
        self.perfil_inversor = ctrl.Consequent(
            np.arange(0, 11, 0.1), "perfil_inversor"
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
        """
        Define las funciones de membresía para todas las variables lingüísticas del sistema.
        
        Implementa funciones triangulares (trimf) y trapezoidales (trapmf) para modelar
        los conjuntos difusos correspondientes a cada término lingüístico.
        """
        # Funciones de membresía para variable EDAD
        # Formato: [a, b, c] para triangular donde b es el punto de máxima pertenencia
        # Formato: [a, b, c, d] para trapezoidal donde el intervalo [b, c] tiene pertenencia máxima
        self.edad["joven"] = fuzz.trimf(self.edad.universe, [20, 27, 35])  # Máxima pertenencia a los 27 años
        self.edad["adulto"] = fuzz.trimf(self.edad.universe, [30, 42, 55])  # Máxima pertenencia a los 42 años
        self.edad["mayor"] = fuzz.trapmf(self.edad.universe, [50, 65, 100, 100])  # Máxima pertenencia desde los 65 años

        # Funciones de membresía para variable INGRESOS (en unidades monetarias)
        self.ingresos["bajo"] = fuzz.trimf(self.ingresos.universe, [0, 1000, 2000])  # Ingresos hasta 2000
        self.ingresos["medio"] = fuzz.trimf(self.ingresos.universe, [1500, 3000, 4500])  # Ingresos entre 1500 y 4500
        self.ingresos["alto"] = fuzz.trapmf(
            self.ingresos.universe, [4000, 6000, 15000, 15000]  # Ingresos desde 4000, máximos a partir de 6000
        )

        # Funciones de membresía para variable CONOCIMIENTO (escala 0-10)
        self.conocimiento["bajo"] = fuzz.trimf(self.conocimiento.universe, [0, 2, 4])  # Conocimiento básico
        self.conocimiento["medio"] = fuzz.trapmf(
            self.conocimiento.universe, [2, 4, 5, 8]  # Conocimiento intermedio
        )
        self.conocimiento["alto"] = fuzz.trapmf(
            self.conocimiento.universe, [6, 8, 10, 10]  # Conocimiento avanzado
        )

        # Funciones de membresía para variable TOLERANCIA AL RIESGO (escala 0-10)
        self.tolerancia["baja"] = fuzz.trimf(self.tolerancia.universe, [0, 2, 4])  # Baja tolerancia al riesgo
        self.tolerancia["media"] = fuzz.trapmf(self.tolerancia.universe, [2, 4, 5, 8])  # Tolerancia moderada
        self.tolerancia["alta"] = fuzz.trapmf(self.tolerancia.universe, [6, 8, 10, 10])  # Alta tolerancia

        # Funciones de membresía para variable POTENCIAL DE INVERSIÓN (variable de salida, escala 0-10)
        self.potencial["bajo"] = fuzz.trimf(self.potencial.universe, [0, 0, 4])  # Bajo potencial (asimétrico)
        self.potencial["medio"] = fuzz.trimf(self.potencial.universe, [3, 5, 8])  # Potencial medio (simétrico)
        self.potencial["alto"] = fuzz.trimf(self.potencial.universe, [7, 10, 10])  # Alto potencial (asimétrico)

        # Funciones de membresía para variable RIESGO (variable de salida, escala 0-10)
        self.riesgo["bajo"] = fuzz.trimf(self.riesgo.universe, [0, 0, 4])  # Bajo riesgo
        self.riesgo["medio"] = fuzz.trimf(self.riesgo.universe, [3, 5, 8])  # Riesgo medio
        self.riesgo["alto"] = fuzz.trimf(self.riesgo.universe, [7, 10, 10])  # Alto riesgo

        # Funciones de membresía para variable PERFIL INVERSOR (variable final de salida, escala 0-10)
        self.perfil_inversor["conservador"] = fuzz.trapmf(
            self.perfil_inversor.universe, [0, 0, 2, 4]  # Perfil conservador: valores hasta 4
        )
        self.perfil_inversor["moderado"] = fuzz.trapmf(
            self.perfil_inversor.universe, [3, 4, 6, 7]  # Perfil moderado: valores entre 3 y 7
        )
        self.perfil_inversor["agresivo"] = fuzz.trapmf(
            self.perfil_inversor.universe, [6, 8, 10, 10]  # Perfil agresivo: valores desde 6
        )

    def definir_reglas(self):
        """
        Define el conjunto de reglas difusas para el sistema.
        
        Retorna:
            list: Lista de reglas de inferencia del sistema utilizando operadores AND (&).
        """
        reglas = []

        # -------- Bloque 1: Reglas para determinar el potencial de inversión --------
        # Basadas en la edad y el nivel de ingresos del inversor
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

        # -------- Bloque 2: Reglas para determinar el nivel de riesgo --------
        # Basadas en el conocimiento financiero y la tolerancia al riesgo
        # Regla 10: Conocimiento bajo con baja tolerancia genera riesgo medio
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

        # -------- Bloque 3: Reglas finales para determinar el perfil de inversor --------
        # Basadas en la combinación del potencial de inversión y el nivel de riesgo del inversor
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
        Evalúa el perfil de inversión con los valores dados aplicando inferencia difusa.
        
        El método realiza la validación de los parámetros de entrada, efectúa la inferencia
        difusa sobre las reglas definidas, y determina el perfil del inversor basándose
        en los valores defuzzificados de las variables de salida.

        Args:
            edad (int): Edad del inversor (20-100 años)
            ingresos (int): Ingresos mensuales (1-15,000 unidades monetarias)
            conocimiento (float): Nivel de conocimiento financiero (escala 1-10)
            tolerancia (float): Tolerancia al riesgo (escala 1-10)

        Returns:
            dict: Diccionario con los resultados de la evaluación:
                - perfil (str): Descripción lingüística del perfil ("Conservador", "Moderado", "Agresivo")
                - valor_perfil (float): Valor numérico del perfil en escala 0-10
                - potencial (float): Valor numérico del potencial de inversión en escala 0-10
                - riesgo (float): Valor numérico del nivel de riesgo en escala 0-10
                
        Raises:
            ValueError: Si algún parámetro está fuera de los rangos permitidos
        """
        # Validación de parámetros de entrada
        if not (20 <= edad <= 100):
            raise ValueError("La edad debe estar entre 20 y 100 años")
        if not (1 <= ingresos <= 15000):
            raise ValueError("Los ingresos deben estar entre 1 y 15,000")
        if not (1 <= conocimiento <= 10):
            raise ValueError("El conocimiento debe estar entre 1 y 10")
        if not (1 <= tolerancia <= 10):
            raise ValueError("La tolerancia al riesgo debe estar entre 1 y 10")

        try:
            # Preparación del sistema de inferencia
            self.simulacion.reset()

            # Fuzzificación: asignación de valores nítidos a las variables lingüísticas
            self.simulacion.input["edad"] = edad
            self.simulacion.input["ingresos"] = ingresos
            self.simulacion.input["conocimiento"] = conocimiento
            self.simulacion.input["tolerancia"] = tolerancia

            # Proceso de inferencia difusa y defuzzificación
            self.simulacion.compute()

            # Extracción de valores defuzzificados (nítidos) de las variables de salida
            valor_potencial = self.simulacion.output["potencial"]
            valor_riesgo = self.simulacion.output["riesgo"]
            valor_perfil = self.simulacion.output["perfil_inversor"]

            # Interpretación lingüística del valor numérico del perfil
            if valor_perfil <= 4.0:
                perfil_texto = "Conservador"  # Perfil orientado a la seguridad y bajo riesgo
            elif valor_perfil <= 7.0:
                perfil_texto = "Moderado"     # Perfil equilibrado entre riesgo y rentabilidad
            else:
                perfil_texto = "Agresivo"     # Perfil orientado a altos rendimientos con mayor riesgo

            return {
                "perfil": perfil_texto,
                "valor_perfil": valor_perfil,
                "potencial": valor_potencial,
                "riesgo": valor_riesgo,
            }

        except Exception as e:
            print(f"\nError en la evaluación del perfil mediante inferencia difusa: {e}")
            # Implementación de sistema de respaldo basado en reglas heurísticas simplificadas
            # para entregar resultados incluso en caso de fallo del sistema principal
            
            # Aplicación de heurísticas de clasificación basadas en factores clave
            if edad >= 60:  # Criterio de edad avanzada: predomina perfil conservador
                perfil_defecto = "Conservador"
                valor_defecto = 2.0
            elif ingresos < 1000:  # Criterio de bajos ingresos: predomina perfil conservador
                perfil_defecto = "Conservador"
                valor_defecto = 3.0
            elif tolerancia >= 8:  # Criterio de alta tolerancia al riesgo: predomina perfil agresivo
                perfil_defecto = "Agresivo"
                valor_defecto = 8.0
            else:  # Caso por defecto: perfil moderado
                perfil_defecto = "Moderado"
                valor_defecto = 5.0

            return {
                "perfil": perfil_defecto,
                "valor_perfil": valor_defecto,
                "potencial": 5.0,  # valor medio por defecto
                "riesgo": 5.0,  # valor medio por defecto
            }

    def visualizar_variables(self):
        """
        Visualiza las funciones de membresía de todas las variables lingüísticas.
        
        Esta función genera una representación gráfica de todos los conjuntos difusos
        definidos en el sistema, mostrando el grado de pertenencia para cada valor
        posible dentro del universo de discurso de cada variable.
        """
        try:
            # Configuración del lienzo de visualización
            fig, axs = plt.subplots(nrows=7, figsize=(12, 16))
            fig.suptitle('Funciones de Membresía del Sistema Experto Difuso', 
                         fontsize=16, fontweight='bold')
            
            # Visualización de variables de entrada
            self.edad.view(sim=self.simulacion, ax=axs[0])
            axs[0].set_title("Variable: Edad del Inversor (años)")
            axs[0].set_xlabel("Edad (años)")
            axs[0].set_ylabel("Grado de pertenencia")
            axs[0].legend()

            self.ingresos.view(sim=self.simulacion, ax=axs[1])
            axs[1].set_title("Variable: Ingresos Mensuales")
            axs[1].set_xlabel("Ingresos (unidades monetarias)")
            axs[1].set_ylabel("Grado de pertenencia")
            axs[1].legend()

            self.conocimiento.view(sim=self.simulacion, ax=axs[2])
            axs[2].set_title("Variable: Nivel de Conocimiento Financiero")
            axs[2].set_xlabel("Conocimiento (escala 0-10)")
            axs[2].set_ylabel("Grado de pertenencia")
            axs[2].legend()

            self.tolerancia.view(sim=self.simulacion, ax=axs[3])
            axs[3].set_title("Variable: Tolerancia al Riesgo")
            axs[3].set_xlabel("Tolerancia (escala 0-10)")
            axs[3].set_ylabel("Grado de pertenencia")
            axs[3].legend()

            self.potencial.view(sim=self.simulacion, ax=axs[4])
            axs[4].set_title("Variable Intermedia: Potencial de Inversión")
            axs[4].set_xlabel("Potencial (escala 0-10)")
            axs[4].set_ylabel("Grado de pertenencia")
            axs[4].legend()

            self.riesgo.view(sim=self.simulacion, ax=axs[5])
            axs[5].set_title("Variable Intermedia: Nivel de Riesgo")
            axs[5].set_xlabel("Nivel de riesgo (escala 0-10)")
            axs[5].set_ylabel("Grado de pertenencia")
            axs[5].legend()

            self.perfil_inversor.view(sim=self.simulacion, ax=axs[6])
            axs[6].set_title("Variable de Salida: Perfil del Inversor")
            axs[6].set_xlabel("Perfil (escala 0-10)")
            axs[6].set_ylabel("Grado de pertenencia")
            axs[6].legend()

            # Ajustar layout para optimizar la visualización
            plt.tight_layout(rect=[0, 0, 1, 0.97])  # Dejar espacio para el título general
            plt.subplots_adjust(top=0.95)  # Ajustar para el título
            
            # Agregar información adicional en la parte inferior
            plt.figtext(0.5, 0.01, 
                      "Sistema Experto Difuso para Determinación de Perfiles de Inversión",
                      ha="center", fontsize=10, fontstyle="italic")
            
            # Mostrar gráfico
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar las funciones de membresía: {e}")
            print("Tipo de error:", type(e).__name__)

    def visualizar_resultado(self):
        """
        Visualiza el resultado concreto de la inferencia difusa para los valores de entrada actuales.
        
        Esta función muestra gráficamente el proceso de defuzzificación y los resultados obtenidos
        para las tres variables de salida del sistema: potencial de inversión, nivel de riesgo
        y perfil de inversor. Los valores específicos de entrada son marcados en cada gráfico.
        """
        try:
            # Configuración del lienzo para visualización de resultados
            fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 12))
            fig.suptitle('Resultados de la Inferencia Difusa', 
                        fontsize=16, fontweight='bold')
            
            # Visualizar el proceso de defuzzificación y el valor resultante para cada salida
            self.potencial.view(sim=self.simulacion, ax=ax0)
            ax0.set_title("Potencial de Inversión Inferido")
            ax0.set_xlabel("Potencial (escala 0-10)")
            ax0.set_ylabel("Grado de activación")
            ax0.grid(True, linestyle='--', alpha=0.6)
            ax0.legend()
            
            # Anotar el valor resultante
            if hasattr(self.simulacion, 'output') and 'potencial' in self.simulacion.output:
                valor = self.simulacion.output['potencial']
                ax0.axvline(x=valor, color='red', linestyle='--', alpha=0.8)
                ax0.text(valor+0.2, 0.2, f'Valor: {valor:.2f}', 
                        bbox=dict(facecolor='white', alpha=0.8))

            self.riesgo.view(sim=self.simulacion, ax=ax1)
            ax1.set_title("Nivel de Riesgo Inferido")
            ax1.set_xlabel("Nivel de riesgo (escala 0-10)")
            ax1.set_ylabel("Grado de activación")
            ax1.grid(True, linestyle='--', alpha=0.6)
            ax1.legend()
            
            # Anotar el valor resultante
            if hasattr(self.simulacion, 'output') and 'riesgo' in self.simulacion.output:
                valor = self.simulacion.output['riesgo']
                ax1.axvline(x=valor, color='red', linestyle='--', alpha=0.8)
                ax1.text(valor+0.2, 0.2, f'Valor: {valor:.2f}', 
                        bbox=dict(facecolor='white', alpha=0.8))

            self.perfil_inversor.view(sim=self.simulacion, ax=ax2)
            ax2.set_title("Perfil de Inversor Resultante")
            ax2.set_xlabel("Perfil (escala 0-10)")
            ax2.set_ylabel("Grado de activación")
            ax2.grid(True, linestyle='--', alpha=0.6)
            ax2.legend()
            
            # Anotar el valor resultante y su interpretación lingüística
            if hasattr(self.simulacion, 'output') and 'perfil_inversor' in self.simulacion.output:
                valor = self.simulacion.output['perfil_inversor']
                perfil = "Conservador" if valor <= 4.0 else "Moderado" if valor <= 7.0 else "Agresivo"
                ax2.axvline(x=valor, color='red', linestyle='--', alpha=0.8)
                ax2.text(valor+0.2, 0.2, f'Valor: {valor:.2f}\nPerfil: {perfil}', 
                        bbox=dict(facecolor='white', alpha=0.8))

            # Optimizar visualización
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.subplots_adjust(top=0.9)
            
            # Agregar metadatos
            plt.figtext(0.5, 0.01, 
                      "© Sistema Experto basado en Lógica Difusa", 
                      ha="center", fontsize=9, fontstyle="italic")
            
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar el resultado de la inferencia difusa: {e}")
            print(f"Detalles: {type(e).__name__}")


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

        # Configurar interfaz de usuario por consola
        clear_screen()
        print("\n" + "=" * 70)
        print("   SISTEMA EXPERTO BASADO EN LÓGICA DIFUSA PARA PERFILES DE INVERSIÓN")
        print("   Implementación Avanzada en Python con Scikit-Fuzzy")
        print("=" * 70)

        while True:
            try:
                print("\n╔" + "═" * 66 + "╗")
                print("║  Ingrese los datos del inversor (o escriba 'salir' para terminar)  ║")
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
                            print("⚠️  Error: Los ingresos deben estar entre 1 y 15,000.")
                    except ValueError:
                        print("⚠️  Error: Por favor, ingrese un número entero válido.")

                # Validación de conocimiento financiero con interfaz mejorada
                while True:
                    try:
                        print("\nEscala de conocimiento financiero:")
                        print("  1-3: Conocimiento básico")
                        print("  4-7: Conocimiento intermedio")
                        print("  8-10: Conocimiento avanzado")
                        conocimiento_str = input("➤ Nivel de conocimiento financiero (1-10): ")
                        conocimiento = float(conocimiento_str)
                        if 1 <= conocimiento <= 10:
                            break
                        else:
                            print("⚠️  Error: El nivel de conocimiento debe estar entre 1 y 10.")
                    except ValueError:
                        print("⚠️  Error: Por favor, ingrese un número válido.")

                # Validación de tolerancia al riesgo con interfaz mejorada
                while True:
                    try:
                        print("\nEscala de tolerancia al riesgo:")
                        print("  1-3: Baja tolerancia (prefiere seguridad)")
                        print("  4-7: Tolerancia media (acepta cierto riesgo)")
                        print("  8-10: Alta tolerancia (asume riesgos por mayor rentabilidad)")
                        tolerancia_str = input("➤ Tolerancia al riesgo (1-10): ")
                        tolerancia = float(tolerancia_str)
                        if 1 <= tolerancia <= 10:
                            break
                        else:
                            print("⚠️  Error: La tolerancia al riesgo debe estar entre 1 y 10.")
                    except ValueError:
                        print("⚠️  Error: Por favor, ingrese un número válido.")

                # Evaluar perfil mediante el sistema de inferencia difusa
                print("\n⏳ Procesando mediante inferencia difusa...")
                resultado = sed.evaluar(edad, ingresos, conocimiento, tolerancia)

                # Presentación visual de resultados
                print("\n" + "┌" + "─" * 68 + "┐")
                print("│" + " RESULTADO DEL ANÁLISIS DE PERFIL DE INVERSIÓN ".center(68) + "│")
                print("└" + "─" * 68 + "┘")
                
                # Sección de parámetros de entrada
                print("\n🔹 PARÁMETROS DE ENTRADA:")
                print("  • Edad: " + str(edad) + " años")
                print("  • Ingresos mensuales: $" + str(ingresos))
                print("  • Conocimiento financiero: " + str(conocimiento) + "/10")
                print("  • Tolerancia al riesgo: " + str(tolerancia) + "/10")
                
                # Sección de resultados de la inferencia
                print("\n🔹 RESULTADOS DE LA INFERENCIA DIFUSA:")
                print("  • Potencial de inversión: " + f"{resultado['potencial']:.2f}/10")
                print("  • Nivel de riesgo: " + f"{resultado['riesgo']:.2f}/10")
                
                # Sección de perfil resultante
                print("\n🔹 PERFIL DE INVERSIÓN RECOMENDADO:")
                
                # Personalización del mensaje según el perfil
                if resultado['perfil'] == "Conservador":
                    print("  • Perfil: \033[94mCONSERVADOR\033[0m")  # Azul para conservador
                    print("  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10")
                    print("  • Recomendación: Inversiones de bajo riesgo como bonos,")
                    print("    fondos de renta fija y depósitos a plazo fijo.")
                elif resultado['perfil'] == "Moderado":
                    print("  • Perfil: \033[93mMODERADO\033[0m")  # Amarillo para moderado
                    print("  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10")
                    print("  • Recomendación: Cartera diversificada con una combinación")
                    print("    equilibrada entre renta fija y renta variable.")
                else:  # Agresivo
                    print("  • Perfil: \033[91mAGRESIVO\033[0m")  # Rojo para agresivo
                    print("  • Valor numérico: " + f"{resultado['valor_perfil']:.2f}/10")
                    print("  • Recomendación: Mayor proporción en renta variable,")
                    print("    acciones e inversiones de alto rendimiento.")
                
                print("\n" + "─" * 70)
                
                # Opciones de visualización con instrucciones mejoradas
                ver_graficas = input(
                    "\n¿Desea ver las gráficas de las funciones de membresía? (s/n): "
                )
                if ver_graficas.lower() in ["s", "si", "sí", "y", "yes"]:
                    print("\n⏳ Generando visualización de funciones de membresía...")
                    sed.visualizar_variables()

                ver_resultado = input("\n¿Desea ver la gráfica del proceso de inferencia? (s/n): ")
                if ver_resultado.lower() in ["s", "si", "sí", "y", "yes"]:
                    print("\n⏳ Generando visualización del proceso de inferencia...")
                    sed.visualizar_resultado()

                print("\n" + "═" * 70)

            except ValueError as e:
                print(f"\n❌ Error de validación: {e}")
                print("   Por favor, corrija los valores e intente nuevamente.")
            except Exception as e:
                print(f"\n❌ Error inesperado: {str(e)}")
                print(f"   Tipo: {type(e).__name__}")
                print("   Si el problema persiste, contacte al administrador del sistema.")

        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " ¡Gracias por utilizar el Sistema Experto de Perfiles de Inversión! ".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
        print("\nDesarrollado con tecnología de Lógica Difusa (Fuzzy Logic)")
        print("© Sistema Experto Profesional v2.0\n")

    except Exception as e:
        print(f"\n❌ ERROR FATAL EN EL SISTEMA: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        print("Detalles técnicos:")
        import traceback
        traceback.print_exc()
        print("\nEl sistema no puede continuar. Por favor, reinicie la aplicación.")


if __name__ == "__main__":
    ejecutar_sistema()
