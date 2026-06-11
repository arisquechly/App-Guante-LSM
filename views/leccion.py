import asyncio
import flet as ft
from views.hand_widget import get_hand_widget, aplicar_resultado
from services.parser_guante import parsear_linea
from services import bluetooth_serial as bt

# Imagen que se usa cuando una letra todavia NO tiene la suya.
PLACEHOLDER = "assets/Media/modo.jpg"

# TABLA de datos: letra -> su imagen y su titulo.
LETRAS_INFO = {
    "A": {"imagen": "assets/Media/Aa.png", "titulo": "Aa"},
    # Agrega mas letras cuando tengas sus imagenes.
}


def _info(letra):
    """Info de una letra; si no esta en la tabla, usa placeholder y titulo 'Aa'."""
    return LETRAS_INFO.get(letra, {"imagen": PLACEHOLDER, "titulo": f"{letra}{letra.lower()}"})


def construir_leccion(letras, page: ft.Page, router=None, titulo_modulo="Modulo"):
    """
    Pantalla de LECCION reutilizable para una lista de letras.
        construir_leccion(["A","E","I","O","U"], page, router, "Modulo 1: Vocales")
    """
    # Estado: dato del guante, en que letra vamos, y cuantas se lograron BIEN.
    estado = {"datos": None, "indice": 0, "completadas": 0}

    info = _info(letras[estado["indice"]])

    # Barra de progreso (avanza conforme pasas de letra).
    barra = ft.ProgressBar(
        value=0, height=10, color=ft.Colors.WHITE, bgcolor=ft.Colors.WHITE24, expand=True
    )

    # ---------- PANTALLA PRINCIPAL: caja con la letra + botones ----------
    titulo_letra = ft.Text(
        info["titulo"], size=40, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"
    )
    caja_letra = ft.Container(
        width=150, height=150, bgcolor=ft.Colors.WHITE, border_radius=10,
        alignment=ft.Alignment.CENTER, content=titulo_letra,
    )
    boton_ayuda = ft.ElevatedButton(content=ft.Text("Ayuda"), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
    boton_siguiente = ft.ElevatedButton(content=ft.Text("Siguiente"), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
    boton_salir = ft.ElevatedButton(content=ft.Text("Salir"), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
    principal = ft.Column(
        visible=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                    [
                    caja_letra,
                    boton_ayuda
                    ]
            ),
            ft.Row(
                [
                boton_salir,
                boton_siguiente
                ]
            ),
        ], 
        alignment=ft.MainAxisAlignment.CENTER
    )

    # ---------- PANTALLA DE AYUDA: imagen + widgets de la mano ----------
    imagen_letra = ft.Image(src=info["imagen"], width=150, height=150, fit=ft.BoxFit.CONTAIN)
    hand_row, mano = get_hand_widget([False] * 5)
    boton_ocultar = ft.ElevatedButton(content=ft.Text("Ocultar"), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
    ayuda = ft.Column(
        visible=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[imagen_letra, hand_row, boton_ocultar],
    )

    # ---------- PANTALLA DE RESUMEN (al terminar todas) ----------
    container_resumen = ft.Text("", size=24, weight=ft.FontWeight.BOLD, font_family="Krabby Patty")

    boton_inicio = ft.ElevatedButton(
        content=ft.Text("Inicio"),
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK
    )

    resumen = ft.Column(
        visible=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[container_resumen, boton_inicio],
    )
    # ---------- Cambiar entre pantallas ----------
    def mostrar_ayuda(e):
        principal.visible = False
        ayuda.visible = True
        page.update()

    def ocultar_ayuda(e):
        ayuda.visible = False
        principal.visible = True
        page.update()

    boton_ayuda.on_click = mostrar_ayuda
    boton_ocultar.on_click = ocultar_ayuda

    # ---------- Salir (en cualquier momento, sin resumen) ----------
    def salir(e):
        destino = "/home"
        if router is not None and hasattr(router, "get_data"):
            destino = router.get_data("previous_route") or "/home"
        page.go(destino)

    boton_salir.on_click = salir
    boton_inicio.on_click = lambda e: page.go("/modulos")

    # ---------- Mostrar resumen al terminar ----------
    def mostrar_resumen():
        principal.visible = False
        ayuda.visible = False
        resumen.visible = True
        container_resumen.value = f"Completaste {estado['completadas']} de {len(letras)} letras"
        page.update()

    # ---------- Avanzar de letra ----------
    def avanzar(completada):
        # completada=True suma a la cuenta; False solo salta.
        if completada:
            estado["completadas"] += 1

        estado["indice"] += 1

        # Si ya no hay mas letras -> resumen.
        if estado["indice"] >= len(letras):
            mostrar_resumen()
            return

        # Cargar la siguiente letra: caja, imagen, barra y mandarla al guante.
        nueva = letras[estado["indice"]]
        info_n = _info(nueva)
        titulo_letra.value = info_n["titulo"]
        imagen_letra.src = info_n["imagen"]
        barra.value = estado["indice"] / len(letras)
        bt.enviar_letra(nueva)
        page.update()

    # El boton Siguiente salta (no cuenta como completada).
    boton_siguiente.on_click = lambda e: avanzar(False)

    # ---------- Lector (hilo) guarda; loop de UI pinta ----------
    def on_linea(linea):
        print(linea)   # MODO PRUEBA: ver en la terminal lo que llega del guante
        datos = parsear_linea(linea)
        if datos:
            estado["datos"] = datos

    bt.iniciar_lectura(on_linea)

    async def actualizar_ui():
        while True:
            datos = estado["datos"]
            if datos is not None:
                estado["datos"] = None
                aplicar_resultado(mano, datos)
            await asyncio.sleep(0.05)

    page.run_task(actualizar_ui)

    # Manda la primera letra al entrar.
    bt.enviar_letra(letras[estado["indice"]])

    body = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        margin=ft.Margin(left=20, right=20, bottom=20, top=20),
        spacing=20,
        scroll=ft.ScrollMode.HIDDEN,
        controls=[
            barra,
            ft.Text(titulo_modulo, size=24, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"),
            principal,
            ayuda,
            resumen,
        ],
    )
    return body
