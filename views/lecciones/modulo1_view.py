from typing import Union
import flet as ft
from Router import Router
from views.leccion import construir_leccion


def get_modulo1_view(router: Union[Router, str, None] = None, page: ft.Page = None):
    # El modulo solo dice CUALES letras y SU titulo; la interfaz la pone construir_leccion.
    return construir_leccion(["A", "E", "I", "O", "U"], page, router, "Modulo 1: Vocales")
