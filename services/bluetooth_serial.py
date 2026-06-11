"""
Comunicacion serial / Bluetooth con el ATmega32 (HC-05).

Pensado para usarse desde la app de Flet. Mantiene UNA sola conexion
abierta (singleton) para toda la app, en vez de abrir el puerto cada vez.

Deteccion de puerto SIN molestar al guante:
El HC-05 crea dos COM (entrante y saliente) y el orden cambia. NO mandamos
ningun byte de prueba (eso arrancaria el streaming de tu firmware). En vez
de eso solo ABRIMOS el puerto al conectar, y el puerto saliente correcto se
confirma con TU PRIMERA LETRA real: si cae en el puerto equivocado, la
escritura falla, se cambia al otro candidato y se reenvia esa misma letra.

Uso tipico desde la app:

    from services import bluetooth_serial as bt

    bt.conectar()                 # abre un puerto candidato (no escribe nada)
    bt.iniciar_lectura(print)     # imprime lo que mande el guante
    bt.enviar_letra("A")          # tu primera letra confirma el puerto
    ...
    bt.desconectar()              # al cerrar la app
"""

import time
import threading
import serial
import serial.tools.list_ports

# Configuracion por defecto. COM3 es el respaldo si la deteccion no halla nada.
PUERTO_DEFAULT = "COM3"
BAUDRATE = 9600

# Estado interno del modulo (la conexion viva).
_ser: serial.Serial | None = None
_hilo_lectura: threading.Thread | None = None
_leyendo = False
_callback_lectura = None          # se recuerda para no perder la lectura al cambiar de puerto
_candidatos: list[str] = []       # puertos a intentar (BT detectados + respaldo)
_puerto_actual: str | None = None  # puerto abierto ahora mismo (y ultimo que funciono)
_ultimo_dato = 0.0                 # marca de tiempo de la ultima linea recibida del guante
_puerto_confirmado = False         # True cuando el guante ya respondio por el puerto actual


# Mapeo EXPLICITO letra -> indice que espera el ATmega32.
# Tomado de assets/Documentacion/PatronLetras.txt.
# Si tu firmware usa otro orden o tiene saltos, edita SOLO este diccionario.
LETRA_A_INDICE = {
    "A": 0,  "B": 1,  "C": 2,  "D": 3,  "E": 4,  "F": 5,  "G": 6,
    "H": 7,  "I": 8,  "J": 9,  "K": 10, "L": 11, "M": 12, "N": 13,
    "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20,
    "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25,
}


def enviar_letra(letra: str) -> bool:
    """
    Manda una LETRA al guante buscando su indice en LETRA_A_INDICE.
    Pensada para usarse desde cualquier view: bt.enviar_letra("C").
    Devuelve True si se envio bien, False si la letra no existe o falla.
    """
    indice = LETRA_A_INDICE.get(letra.upper())
    if indice is None:
        print(f"[bluetooth] Letra no reconocida: {letra!r}")
        return False
    return enviar_indice(indice)


def encontrar_puertos() -> list[str]:
    """
    Devuelve TODOS los puertos que parezcan HC-05 / adaptador BT.
    (El HC-05 suele crear dos COM: entrante y saliente, y el orden cambia,
    por eso devolvemos todos y se decide cual sirve al primer envio real.)
    """
    candidatos = []
    for p in serial.tools.list_ports.comports():
        texto = (p.device + " " + p.description).lower()
        if any(k in texto for k in ("bluetooth", "hc-05", "hc05", "ch340")):
            candidatos.append(p.device)
    return candidatos


def esta_conectado() -> bool:
    return _ser is not None and _ser.is_open


def _abrir(puerto: str) -> bool:
    """Abre un puerto concreto (sin escribir nada). True si lo logro."""
    global _ser, _puerto_actual
    try:
        _ser = serial.Serial(puerto, BAUDRATE, timeout=1, write_timeout=2)
        _puerto_actual = puerto
        print(f"[bluetooth] Puerto abierto: {puerto}")
        return True
    except Exception as e:
        _ser = None
        print(f"[bluetooth] No se pudo abrir {puerto}: {e}")
        return False


def _cerrar_puerto() -> None:
    """Cierra SOLO el puerto, sin detener el hilo de lectura."""
    global _ser
    if _ser is not None:
        try:
            _ser.close()
        except Exception:
            pass
    _ser = None


def _construir_candidatos(puerto: str | None) -> list[str]:
    """Lista ordenada de puertos a intentar."""
    if puerto is not None:
        return [puerto]
    cands = encontrar_puertos()
    if PUERTO_DEFAULT not in cands:
        cands.append(PUERTO_DEFAULT)   # respaldo siempre al final
    return cands


def conectar(puerto: str | None = None) -> bool:
    """
    Abre un puerto candidato SIN mandar ningun byte (el guante sigue callado).
    Devuelve True si quedo abierto algun puerto.

      1. Si pasas un 'puerto' explicito, usa solo ese.
      2. Si no, detecta los COM Bluetooth (+ COM3 de respaldo) y abre el
         primero que se pueda abrir. El puerto saliente correcto se confirma
         con tu primera letra real en enviar_indice() (rotacion automatica).

    write_timeout=2 -> si la escritura se bloquea (puerto equivocado / link
                       caido) lanza excepcion en vez de colgarse para siempre.
    timeout=1       -> readline() no se queda atorado indefinidamente.
    """
    global _candidatos
    if esta_conectado():
        return True

    _candidatos = _construir_candidatos(puerto)

    # Intentar el ultimo puerto que funciono primero (si lo hay), luego el resto.
    orden = []
    for c in [_puerto_actual, *_candidatos]:
        if c and c not in orden:
            orden.append(c)

    for cand in orden:
        if _abrir(cand):
            return True

    print("[bluetooth] No se pudo abrir ningun puerto candidato.")
    return False


def enviar_indice(indice: int) -> bool:
    """
    Manda el byte crudo (ej. 0x05, NO el ASCII '5') al micro.

    Si el puerto actual es el equivocado (saliente/entrante intercambiados),
    la escritura falla y se prueba el OTRO candidato reenviando ESTA misma
    letra. Asi el guante solo recibe letras reales, nunca un byte de prueba.
    Devuelve True si algun puerto acepto el envio.
    """
    global _puerto_confirmado

    if not (0 <= indice <= 25):
        print(f"[bluetooth] Indice fuera de rango (0-25): {indice}")
        return False

    if not esta_conectado():
        print("[bluetooth] No conectado: intentando conectar...")
        if not conectar():
            print("[bluetooth] Sin conexion (guante apagado o puerto ocupado)")
            return False

    # CAMINO RAPIDO: si ya confirmamos el puerto, manda directo (sin esperar respuesta).
    if _puerto_confirmado and esta_conectado():
        try:
            _ser.write(bytes([indice]))
            _ser.flush()
            print(f">> Enviado indice {indice} (byte 0x{indice:02X}) por {_puerto_actual}")
            return True
        except Exception as e:
            print(f"[bluetooth] {_puerto_actual} se cayo ({e}); re-detectando puerto...")
            _cerrar_puerto()
            _puerto_confirmado = False
            # cae a la deteccion de abajo

    # DETECCION (una sola vez): el puerto SALIENTE acepta la escritura; el
    # ENTRANTE lanza SerialTimeoutException. Nos quedamos con el primero que
    # acepte y marcamos _puerto_confirmado, para NO volver a rotar (eso era lo
    # que abria/cerraba puertos sin parar y desconectaba todo).
    orden = []
    for c in [_puerto_actual, *_candidatos]:
        if c and c not in orden:
            orden.append(c)

    for cand in orden:
        if not esta_conectado() or _puerto_actual != cand:
            _cerrar_puerto()
            time.sleep(0.3)   # dar tiempo a que el COM se libere antes de abrir otro
            if not _abrir(cand):
                continue
        try:
            _ser.write(bytes([indice]))
            _ser.flush()
            _puerto_confirmado = True   # este es el saliente: nos quedamos aqui
            print(f">> Enviado indice {indice} (byte 0x{indice:02X}) por {cand} [puerto confirmado]")
            return True
        except serial.SerialTimeoutException:
            print(f"[bluetooth] {cand} es el entrante (no escribe), probando el otro...")
            _cerrar_puerto()
            continue
        except Exception as e:
            print(f"[bluetooth] Error al enviar por {cand}: {e}")
            _cerrar_puerto()
            continue

    print("[bluetooth] Ningun puerto acepto el envio (¿guante apagado?).")
    return False


def iniciar_lectura(on_dato) -> None:
    """
    Arranca un hilo que escucha respuestas del micro y se las pasa a 'on_dato'.
    Es robusto a los cambios de puerto: si el puerto se cierra un instante
    (al rotar al correcto) el hilo espera y reanuda, no muere.
    """
    global _hilo_lectura, _leyendo, _callback_lectura
    _callback_lectura = on_dato
    if _leyendo:
        return
    _leyendo = True
    _hilo_lectura = threading.Thread(target=_loop_lectura, daemon=True)
    _hilo_lectura.start()


def _loop_lectura() -> None:
    global _ultimo_dato
    while _leyendo:
        if not esta_conectado():
            time.sleep(0.1)   # puerto cerrado un momento (cambio de puerto); reintenta
            continue
        try:
            dato = _ser.readline().decode(errors="ignore").strip()
        except Exception:
            time.sleep(0.1)   # puerto se cerro mientras leiamos; reintenta sin morir
            continue
        if dato:
            _ultimo_dato = time.monotonic()   # marca: el guante respondio (sirve para confirmar puerto)
            if _callback_lectura:
                _callback_lectura(dato)


def desconectar() -> None:
    """Cierra el puerto y detiene la lectura. Llamar al cerrar la app."""
    global _leyendo
    _leyendo = False
    _cerrar_puerto()
