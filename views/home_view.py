from typing import Union
import flet as ft
from Router import Router

def get_home_view(router: Union[Router, str, None] = None, page: ft.Page = None):
    body = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        margin=ft.Margin(
            left=20,
            right=20,
            bottom=20,
            top=40,   # diferente
        ),
        spacing=20,
        controls=[
            ft.Row(
                controls=[
                    ft.SearchBar(
                        bar_hint_text="Search...",
                        expand=True,
                        aspect_ratio=8,
                        bar_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        bar_shape=ft.RoundedRectangleBorder(radius=10),
                        bar_leading=ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLACK),
                        bar_text_style=ft.TextStyle(
                            color=ft.Colors.WHITE,
                            size=14,
                        ),
                        bar_hint_text_style=ft.TextStyle(
                            color=ft.Colors.BLACK,
                            size=14,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Mundo Guante", 
                                        size=24, 
                                        weight=ft.FontWeight.BOLD, 
                                        font_family="Krabby Patty"),
                                ft.Row(
                                    controls=[
                                        ft.Image(src="assets/Media/LogoSinFondo.png", 
                                                 fit=ft.BoxFit.CONTAIN, 
                                                 width=120, 
                                                 height=120),
                                        ft.Text("Aprende Lengua de Señas Mexicana de forma práctica e interactiva. Conecta tu guante " \
                                        "inteligente y recibe retroalimentación en tiempo real mientras practicas señas, fortaleces tus " \
                                        "habilidades y avanzas a tu propio ritmo.", 
                                        size=10, 
                                        expand=True, 
                                        text_align=ft.TextAlign.LEFT),
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                ),
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        expand=True,
                        padding=5,
                        border_radius=10,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text("Modos", size=20, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
            ft.Row(
                controls=[
                    ft.Container(
                        image=ft.DecorationImage(src="assets/Media/MedusaRosaModo.png", fit=ft.BoxFit.CONTAIN),
                        bgcolor=ft.Colors.WHITE,
                        expand=True,
                        padding=20,
                        aspect_ratio=1,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: page.go('/modulos'),
                    ),
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )

    return body