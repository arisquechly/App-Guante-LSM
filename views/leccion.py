import asyncio
import time
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
    estado = {"datos": None, "indice": 0, "completadas": 0, "bloqueo_hasta": 0.0}

    info = _info(letras[estado["indice"]])

    # Barra de progreso con Don Cangrejo caminando en la punta que avanza.
    ANCHO_BARRA = 300
    TAM_CANGREJO = 45

    barra_track = ft.Container(   # la pista (fondo gris), todo el ancho
        width=ANCHO_BARRA, height=10, bgcolor=ft.Colors.WHITE24, border_radius=5, left=0, bottom=0,
    )
    barra_relleno = ft.Container(  # la parte llena (crece con el progreso)
        width=0, height=10, bgcolor=ft.Colors.WHITE, border_radius=5, left=0, bottom=0,
    )
    cangrejo = ft.Image(           # Don Cangrejo, parado en la punta
        src="assets/Media/DonCangrejoCaminando.png",
        width=TAM_CANGREJO, height=TAM_CANGREJO, left=0, bottom=0,
    )
    # Stack = apila las 3 capas: pista, relleno y el cangrejo encima.
    barra = ft.Stack(
        width=ANCHO_BARRA, height=TAM_CANGREJO,
        controls=[barra_track, barra_relleno, cangrejo],
    )

    def set_progreso(p):
        # p va de 0.0 a 1.0: ajusta el ancho del relleno y mueve al cangrejo a la punta.
        barra_relleno.width = ANCHO_BARRA * p
        x = ANCHO_BARRA * p - TAM_CANGREJO / 2          # centrar al cangrejo en la punta
        cangrejo.left = max(0, min(x, ANCHO_BARRA - TAM_CANGREJO))  # que no se salga

    # ---------- PANTALLA PRINCIPAL: caja con la letra + botones ----------
    titulo_letra = ft.Text(
        info["titulo"], size=40, weight=ft.FontWeight.BOLD, font_family="Krabby Patty"
    )
    caja_letra = ft.Container(
        width=150, height=150, bgcolor=ft.Colors.WHITE, border_radius=10,
        alignment=ft.Alignment.CENTER, content=titulo_letra,
    )
    boton_ayuda = ft.ElevatedButton(content=ft.Text("Ayuda", size=11), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, height=32)
    boton_siguiente = ft.ElevatedButton(content=ft.Text("Siguiente", size=11), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, height=32)
    boton_salir = ft.ElevatedButton(content=ft.Text("Salir", size=11), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK, height=32)
    principal = ft.Column(
        visible=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                    [
                    caja_letra,
                    boton_ayuda
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40,
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
        controls=[
            ft.Row([imagen_letra], alignment=ft.MainAxisAlignment.CENTER),
            hand_row,
            boton_ocultar,
        ],
    )

    # ---------- PANTALLA DE RESUMEN (al terminar todas) ----------
    texto_resumen = ft.Text(
        "", size=22, weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
    caja_resumen = ft.Container(
        content=texto_resumen,
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=15,
        alignment=ft.Alignment.CENTER,
    )

    boton_inicio = ft.ElevatedButton(
        content=ft.Text("Inicio"),
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK
    )

    resumen = ft.Column(
        visible=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[caja_resumen, boton_inicio],
    )

    # ---------- FELICIDADES: GIF a PANTALLA COMPLETA (tapa todo, como bienvenido) ----------
    felicidades = ft.Container(
        visible=False,
        expand=True,
        image=ft.DecorationImage(src="assets/Media/felicidades.gif", fit=ft.BoxFit.COVER),
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

    # ---------- Terminar el modulo: felicidades unos segundos, luego el resumen ----------
    async def terminar_modulo():
        # 1) Felicidades a pantalla completa (oculta tambien la barra inferior).
        principal.visible = False
        ayuda.visible = False
        felicidades.visible = True
        if page.bottom_appbar is not None:
            page.bottom_appbar.visible = False
        page.update()

        await asyncio.sleep(4)   # felicidades por 4 segundos (no bloquea la app)

        # 2) Resumen (regresa la barra inferior).
        felicidades.visible = False
        if page.bottom_appbar is not None:
            page.bottom_appbar.visible = True
        resumen.visible = True
        texto_resumen.value = f"Completaste {estado['completadas']} de {len(letras)} letras"
        page.update()

    # ---------- Avanzar de letra ----------
    def avanzar(completada):
        # completada=True suma a la cuenta; False solo salta.
        if completada:
            estado["completadas"] += 1

        estado["indice"] += 1

        # Si ya no hay mas letras -> felicidades + resumen (en esta misma vista).
        if estado["indice"] >= len(letras):
            page.run_task(terminar_modulo)
            return

        # Cargar la siguiente letra: caja, imagen, barra y mandarla al guante.
        nueva = letras[estado["indice"]]
        info_n = _info(nueva)
        titulo_letra.value = info_n["titulo"]
        imagen_letra.src = info_n["imagen"]
        set_progreso(estado["indice"] / len(letras))
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

    def gesto_correcto(datos):
        # "Todo el gesto": dedos + presion + movimiento + orientacion, todo bien.
        return (all(datos["flex_correcta"]) and all(datos["pres_correcta"])
                and datos["mov_correcto"] and datos["ori_correcta"])

    async def actualizar_ui():
        while True:
            datos = estado["datos"]
            if datos is not None:
                estado["datos"] = None
                aplicar_resultado(mano, datos)
                # Auto-avanzar si TODO coincide y ya paso el "respiro" anti-rebote.
                if gesto_correcto(datos) and time.monotonic() >= estado["bloqueo_hasta"]:
                    estado["bloqueo_hasta"] = time.monotonic() + 1.5   # respiro mientras el micro cambia de letra
                    avanzar(True)
            await asyncio.sleep(0.05)

    page.run_task(actualizar_ui)

    # Manda la primera letra al entrar.
    bt.enviar_letra(letras[estado["indice"]])

    contenido = ft.Column(
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

    # 'felicidades' va ENCIMA de todo (Stack) para tapar la pantalla completa.
    body = ft.Stack(
        expand=True,
        controls=[contenido, felicidades],
    )
    return body
