import asyncio
import flet as ft
from routes import router
from user_controls.app_bar import NavBar

#Constants:
#Delay_page:
DELAY_BIENVENIDO = 7
DELAY_FELICIDADES = 4
#Variables: 
#Delay_page:
delay_page = 0; 

async def delay_page(page: ft.Page, delay: int, route: str):
    await asyncio.sleep(delay)
    page.go(route)

def main(page: ft.Page):
    router.page = page

    page.fonts = {
        "Quicksand": "assets/Fuentes/Quicksand-Bold.ttf",
        "Krabby Patty": "assets/Fuentes/Krabby Patty.ttf"
    }
    page.theme = ft.Theme(
        font_family="Quicksand"
    )

    page.window.width = 1080 / 3
    page.window.height = 2340 / 3
    page.window.resizable = False

    page.padding = 0
    page.update()

    page.on_route_change = router.route_change
    router.page = page
    page.add(
        router.body
    )
    
    page.go('/bienvenido')
    #page.go('/respuestas?imagen=assets/Media/Aa.png')

    page.bottom_appbar = NavBar(page)

    asyncio.create_task(delay_page(page, DELAY_BIENVENIDO, '/home'))

ft.run(
    main,
    assets_dir="assets",
)