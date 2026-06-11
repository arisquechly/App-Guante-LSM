from typing import Callable, Any
import flet as ft
from enum import Enum
from urllib.parse import parse_qsl

class DataStrategyEnum(Enum):
    QUERY = 0
    ROUTER_DATA = 1
    CLIENT_STORAGE = 2
    STATE = 3

class Router:
    def __init__(self, data_strategy=DataStrategyEnum.QUERY):
        self.page = None
        self.data_strategy = data_strategy
        self.routes = {}
        self.data = {}
        self.current_route = None
        self.body = ft.Container(
            expand=True, 
            image=ft.DecorationImage( 
                src="assets/Media/Fondo.jpg",
                fit=ft.BoxFit.COVER,
                ),
        )

    def set_route(self, stub: str, view: Callable):
        self.routes[stub] = view
    
    def set_routes(self, route_dictionary: dict):
        """Sets multiple routes at once. Ex: {"/": IndexView }"""
        self.routes.update(route_dictionary)

    def route_change(self, route):
        next_route = route.route.split("?")[0]
        previous_route = self.current_route
        self.current_route = route.route
        query_string = route.route.split("?")[1] if "?" in route.route else ""

        self.data.clear()
        if previous_route:
            self.data['previous_route'] = previous_route

        for key, value in parse_qsl(query_string, keep_blank_values=True):
            self.data[key] = value.replace('+', ' ')

        self.body.content = self.routes[next_route](self, self.page)
        self.body.update()

        if route.route == "/bienvenido" or route.route == "/felicidades":
            self.page.bottom_appbar.visible = False
        else:
            self.page.bottom_appbar.visible = True

        self.page.update()
            

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)

    def get_query(self, key):
        return self.data.get(key)

