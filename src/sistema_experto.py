"""
Sistema Experto Difuso para determinar el perfil de un inversor
Implementación en Python del archivo FCL (Fuzzy Control Language)
"""

import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz


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
        self.perfil_inversor = ctrl.Consequent(np.arange(0, 11, 0.1), "perfil_inversor")

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

        Implementa funciones gaussianas (gaussmf), sigmoidales (sigmf), triangulares (trimf)
        y trapezoidales (trapmf) para modelar los conjuntos difusos correspondientes a cada
        término lingüístico de manera más precisa.
        """
        # Funciones de membresía para variable EDAD
        # Para edad usamos gaussianas que modelan mejor la transición gradual entre etapas
        self.edad["joven"] = fuzz.gaussmf(
            self.edad.universe, 27, 5
        )  # Centro en 27 años con dispersión de 5
        self.edad["adulto"] = fuzz.gaussmf(
            self.edad.universe, 42, 7
        )  # Centro en 42 años con dispersión de 7
        self.edad["mayor"] = fuzz.sigmf(
            self.edad.universe, 60, 0.15
        )  # Transición suave desde 60 años

        # Funciones de membresía para variable INGRESOS (en unidades monetarias)
        # Para ingresos usamos combinación de gausianas para bajo/medio y sigmoidal para altos ingresos
        self.ingresos["bajo"] = fuzz.gaussmf(
            self.ingresos.universe, 1000, 600
        )  # Centro en 1000 con dispersión
        self.ingresos["medio"] = fuzz.gaussmf(
            self.ingresos.universe, 3000, 900
        )  # Centro en 3000 con dispersión
        self.ingresos["alto"] = fuzz.sigmf(
            self.ingresos.universe, 5000, 0.001
        )  # Transición gradual desde 5000

        # Funciones de membresía para variable CONOCIMIENTO (escala 0-10)
        # Usamos funciones que reflejan mejor la percepción y autoevaluación del conocimiento financiero
        self.conocimiento["bajo"] = fuzz.gaussmf(
            self.conocimiento.universe, 2, 1.2
        )  # Conocimiento básico
        self.conocimiento["medio"] = fuzz.gaussmf(
            self.conocimiento.universe, 5.5, 1.5
        )  # Conocimiento intermedio
        self.conocimiento["alto"] = fuzz.sigmf(
            self.conocimiento.universe, 7.5, 1.5
        )  # Conocimiento avanzado

        # Funciones de membresía para variable TOLERANCIA AL RIESGO (escala 0-10)
        # La tolerancia al riesgo tiene transiciones más definidas por lo que usamos sigmoidales para los extremos
        self.tolerancia["baja"] = fuzz.sigmf(
            self.tolerancia.universe, 3, -2
        )  # Baja tolerancia, curva descendente
        self.tolerancia["media"] = fuzz.gaussmf(
            self.tolerancia.universe, 5, 1.5
        )  # Tolerancia moderada
        self.tolerancia["alta"] = fuzz.sigmf(
            self.tolerancia.universe, 7, 2
        )  # Alta tolerancia, curva ascendente

        # Funciones de membresía para variable POTENCIAL DE INVERSIÓN (variable de salida, escala 0-10)
        # Para variables de salida usamos gaussianas que permiten una defuzzificación más precisa
        self.potencial["bajo"] = fuzz.gaussmf(
            self.potencial.universe, 2, 1.5
        )  # Bajo potencial
        self.potencial["medio"] = fuzz.gaussmf(
            self.potencial.universe, 5, 1.2
        )  # Potencial medio
        self.potencial["alto"] = fuzz.gaussmf(
            self.potencial.universe, 8, 1.5
        )  # Alto potencial

        # Funciones de membresía para variable RIESGO (variable de salida, escala 0-10)
        self.riesgo["bajo"] = fuzz.gaussmf(self.riesgo.universe, 2, 1.5)  # Bajo riesgo
        self.riesgo["medio"] = fuzz.gaussmf(
            self.riesgo.universe, 5, 1.2
        )  # Riesgo medio
        self.riesgo["alto"] = fuzz.gaussmf(self.riesgo.universe, 8, 1.5)  # Alto riesgo

        # Funciones de membresía para variable PERFIL INVERSOR (variable final de salida, escala 0-10)
        # Actualizamos a 5 perfiles con transiciones más suaves entre categorías
        self.perfil_inversor["muy_conservador"] = fuzz.gaussmf(
            self.perfil_inversor.universe,
            1,
            0.8,  # Perfil muy conservador: valores cercanos a 1
        )
        self.perfil_inversor["conservador"] = fuzz.gaussmf(
            self.perfil_inversor.universe,
            3,
            0.8,  # Perfil conservador: valores cercanos a 3
        )
        self.perfil_inversor["moderado"] = fuzz.gaussmf(
            self.perfil_inversor.universe,
            5,
            0.8,  # Perfil moderado: valores cercanos a 5
        )
        self.perfil_inversor["agresivo"] = fuzz.gaussmf(
            self.perfil_inversor.universe,
            7,
            0.8,  # Perfil agresivo: valores cercanos a 7
        )
        self.perfil_inversor["muy_agresivo"] = fuzz.gaussmf(
            self.perfil_inversor.universe,
            9,
            0.8,  # Perfil muy agresivo: valores cercanos a 9
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
        # Corrección de las reglas inconsistentes para un modelado más lógico del riesgo

        # RULE 10: Conocimiento bajo con baja tolerancia al riesgo -> riesgo bajo
        # (Una persona con poco conocimiento y baja tolerancia debería tener poco riesgo)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["bajo"] & self.tolerancia["baja"],
                self.riesgo["bajo"],
            )
        )

        # RULE 11: Conocimiento bajo con tolerancia media -> riesgo medio
        # (Una persona con poco conocimiento pero tolerancia media acepta riesgo moderado)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["bajo"] & self.tolerancia["media"],
                self.riesgo["medio"],
            )
        )

        # RULE 12: Conocimiento bajo con alta tolerancia -> riesgo medio
        # (Aunque tenga alta tolerancia, el bajo conocimiento limita el nivel de riesgo recomendado)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["bajo"] & self.tolerancia["alta"],
                self.riesgo["medio"],
            )
        )

        # RULE 13: Conocimiento medio con baja tolerancia -> riesgo bajo
        # (El conocimiento medio no compensa la baja tolerancia al riesgo)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["medio"] & self.tolerancia["baja"],
                self.riesgo["bajo"],
            )
        )

        # RULE 14: Conocimiento medio con tolerancia media -> riesgo medio
        # (Combinación equilibrada de conocimiento y tolerancia)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["medio"] & self.tolerancia["media"],
                self.riesgo["medio"],
            )
        )

        # RULE 15: Conocimiento medio con alta tolerancia -> riesgo alto
        # (La alta tolerancia con conocimiento medio permite asumir mayor riesgo)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["medio"] & self.tolerancia["alta"],
                self.riesgo["alto"],
            )
        )

        # RULE 16: Conocimiento alto con baja tolerancia -> riesgo medio
        # (A pesar de la baja tolerancia, el alto conocimiento permite un poco más de riesgo)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["alto"] & self.tolerancia["baja"],
                self.riesgo["medio"],
            )
        )

        # RULE 17: Conocimiento alto con tolerancia media -> riesgo alto
        # (El alto conocimiento potencia el efecto de la tolerancia media)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["alto"] & self.tolerancia["media"],
                self.riesgo["alto"],
            )
        )

        # RULE 18: Conocimiento alto con alta tolerancia -> riesgo alto
        # (Máximo conocimiento y tolerancia justifican el máximo nivel de riesgo)
        reglas.append(
            ctrl.Rule(
                self.conocimiento["alto"] & self.tolerancia["alta"],
                self.riesgo["alto"],
            )
        )

        # -------- Bloque 3: Reglas finales para determinar el perfil de inversor --------
        # Basadas en la combinación del potencial de inversión y el nivel de riesgo del inversor
        # Actualizado para 5 perfiles: muy conservador, conservador, moderado, agresivo, muy agresivo

        # Reglas para perfil muy conservador:
        # RULE 19: Potencial bajo y riesgo bajo -> muy conservador
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["bajo"],
                self.perfil_inversor["muy_conservador"],
            )
        )

        # Reglas para perfil conservador:
        # RULE 20: Potencial bajo y riesgo medio -> conservador
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["medio"],
                self.perfil_inversor["conservador"],
            )
        )
        # RULE 21: Potencial medio y riesgo bajo -> conservador
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["bajo"],
                self.perfil_inversor["conservador"],
            )
        )
        # RULE 22: Potencial bajo y riesgo alto -> conservador
        # (Potencial bajo limita el perfil a pesar del riesgo alto)
        reglas.append(
            ctrl.Rule(
                self.potencial["bajo"] & self.riesgo["alto"],
                self.perfil_inversor["conservador"],
            )
        )

        # Reglas para perfil moderado:
        # RULE 23: Potencial medio y riesgo medio -> moderado
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["medio"],
                self.perfil_inversor["moderado"],
            )
        )
        # RULE 24: Potencial alto y riesgo bajo -> moderado
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["bajo"],
                self.perfil_inversor["moderado"],
            )
        )

        # Reglas para perfil agresivo:
        # RULE 25: Potencial medio y riesgo alto -> agresivo
        reglas.append(
            ctrl.Rule(
                self.potencial["medio"] & self.riesgo["alto"],
                self.perfil_inversor["agresivo"],
            )
        )
        # RULE 26: Potencial alto y riesgo medio -> agresivo
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["medio"],
                self.perfil_inversor["agresivo"],
            )
        )

        # Reglas para perfil muy agresivo:
        # RULE 27: Potencial alto y riesgo alto -> muy agresivo
        reglas.append(
            ctrl.Rule(
                self.potencial["alto"] & self.riesgo["alto"],
                self.perfil_inversor["muy_agresivo"],
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

            # Interpretación lingüística del valor numérico del perfil (actualizada para 5 perfiles)
            if valor_perfil <= 2.0:
                perfil_texto = "Muy Conservador"  # Perfil extremadamente orientado a la seguridad y mínimo riesgo
            elif valor_perfil <= 4.0:
                perfil_texto = (
                    "Conservador"  # Perfil orientado a la seguridad y bajo riesgo
                )
            elif valor_perfil <= 6.0:
                perfil_texto = (
                    "Moderado"  # Perfil equilibrado entre riesgo y rentabilidad
                )
            elif valor_perfil <= 8.0:
                perfil_texto = (
                    "Agresivo"  # Perfil orientado a altos rendimientos con mayor riesgo
                )
            else:
                perfil_texto = "Muy Agresivo"  # Perfil extremadamente orientado a altos rendimientos con riesgo máximo

            return {
                "perfil": perfil_texto,
                "valor_perfil": valor_perfil,
                "potencial": valor_potencial,
                "riesgo": valor_riesgo,
            }

        except Exception as e:
            print(
                f"\nError en la evaluación del perfil mediante inferencia difusa: {e}"
            )
            # Implementación de sistema de respaldo basado en reglas heurísticas simplificadas
            # para entregar resultados incluso en caso de fallo del sistema principal

            # Aplicación de heurísticas de clasificación actualizadas para 5 perfiles
            if (
                edad >= 70
            ):  # Criterio de edad muy avanzada: predomina perfil muy conservador
                perfil_defecto = "Muy Conservador"
                valor_defecto = 1.5
            elif (
                edad >= 60 or ingresos < 1000
            ):  # Criterio de edad avanzada/bajos ingresos: predomina perfil conservador
                perfil_defecto = "Conservador"
                valor_defecto = 3.0
            elif (edad >= 45 and edad < 60) or (ingresos >= 1000 and ingresos < 3000):
                perfil_defecto = "Moderado"
                valor_defecto = 5.0
            elif (
                tolerancia >= 8 and conocimiento >= 7
            ):  # Alta tolerancia y conocimiento: perfil muy agresivo
                perfil_defecto = "Muy Agresivo"
                valor_defecto = 9.0
            elif (
                tolerancia >= 6 or conocimiento >= 6
            ):  # Tolerancia o conocimiento alto: perfil agresivo
                perfil_defecto = "Agresivo"
                valor_defecto = 7.0
            else:  # Caso por defecto: perfil moderado
                perfil_defecto = "Moderado"
                valor_defecto = 5.0

            return {
                "perfil": perfil_defecto,
                "valor_perfil": valor_defecto,
                "potencial": 5.0,  # valor medio por defecto
                "riesgo": 5.0,  # valor medio por defecto
            }
