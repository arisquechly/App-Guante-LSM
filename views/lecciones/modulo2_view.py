from typing import Union
import flet as ft
from Router import Router
from services import bluetooth_serial as bt

def get_modulo2_view(router: Union[Router, str, None] = None, page: ft.Page = None):
    body = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        margin=ft.Margin(
            left=20,
            right=20,
            bottom=20,
            top=40,   # diferente
        ),
        controls=[
                    ft.Container(
                        image=ft.DecorationImage(src="assets/Media/Aa.png", fit=ft.BoxFit.CONTAIN),
                        bgcolor=ft.Colors.WHITE,
                        expand=True,
                        padding=20,
                        aspect_ratio=1,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: bt.enviar_letra("A"),
                    ),
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
    )

    return body