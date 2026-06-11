from typing import Union
import flet as ft
from Router import Router

def get_modulo1_view(router: Union[Router, str, None] = None, page: ft.Page = None):
    progress_value = 0

    imagenes = ft.Column(
        expand=True,
        visible=False,
        controls=[
            ft.Image(
                src="assets/Media/Aa.png",
                fit=ft.BoxFit.CONTAIN,
                width=150,
                height=100,
                expand=True,
            ),
            ft.Row(
                expand=True,
                controls=[
                    ft.Image(
                        src="assets/Media/modo.jpg",
                        fit=ft.BoxFit.CONTAIN,
                        width=150,
                        height=150,
                        expand=True,
                    ),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Image(
                                        src="assets/Media/modo.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        width=150,
                                        height=150,
                                        expand=True,
                                    ),
                                    ft.Image(
                                        src="assets/Media/modo.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        width=150,
                                        height=150,
                                        expand=True,
                                    ),
                                    ft.Image(
                                        src="assets/Media/modo.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        width=150,
                                        height=150,
                                        expand=True,
                                    ),
                                    ft.Image(
                                        src="assets/Media/modo.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        width=150,
                                        height=150,
                                        expand=True,
                                    ),
                                     ft.Image(
                                        src="assets/Media/modo.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        width=150,
                                        height=150,
                                        expand=True,
                                    ),
                                ],
                            ),   
                            ft.Row(
                                    controls=[
                                        ft.Image(
                                            src="assets/Media/modo.jpg",
                                            fit=ft.BoxFit.CONTAIN,
                                            width=150,
                                            height=150,
                                            expand=True,
                                        ),
                                        ft.Image(
                                            src="assets/Media/modo.jpg",
                                            fit=ft.BoxFit.CONTAIN,
                                            width=150,
                                            height=150,
                                            expand=True,
                                        ),
                                        ft.Image(
                                            src="assets/Media/modo.jpg",
                                            fit=ft.BoxFit.CONTAIN,
                                            width=150,
                                            height=150,
                                            expand=True,
                                        ),
                                        ft.Image(
                                            src="assets/Media/modo.jpg",
                                            fit=ft.BoxFit.CONTAIN,
                                            width=150,
                                            height=150,
                                            expand=True,
                                        ),
                                    ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
    boton_ayuda = ft.ElevatedButton(
        content=ft.Text("Ayuda"),
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
    )

    def toggle(e):
        
        page.go('/respuestas?imagen=Media/Aa.png')

    boton_ayuda.on_click = toggle
    
    body = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        margin=ft.Margin(
            left=20,
            right=20,
            bottom=0,
            top=20,
        ),
        spacing=20,
        scroll=ft.ScrollMode.HIDDEN,
        controls=[
            ft.ProgressBar(
                value=progress_value,
                height=10,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.WHITE24,
                expand=True,
            ),
            ft.Text(
                "Modulo 1: Vocales",
                size=24,
                weight=ft.FontWeight.BOLD,
                font_family="Krabby Patty",
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        margin=10,
                        padding=10,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=ft.Colors.WHITE,
                        width=150,
                        height=150,
                        border_radius=10,
                        content=ft.Text(
                            "Aa",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            font_family="Krabby Patty",
                        ),
                        expand=True,
                    ),
                    imagenes,
                ],
            ),
            boton_ayuda,
        ],
    )

    return body