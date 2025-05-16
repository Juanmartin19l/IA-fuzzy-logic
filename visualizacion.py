"""
Funcionalidades de visualización para el Sistema Experto Difuso
"""

import matplotlib.pyplot as plt


class VisualizadorSistemaExperto:
    """
    Clase para visualizar los resultados y componentes del sistema experto difuso
    """

    @staticmethod
    def visualizar_variables(sistema_experto):
        """
        Visualiza las funciones de membresía de todas las variables lingüísticas.

        Esta función genera una representación gráfica de todos los conjuntos difusos
        definidos en el sistema, mostrando el grado de pertenencia para cada valor
        posible dentro del universo de discurso de cada variable.

        Args:
            sistema_experto: Instancia de SistemaExpertoDifusoInversorFCL
        """
        try:
            # Configuración del lienzo de visualización
            fig, axs = plt.subplots(nrows=7, figsize=(12, 16))

            # GRÁFICA 1: Edad del inversor
            # Muestra las funciones de membresía para las categorías: joven, adulto y mayor
            sistema_experto.edad.view(sim=sistema_experto.simulacion, ax=axs[0])
            axs[0].set_title("Variable: Edad del Inversor (años)")
            axs[0].set_xlabel("Edad (años)")
            axs[0].set_ylabel("Grado de pertenencia")
            axs[0].legend()

            # GRÁFICA 2: Ingresos mensuales
            # Muestra las funciones de membresía para: bajos, medios y altos ingresos
            sistema_experto.ingresos.view(sim=sistema_experto.simulacion, ax=axs[1])
            axs[1].set_title("Variable: Ingresos Mensuales")
            axs[1].set_xlabel("Ingresos (unidades monetarias)")
            axs[1].set_ylabel("Grado de pertenencia")
            axs[1].legend()

            # GRÁFICA 3: Conocimiento financiero
            # Muestra las funciones de membresía para: bajo, medio y alto conocimiento
            sistema_experto.conocimiento.view(sim=sistema_experto.simulacion, ax=axs[2])
            axs[2].set_title("Variable: Nivel de Conocimiento Financiero")
            axs[2].set_xlabel("Conocimiento (escala 0-10)")
            axs[2].set_ylabel("Grado de pertenencia")
            axs[2].legend()

            # GRÁFICA 4: Tolerancia al riesgo
            # Muestra las funciones de membresía para: conservador, moderado y arriesgado
            sistema_experto.tolerancia.view(sim=sistema_experto.simulacion, ax=axs[3])
            axs[3].set_title("Variable: Tolerancia al Riesgo")
            axs[3].set_xlabel("Tolerancia (escala 0-10)")
            axs[3].set_ylabel("Grado de pertenencia")
            axs[3].legend()

            # GRÁFICA 5: Potencial de inversión (Variable intermedia)
            # Muestra el resultado de combinar edad e ingresos
            sistema_experto.potencial.view(sim=sistema_experto.simulacion, ax=axs[4])
            axs[4].set_title("Variable Intermedia: Potencial de Inversión")
            axs[4].set_ylabel("Grado de pertenencia")
            axs[4].legend()

            # GRÁFICA 6: Nivel de riesgo (Variable intermedia)
            # Muestra el resultado de combinar conocimiento y tolerancia
            sistema_experto.riesgo.view(sim=sistema_experto.simulacion, ax=axs[5])
            axs[5].set_title("Variable Intermedia: Nivel de Riesgo")
            axs[5].set_ylabel("Grado de pertenencia")
            axs[5].legend()

            # GRÁFICA 7: Perfil del inversor (Variable de salida)
            # Muestra el perfil final: conservador, moderado o agresivo
            sistema_experto.perfil_inversor.view(
                sim=sistema_experto.simulacion, ax=axs[6]
            )
            axs[6].set_title("Variable de Salida: Perfil del Inversor")
            axs[6].set_ylabel("Grado de pertenencia")
            axs[6].legend()

            # Ajustar layout para optimizar la visualización
            plt.tight_layout()

            # Mostrar gráfico
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar las funciones de membresía: {e}")
            print("Tipo de error:", type(e).__name__)
