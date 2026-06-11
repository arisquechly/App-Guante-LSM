from typing import Union
import flet as ft
from Router import Router
from views.hand_widget import get_hand_widget

def get_respuestas_view(router: Union[Router, str, None] = None, page: ft.Page = None):
    imagen = "assets/Media/Aa.png"

    if isinstance(router, Router):
        imagen = router.get_query("imagen") or imagen

    body = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        margin=ft.Margin(
            left=20,
            right=20,
            bottom=20,
            top=40,
        ),
        spacing=20,
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ARROW_BACK, size=30),
                        ft.Text("Regresar", size=18, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                    ]
                ),
                ink=True,
                on_click=(lambda e: page.go(
                    (router.get_query("back") if hasattr(router, 'get_query') else None)
                    or (router.get_data("previous_route") if hasattr(router, 'get_data') else None)
                    or "/home"
                )),
            ),
            ft.Text(
                "Respuestas",
                size=26,
                weight=ft.FontWeight.BOLD,
                font_family="Krabby Patty",
            ),
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Image(
                    src=imagen,
                    fit=ft.BoxFit.CONTAIN,
                    expand=True,
                ),
            ),
        ],
    )

    finger_states = [False, False, False, False, False]

    hand_row, toggle_finger = get_hand_widget(finger_states)

    toggle_finger(4, True)  # Example: set thumb as pressed

    body.controls.append(hand_row)
    return body