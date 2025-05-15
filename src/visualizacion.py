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
            fig.suptitle(
                "Funciones de Membresía del Sistema Experto Difuso",
                fontsize=16,
                fontweight="bold",
            )

            # Visualización de variables de entrada
            sistema_experto.edad.view(sim=sistema_experto.simulacion, ax=axs[0])
            axs[0].set_title("Variable: Edad del Inversor (años)")
            axs[0].set_xlabel("Edad (años)")
            axs[0].set_ylabel("Grado de pertenencia")
            axs[0].legend()

            sistema_experto.ingresos.view(sim=sistema_experto.simulacion, ax=axs[1])
            axs[1].set_title("Variable: Ingresos Mensuales")
            axs[1].set_xlabel("Ingresos (unidades monetarias)")
            axs[1].set_ylabel("Grado de pertenencia")
            axs[1].legend()

            sistema_experto.conocimiento.view(sim=sistema_experto.simulacion, ax=axs[2])
            axs[2].set_title("Variable: Nivel de Conocimiento Financiero")
            axs[2].set_xlabel("Conocimiento (escala 0-10)")
            axs[2].set_ylabel("Grado de pertenencia")
            axs[2].legend()

            sistema_experto.tolerancia.view(sim=sistema_experto.simulacion, ax=axs[3])
            axs[3].set_title("Variable: Tolerancia al Riesgo")
            axs[3].set_xlabel("Tolerancia (escala 0-10)")
            axs[3].set_ylabel("Grado de pertenencia")
            axs[3].legend()

            sistema_experto.potencial.view(sim=sistema_experto.simulacion, ax=axs[4])
            axs[4].set_title("Variable Intermedia: Potencial de Inversión")
            axs[4].set_ylabel("Grado de pertenencia")
            axs[4].legend()

            sistema_experto.riesgo.view(sim=sistema_experto.simulacion, ax=axs[5])
            axs[5].set_title("Variable Intermedia: Nivel de Riesgo")
            axs[5].set_ylabel("Grado de pertenencia")
            axs[5].legend()

            sistema_experto.perfil_inversor.view(
                sim=sistema_experto.simulacion, ax=axs[6]
            )
            axs[6].set_title("Variable de Salida: Perfil del Inversor")
            axs[6].set_ylabel("Grado de pertenencia")
            axs[6].legend()

            # Ajustar layout para optimizar la visualización
            plt.tight_layout(
                rect=[0, 0, 1, 0.97]
            )  # Dejar espacio para el título general
            plt.subplots_adjust(top=0.95)  # Ajustar para el título

            # Agregar información adicional en la parte inferior
            plt.figtext(
                0.5,
                0.01,
                "Sistema Experto Difuso para Determinación de Perfiles de Inversión",
                ha="center",
                fontsize=10,
                fontstyle="italic",
            )

            # Mostrar gráfico
            plt.show()
        except Exception as e:
            print(f"\nError al visualizar las funciones de membresía: {e}")
            print("Tipo de error:", type(e).__name__)

    @staticmethod
    def visualizar_resultado(sistema_experto):
        """
        Visualiza el resultado concreto de la inferencia difusa para los valores de entrada actuales.

        Esta función muestra gráficamente el proceso de defuzzificación y los resultados obtenidos
        para las tres variables de salida del sistema: potencial de inversión, nivel de riesgo
        y perfil de inversor. Los valores específicos de entrada son marcados en cada gráfico.

        Args:
            sistema_experto: Instancia de SistemaExpertoDifusoInversorFCL
        """
        try:
            # Configuración del lienzo para visualización de resultados
            fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 12))
            fig.suptitle(
                "Resultados de la Inferencia Difusa", fontsize=16, fontweight="bold"
            )

            # Visualizar el proceso de defuzzificación y el valor resultante para cada salida
            sistema_experto.potencial.view(sim=sistema_experto.simulacion, ax=ax0)
            ax0.set_title("Potencial de Inversión Inferido")
            ax0.set_ylabel("Grado de activación")
            ax0.grid(True, linestyle="--", alpha=0.6)
            ax0.legend()

            # Anotar el valor resultante
            if (
                hasattr(sistema_experto.simulacion, "output")
                and "potencial" in sistema_experto.simulacion.output
            ):
                valor = sistema_experto.simulacion.output["potencial"]
                ax0.axvline(x=valor, color="red", linestyle="--", alpha=0.8)
                ax0.text(
                    valor + 0.2,
                    0.2,
                    f"Valor: {valor:.2f}",
                    bbox=dict(facecolor="white", alpha=0.8),
                )

            sistema_experto.riesgo.view(sim=sistema_experto.simulacion, ax=ax1)
            ax1.set_title("Nivel de Riesgo Inferido")
            ax1.set_ylabel("Grado de activación")
            ax1.grid(True, linestyle="--", alpha=0.6)
            ax1.legend()

            # Anotar el valor resultante
            if (
                hasattr(sistema_experto.simulacion, "output")
                and "riesgo" in sistema_experto.simulacion.output
            ):
                valor = sistema_experto.simulacion.output["riesgo"]
                ax1.axvline(x=valor, color="red", linestyle="--", alpha=0.8)
                ax1.text(
                    valor + 0.2,
                    0.2,
                    f"Valor: {valor:.2f}",
                    bbox=dict(facecolor="white", alpha=0.8),
                )

            sistema_experto.perfil_inversor.view(sim=sistema_experto.simulacion, ax=ax2)
            ax2.set_title("Perfil de Inversor Resultante")
            ax2.set_ylabel("Grado de activación")
            ax2.grid(True, linestyle="--", alpha=0.6)
            ax2.legend()

            # Anotar el valor resultante
            if (
                hasattr(sistema_experto.simulacion, "output")
                and "perfil_inversor" in sistema_experto.simulacion.output
            ):
                valor = sistema_experto.simulacion.output["perfil_inversor"]

                # Determinación del perfil según el valor numérico
                if valor <= 3.33:
                    perfil = "Conservador"
                    color = "blue"
                elif valor <= 6.66:
                    perfil = "Moderado"
                    color = "green"
                else:
                    perfil = "Agresivo"
                    color = "red"

                ax2.axvline(x=valor, color=color, linestyle="--", alpha=0.8)
                ax2.text(
                    valor + 0.2,
                    0.2,
                    f"Valor: {valor:.2f}\nPerfil: {perfil}",
                    bbox=dict(facecolor="white", alpha=0.8, boxstyle="round,pad=0.5"),
                    color=color,
                    fontweight="bold",
                )

            # Optimizar visualización
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.subplots_adjust(top=0.9)

            # Agregar metadatos
            plt.figtext(
                0.5,
                0.01,
                "© Sistema Experto basado en Lógica Difusa",
                ha="center",
                fontsize=9,
                fontstyle="italic",
            )

            plt.show()
        except Exception as e:
            print(f"\nError al visualizar el resultado de la inferencia difusa: {e}")
            print(f"Detalles: {type(e).__name__}")
