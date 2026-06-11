from Router import Router, DataStrategyEnum
from views.bienvenido_view import get_bienvenido_view
from views.felicidades_view import get_felicidades_view 
from views.home_view import get_home_view
from views.modulos_view import get_modulos_view
from views.respuestas_view import get_respuestas_view
from views.lecciones.modulo1_view import get_modulo1_view
from views.lecciones.modulo2_view import get_modulo2_view

router = Router(DataStrategyEnum.QUERY)

router.routes = {
    "/bienvenido":  get_bienvenido_view,
    "/felicidades": get_felicidades_view,
    "/home": get_home_view,
    "/modulos": get_modulos_view,
    "/respuestas": get_respuestas_view,
    "/lecciones/modulo1": get_modulo1_view,
    "/lecciones/modulo2": get_modulo2_view,
}