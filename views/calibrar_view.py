import asyncio
import flet as ft
from views.hand_widget import get_hand_widget
from services import bluetooth_serial as bt

VERDE = ft.Colors.GREEN_400
GRIS = ft.Colors.GREY_300


def get_calibrar_view(router=None, page: ft.Page = None):
    # --- Textos de la pantalla ---
    titulo = ft.Text("Calibracion", size=28, weight=ft.FontWeight.BOLD, font_family="Krabby Patty")
    estado_txt = ft.Text("Presiona el botón del guante para empezar", size=20, weight=ft.FontWeight.BOLD)
    sub_txt = ft.Text("", size=13, color=ft.Colors.WHITE)   # texto chico gris

    # --- La mano (reusamos el hand_widget) ---
    hand_row, mano = get_hand_widget([False] * 5, solo_dedos=True)
    for i in range(5):
        mano.set_finger_color(i, False, GRIS, refrescar_ahora=False)   # arrancan en gris

    # --- Lector (hilo) guarda la linea; loop de UI la procesa ---
    estado = {"linea": None}

    def on_linea(linea):
        estado["linea"] = linea

    bt.iniciar_lectura(on_linea)

    def procesar(linea):
        t = linea.strip().upper()

        if t.startswith("CALIBRANDO"):
            for i in range(5):
                mano.set_finger_color(i, False, GRIS, refrescar_ahora=False)
            estado_txt.value = "Calibrando..."
            sub_txt.value = "Sigue las instrucciones del guante"

        elif t.startswith("DEDO"):
            # Formato: "DEDO N ABIERTO" / "DEDO N CERRADO"
            partes = t.split()
            try:
                n = int(partes[1])
            except (IndexError, ValueError):
                return
            modo = partes[2] if len(partes) > 2 else ""
            # El firmware calibra de MEÑIQUE a PULGAR: DEDO 1 = indice 4, DEDO 5 = indice 0.
            idx = 5 - n

            # Los dedos ya calibrados son los de indice MAYOR -> gris.
            for j in range(idx + 1, 5):
                mano.set_finger_color(j, False, GRIS, refrescar_ahora=False)

            if modo == "ABIERTO":
                mano.set_finger_color(idx, False, VERDE, refrescar_ahora=False)   # verde + arriba
                estado_txt.value = f"Dedo {n} — Abierto"
            elif modo == "CERRADO":
                mano.set_finger_color(idx, True, VERDE, refrescar_ahora=False)    # verde + abajo
                estado_txt.value = f"Dedo {n} — Cerrado"
            sub_txt.value = "Recolectando datos..."

        elif t.startswith("FLEX OK") or t.startswith("CALIBRACION OK"):
            for i in range(5):
                mano.set_finger_color(i, False, GRIS, refrescar_ahora=False)
            estado_txt.value = "¡Calibración completa!"
            sub_txt.value = ""

        page.update()   # una sola actualizacion de toda la pantalla

    async def actualizar_ui():
        while True:
            linea = estado["linea"]
            if linea is not None:
                estado["linea"] = None
                procesar(linea)
            await asyncio.sleep(0.05)

    page.run_task(actualizar_ui)

    def salir(e):
        page.go("/home")

    body = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        margin=ft.Margin(left=20, right=20, top=30, bottom=20),
        spacing=15,
        controls=[
            titulo,
            estado_txt,
            sub_txt,
            hand_row,
            ft.ElevatedButton(
                content=ft.Text("Salir"), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
                on_click=salir,
            ),
        ],
    )
    return body
