from typing import Union
import flet as ft
from Router import Router

def get_modulos_view(router: Union[Router, str, None] = None, page: ft.Page = None):
    body = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        margin=ft.Margin(
            left=20,
            right=20,
            bottom=0,
            top=0,
        ),
        spacing=20,
        scroll=ft.ScrollMode.HIDDEN,
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Modulos", size=26, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                margin=ft.Margin(top=40)
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    image=ft.DecorationImage(
                                        src="assets/Media/MedusaAzul.jpg",
                                        fit=ft.BoxFit.COVER,
                                    ),
                                    shape=ft.BoxShape.CIRCLE,
                                    expand=True
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Modulo 1", size=18, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                                        ft.Text("Módulo de Aprendizaje 1: Vocales", size=10),
                                        ft.Text("Bienvenido al primer módulo de aprendizaje. En esta sección conocerás y practicarás " \
                                        "las vocales de la Lengua de Señas Mexicana (A, E, I, O y U). A través de ejemplos visuales y " \
                                        "actividades interactivas, podrás familiarizarte con la posición correcta de la mano para cada " \
                                        "vocal y reforzar tu aprendizaje mediante la práctica. El objetivo de este módulo es desarrollar " \
                                        "una base sólida que facilite el aprendizaje de señas más complejas en etapas posteriores.", 
                                        size=10),
                                    ],
                                    expand=True,
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        expand=True,
                        padding=20,
                        aspect_ratio=2,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: page.go('/lecciones/modulo1'),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    image=ft.DecorationImage(
                                        src="assets/Media/MedusaMorada.jpg",
                                        fit=ft.BoxFit.COVER,
                                    ),
                                    shape=ft.BoxShape.CIRCLE,
                                    expand=True
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Modulo 2", size=18, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                                        ft.Text("Descripción del módulo 2.", size=10),
                                    ],
                                    expand=True,
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        expand=True,
                        padding=20,
                        aspect_ratio=2,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: page.go('/lecciones/modulo2'),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    image=ft.DecorationImage(
                                        src="assets/Media/MedusaVerde.jpg",
                                        fit=ft.BoxFit.COVER,
                                    ),
                                    shape=ft.BoxShape.CIRCLE,
                                    expand=True
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Modulo 3", size=18, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                                        ft.Text("Descripción del módulo 3.", size=10),
                                    ],
                                    expand=True,
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        expand=True,
                        padding=20,
                        aspect_ratio=2,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: page.go('/lecciones/modulo3 '),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    image=ft.DecorationImage(
                                        src="assets/Media/MedusaAmarilla.jpg",
                                        fit=ft.BoxFit.COVER,
                                    ),
                                    shape=ft.BoxShape.CIRCLE,
                                    expand=True
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Modulo 4", size=18, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                                        ft.Text("Descripción del módulo 4.", size=10),
                                    ],
                                    expand=True,
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        expand=True,
                        padding=20,
                        aspect_ratio=2,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: page.go('/lecciones/modulo4'),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    image=ft.DecorationImage(
                                        src="assets/Media/MedusaNaranja.jpg",
                                        fit=ft.BoxFit.COVER,
                                    ),
                                    shape=ft.BoxShape.CIRCLE,
                                    expand=True
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Modulo 5", size=18, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
                                        ft.Text("Descripción del módulo 5.", size=10),
                                    ],
                                    expand=True,
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                        expand=True,
                        padding=20,
                        aspect_ratio=2,
                        border_radius=10,
                        ink=True,
                        on_click=lambda _: page.go('/lecciones/modulo5'),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
    )

    return body