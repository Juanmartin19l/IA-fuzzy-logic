"""
Utilidades para el Sistema Experto Difuso de perfiles de inversión
"""

import os


def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system("cls" if os.name == "nt" else "clear")
