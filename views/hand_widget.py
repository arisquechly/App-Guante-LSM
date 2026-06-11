from typing import List, Callable, Tuple, Optional
import flet as ft

finger_names = ["Pulgar", "Índice", "Medio", "Anular", "Meñique"]


def get_hand_widget(states: Optional[List[bool]] = None) -> Tuple[ft.Row, Callable[[int, Optional[bool]], None]]:
    if states is None:
        states = [False] * 5

    finger_containers: List[Tuple[ft.Container, ft.Container]] = []
    controls = []

    def make_finger(i: int, name: str):
        pressed = states[i]
        visual = ft.Container(
            width=36,
            height=120,
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

    row = ft.Row(controls=controls, alignment=ft.MainAxisAlignment.CENTER)

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
            row.update()
        except Exception:
            pass

    return row, toggle_fn
