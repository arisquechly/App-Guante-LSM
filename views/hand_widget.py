from typing import List, Callable, Tuple, Optional
import flet as ft

finger_names = ["Pulgar", "Índice", "Medio", "Anular", "Meñique"]
pressed_names = ["P1", "P2", "P3"]
movement_names = ["Movimiento"]
orientation_names = ["Orientación"]

def get_hand_widget(states: Optional[List[bool]] = None) -> Tuple[ft.Column, Callable[[int, Optional[bool]], None]]:
    if states is None:
        states = [False] * 5

    finger_containers: List[Tuple[ft.Container, ft.Container]] = []
    controls = []

    def make_finger(i: int, name: str):
        pressed = states[i]
        visual = ft.Container(
            width=36,
            height=100,
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.WHITE) if not pressed else ft.Colors.GREY_300,
            alignment=ft.Alignment.TOP_CENTER,
            padding=ft.Padding(4, 4, 4, 4),
            margin=ft.Margin(top=10 if not pressed else 40),
        )

        wrapper = ft.Container(
            content=ft.Column([
                visual,
                ft.Text(name, size=12, text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.START),
            padding=5,
        )

        return wrapper, visual

    for i, name in enumerate(finger_names):
        wrapper, visual = make_finger(i, name)
        finger_containers.append((wrapper, visual))
        controls.append(wrapper)

    finger_row = ft.Row(controls=controls, alignment=ft.MainAxisAlignment.CENTER)

    # Contenedores de PRESION (3 sensores, segun pressed_names). Por ahora solo
    # visuales, en gris; mas adelante se prenderan en verde cuando coincidan.
    pressure_controls = []
    pressure_containers = []   # cuadros internos de presion (para pintarlos de verde)
    for name in pressed_names:
        cuadro = ft.Container(
            width=36,
            height=36,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_500),
        )
        pressure_containers.append(cuadro)
        pressure_controls.append(
            ft.Container(
                content=ft.Column(
                    [cuadro, ft.Text(name, size=10, text_align=ft.TextAlign.CENTER)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=4,
            )
        )
    pressure_row = ft.Row(controls=pressure_controls, alignment=ft.MainAxisAlignment.CENTER)

    movement_controls = []
    movement_containers = []   # cuadro(s) internos de movimiento
    for name in movement_names:
        cuadro = ft.Container(
            width=36,
            height=36,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_500),
        )
        movement_containers.append(cuadro)
        movement_controls.append(
            ft.Container(
                content=ft.Column(
                    [cuadro, ft.Text(name, size=10, text_align=ft.TextAlign.CENTER)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=4,
            )
        )
    movement_row = ft.Row(controls=movement_controls, alignment=ft.MainAxisAlignment.CENTER)

    orientation_controls = []
    orientation_containers = []   # cuadro(s) internos de orientacion
    for name in orientation_names:
        cuadro = ft.Container(
            width=36,
            height=36,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_500),
        )
        orientation_containers.append(cuadro)
        orientation_controls.append(
            ft.Container(
                content=ft.Column(
                    [cuadro, ft.Text(name, size=10, text_align=ft.TextAlign.CENTER)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=4,
            )
        )
    orientation_row = ft.Row(controls=orientation_controls, alignment=ft.MainAxisAlignment.CENTER)

    # Apila la presion arriba y los dedos abajo.
    panel = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    pressure_row, 
                    movement_row,
                    orientation_row,
                ]),
            finger_row],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def toggle_fn(idx: int, value: Optional[bool] = None):
        if idx < 0 or idx >= len(states):
            return
        if value is None:
            states[idx] = not states[idx]
        else:
            states[idx] = bool(value)

        wrapper, visual = finger_containers[idx]
        pressed = states[idx]
        visual.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.WHITE) if not pressed else ft.Colors.GREY_300
        visual.margin = ft.Margin(top=10 if not pressed else 40)
        try:
            finger_row.update()
        except Exception:
            pass

    # --- Poner en verde (detectado) o blanco (no detectado) ---
    def _pintar(cuadro, detectado):
        cuadro.bgcolor = ft.Colors.GREEN_400 if detectado else ft.Colors.WHITE
        try:
            panel.update()
        except Exception:
            pass

    def set_pressure(i, detectado=True):
        if 0 <= i < len(pressure_containers):
            _pintar(pressure_containers[i], detectado)

    def set_movement(detectado=True):
        _pintar(movement_containers[0], detectado)

    def set_orientation(detectado=True):
        _pintar(orientation_containers[0], detectado)

    # Se enganchan a toggle_fn para no cambiar el retorno (panel, toggle_fn).
    toggle_fn.set_pressure = set_pressure
    toggle_fn.set_movement = set_movement
    toggle_fn.set_orientation = set_orientation

    return panel, toggle_fn