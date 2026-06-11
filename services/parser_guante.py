"""
Parser de la linea de resultados que manda el guante (ATmega32).

El micro envia, cada ciclo, una linea como:
    RES FC:11110 FO:00111 PC:101 MC:1 OC:0

Donde (PULGAR a la izquierda / primero):
    FC = Flex Correcta    (5 bits, dedo 0..4)  -> color del dedo (verde si coincide)
    FO = Flex Obtenida    (5 bits, dedo 0..4)  -> mover el dedo (doblado/estirado)
    PC = Presion Correcta (3 bits, sensor 0..2)
    MC = Movimiento Correcto  (1 bit)
    OC = Orientacion Correcta (1 bit)

parsear_linea(linea) devuelve un diccionario con listas de bool, o None si la
linea no es valida (asi la app ignora mensajes como 'RX decimal:' o lineas
cortadas por Bluetooth).
"""


def _bits(texto: str) -> list[bool]:
    """Convierte '11110' -> [True, True, True, True, False]."""
    return [c == "1" for c in texto]


def parsear_linea(linea: str):
    # Guarda: si llega vacio o None, no hay nada que parsear.
    if not linea:
        return None

    linea = linea.strip()

    # 1. Solo nos interesan las lineas de resultados (empiezan con 'RES').
    if not linea.startswith("RES"):
        return None

    # 2. Separar (tokenizar) por espacios: ["RES", "FC:11110", "FO:00111", ...]
    tokens = linea.split()

    # 3. Armar un diccionario etiqueta -> valor: {"FC": "11110", "MC": "1", ...}
    campos = {}
    for token in tokens[1:]:              # saltamos el "RES"
        if ":" in token:
            etiqueta, valor = token.split(":", 1)
            campos[etiqueta] = valor

    # 4. Convertir a datos utiles. Si falta algun campo -> linea incompleta.
    try:
        resultado = {
            "flex_correcta": _bits(campos["FC"]),
            "flex_obtenida": _bits(campos["FO"]),
            "pres_correcta": _bits(campos["PC"]),
            "mov_correcto":  campos["MC"] == "1",
            "ori_correcta":  campos["OC"] == "1",
        }
    except KeyError:
        return None   # falto un campo (linea cortada por Bluetooth)

    # 5. Verificar tamanos esperados (5, 5, 3). Si no, la linea venia rota.
    if len(resultado["flex_correcta"]) != 5:
        return None
    if len(resultado["flex_obtenida"]) != 5:
        return None
    if len(resultado["pres_correcta"]) != 3:
        return None

    return resultado
