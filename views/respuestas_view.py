from typing import Union
import asyncio
import flet as ft
from Router import Router
from views.hand_widget import get_hand_widget, aplicar_resultado
from services.parser_guante import parsear_linea
from services import bluetooth_serial as bt

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

    hand_row, mano = get_hand_widget(finger_states)

    # --- ENTREGAR (parte 2): conectar el guante REAL a este widget ---
    # El hilo lector NO puede pintar la pantalla (Flet solo actualiza desde su
    # propio loop). Por eso el lector solo PARSEA y GUARDA el dato; un loop de
    # la UI lo lee y pinta en el hilo correcto.
    estado = {"datos": None}

    def on_linea(linea):
        # Corre en el HILO LECTOR: solo parsea y guarda (NO toca la pantalla).
        print(linea)   # MODO PRUEBA: ver en la terminal lo que llega del guante
        datos = parsear_linea(linea)
        if datos:
            estado["datos"] = datos

    bt.iniciar_lectura(on_linea)

    async def actualizar_ui():
        # Corre en el LOOP de Flet (hilo principal): AQUI si se puede pintar.
        while True:
            datos = estado["datos"]
            if datos is not None:
                estado["datos"] = None        # consumir el dato
                aplicar_resultado(mano, datos)
            await asyncio.sleep(0.05)          # revisa ~20 veces por segundo

    page.run_task(actualizar_ui)

    # MODO PRUEBA (temporal): manda "A" al abrir para arrancar el streaming del micro.
    bt.enviar_letra("A")

    body.controls.append(hand_row)
    return body