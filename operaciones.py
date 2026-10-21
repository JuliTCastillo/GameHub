import re
import random
import json


def normalizar_string(string):
    """Convierte un texto a mayúsculas y elimina todos los espacios."""
    return re.sub(r"\s+", "", string.upper())


# ============================================================
# LOGIN
# ============================================================

def cargar_usuario(nombre_archivo):
    """Lee usuario y contraseña desde la primera línea de un archivo CSV."""
    with open(nombre_archivo, "r", encoding="utf-8") as arch:
        usuario_correcto, contrasena_correcta = arch.readline().strip().split(",")
    return usuario_correcto, contrasena_correcta


def login_valido(nombre_archivo):
    """Solicita credenciales por consola y valida que coincidan con el archivo."""
    usuario = input("Ingrese el usario: ").strip()
    contrasena = input("Ingrese la contraseña: ").strip()
    usuario_correcto, contrasena_correcta = cargar_usuario(nombre_archivo)
    return usuario_correcto == usuario and contrasena_correcta == contrasena


# ============================================================
# CONFIGURACION DE TORNEO
# ============================================================

def cargar_configuracion(nombre_archivo):
    """Carga la configuración desde un archivo JSON o devuelve None si falla."""
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{nombre_archivo}'.")
        return None

    except json.JSONDecodeError:
        print(f"Error: '{nombre_archivo}' no tiene un formato JSON válido.")
        return None

    return config


def validar_configuracion(config):
    """Verifica la estructura, tipos de datos y reglas de la configuración."""
    if not isinstance(config, dict):
        print("La configuración debe ser un objeto JSON { ... }.")
        return False

    valida = True

    # 1) Secciones principales obligatorias
    secciones = ("torneo", "reglas", "regiones_validas", "mapas")
    for seccion in secciones:
        if seccion not in config:
            print(f"Falta la sección '{seccion}' en la configuración.")
            valida = False

    if not valida:
        return valida

    # 2) Claves requeridas dentro de 'torneo' y 'reglas'
    claves_requeridas = {
        "torneo": ("nombre", "juego", "cantidad_equipos"),
        "reglas": ("puntos_para_ganar", "diferencia_minima", "permite_overtime"),
    }

    for seccion in claves_requeridas:
        if not isinstance(config[seccion], dict):
            print(f"La sección '{seccion}' debe ser un objeto JSON {{ ... }}.")
            valida = False
        else:
            for clave in claves_requeridas[seccion]:
                if clave not in config[seccion]:
                    print(f"Falta '{clave}' dentro de '{seccion}'.")
                    valida = False

    if not valida:
        return valida

    torneo = config["torneo"]
    reglas = config["reglas"]

    # 3) Tipos de datos de los valores
    cantidad = torneo["cantidad_equipos"]
    puntos = reglas["puntos_para_ganar"]
    dif = reglas["diferencia_minima"]

    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        print("'cantidad_equipos' debe ser un número entero.")
        valida = False

    if not isinstance(puntos, int) or isinstance(puntos, bool):
        print("'puntos_para_ganar' debe ser un número entero.")
        valida = False

    if not isinstance(dif, int) or isinstance(dif, bool):
        print("'diferencia_minima' debe ser un número entero.")
        valida = False

    if not isinstance(reglas["permite_overtime"], bool):
        print("'permite_overtime' debe ser true o false.")
        valida = False

    if not isinstance(torneo["nombre"], str) or torneo["nombre"].strip() == "":
        print("'nombre' debe ser un texto no vacío.")
        valida = False

    if not isinstance(torneo["juego"], str) or torneo["juego"].strip() == "":
        print("'juego' debe ser un texto no vacío.")
        valida = False

    if not valida:
        return valida

    # 4) Rangos y coherencia numérica
    if cantidad < 2:
        print("Tiene que haber al menos 2 equipos.")
        valida = False

    if cantidad % 2 != 0:
        print("La cantidad de equipos debe ser par.")
        valida = False

    if puntos < 1:
        print("Los puntos para ganar deben ser al menos 1.")
        valida = False

    if dif < 1:
        print("La diferencia mínima debe ser al menos 1.")
        valida = False

    if dif > puntos:
        print("La diferencia mínima no puede ser mayor a los puntos para ganar.")
        valida = False

    # 5) Lista de mapas no vacía
    if not isinstance(config["mapas"], list) or len(config["mapas"]) == 0:
        print("'mapas' debe ser una lista con al menos un mapa.")
        valida = False

    # 6) Lista de regiones no vacía y normalizada
    regiones = config["regiones_validas"]

    if not isinstance(regiones, list) or len(regiones) == 0:
        print("'regiones_validas' debe ser una lista con al menos una región.")
        valida = False
    else:
        for region in regiones:
            if not isinstance(region, str) or region != normalizar_string(region):
                print(f"La región {region!r} debe estar en MAYÚSCULAS y sin espacios.")
                valida = False

    return valida


# ============================================================
# CARGA DE REGISTROS
# ============================================================

def cargar_datos(nombre_archivo, valor_por_defecto):
    """Lee un archivo JSON; devuelve valor_por_defecto si no existe o None si está dañado."""
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as arch:
            return json.load(arch)

    except FileNotFoundError:
        return valor_por_defecto

    except json.JSONDecodeError:
        print(f"Error: '{nombre_archivo}' está dañado o no es un JSON válido.")
        return None


def guardar_datos(nombre_archivo, datos):
    """Guarda una estructura de datos en un archivo JSON."""
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as arch:
            json.dump(datos, arch, indent=4, ensure_ascii=False)

    except OSError:
        print(f"Error: no se pudo guardar '{nombre_archivo}'.")


def guardar_fixture(nombre_archivo, fixture):
    """Guarda el fixture en un archivo JSON escribiendo un partido por línea."""
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as arch:
            arch.write("[\n")

            for i in range(len(fixture)):
                linea = "    " + json.dumps(fixture[i])

                if i < len(fixture) - 1:
                    linea += ","

                arch.write(linea + "\n")

            arch.write("]")

    except OSError:
        print(f"Error: no se pudo guardar '{nombre_archivo}'.")


# ============================================================
# VALIDACIONES
# ============================================================

def es_numerico(valor):
    """Convierte una cadena de dígitos a entero; devuelve None si no es numérica."""
    if valor.isdigit():
        return int(valor)


def validacion_de_rango(min, max, valor):
    """Verifica que un valor esté entre min y max, solicitándolo de nuevo si no cumple."""
    try:
        while valor < min or valor > max:
            print(f"Error. Ingrese un valor entre {min} a {max}")
            valor = es_numerico(input("Ingrese la operación que desea realizar: "))

        return valor

    except TypeError:
        print(f"ERROR. El valor ingresado no es numerico")


def validar_estadisticas(equipos, fixture, cantidad_equipos):
    """Recalcula PJ, PG, PP y PTS desde el fixture y verifica que coincidan con equipos."""
    if len(equipos) != cantidad_equipos:
        print(f"Se esperaban {cantidad_equipos} equipos y hay {len(equipos)}.")
        return False

    esperado = []
    for i in range(cantidad_equipos):
        esperado.append({"PJ": 0, "PG": 0, "PP": 0, "PTS": 0})

    for partido in fixture:
        jornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido

        if jugado == 1:
            if puntosA > puntosB:
                ganador, perdedor = idA, idB
            else:
                ganador, perdedor = idB, idA

            esperado[idA]["PJ"] += 1
            esperado[idB]["PJ"] += 1
            esperado[ganador]["PG"] += 1
            esperado[ganador]["PTS"] += 3
            esperado[perdedor]["PP"] += 1

    for i in range(cantidad_equipos):
        if equipos[i]["estadisticas"] != esperado[i]:
            print(f"Las estadísticas de '{equipos[i]['nombre']}' no coinciden "
                  f"con sus partidos jugados.")
            return False

    return True


# ============================================================
# REGISTRO
# ============================================================

def validar_suficientes_equipos(equipos, cantidad):
    """Verifica si se alcanzó la cantidad mínima de equipos requerida."""
    valido = True

    if len(equipos) < cantidad:
        valido = False

    return valido


def validar_registro_equipo(equipos, nombre, tag, region, regionesValidas):
    """Valida formato, unicidad de nombre/tag y región permitida para un nuevo equipo."""
    valido = True

    # Nombre no vacío, sin espacios dobles ni repetido
    if nombre == "":
        print("El nombre del equipo no puede estar vacío.")
        valido = False

    if "  " in nombre:
        print("El nombre no puede tener espacios dobles o de más.")
        valido = False

    nombreNormalizado = normalizar_string(nombre)

    for equipo in equipos:
        if normalizar_string(equipo["nombre"]) == nombreNormalizado:
            print("El nombre de equipo ya está registrado.")
            valido = False

    # Tag no vacío ni repetido
    if tag == "":
        print("El tag no puede estar vacío.")
        valido = False

    tagNormalizado = normalizar_string(tag)

    for equipo in equipos:
        if equipo["tag"] == tagNormalizado:
            print("El tag ya está registrado por otro equipo.")
            valido = False

    # Región no vacía y dentro de las habilitadas
    if region == "":
        print("La región no puede estar vacía.")
        valido = False

    regionNormalizada = normalizar_string(region)

    if regionNormalizada not in regionesValidas:
        print(
            f"Región inválida. Las regiones permitidas son: "
            f"{', '.join(regionesValidas)}.")
        valido = False

    return valido


def registrar(equipos, nombre, tag, region):
    """Agrega un equipo con estadísticas en cero a la lista y devuelve su ID."""
    idNuevo = len(equipos)

    equipoNuevo = {
        "nombre": nombre,
        "tag": tag,
        "region": region,
        "estadisticas": {
            "PJ": 0,
            "PG": 0,
            "PP": 0,
            "PTS": 0,
        }}

    equipos.append(equipoNuevo)

    return idNuevo


def registrar_equipo(equipos, regionesValidas):
    """Solicita los datos de un equipo por consola y lo registra si es válido."""
    print("\n--- Registrar equipo ---")

    nombre = input("Nombre del equipo: ").strip()

    tag = normalizar_string(
        input("Tag (código corto): ")
    )

    region = normalizar_string(input(f"Región ({', '.join(regionesValidas)}): ")
)

    valido = validar_registro_equipo(
        equipos,
        nombre,
        tag,
        region,
        regionesValidas
    )

    if not valido:
        print("No se registro el equipo.")

    else:
        idEquipo = registrar(
            equipos,
            nombre,
            tag,
            region
        )

        print(
            f"El equipo '{equipos[idEquipo]['nombre']}' "
            f"fue registrado correctamente con el id {idEquipo}."
        )


# ============================================================
# FIXTURE
# ============================================================

def generar_partidos(cantidad_equipos, mapas):
    """Genera el fixture todos contra todos (Round-Robin) con mapas aleatorios."""
    partidos = []
    ids = list(range(cantidad_equipos))

    total_jornadas = cantidad_equipos - 1
    partidos_por_jornada = cantidad_equipos // 2

    for jornada in range(1, total_jornadas + 1):
        for i in range(partidos_por_jornada):
            idA = ids[i]
            idB = ids[(cantidad_equipos - 1) - i]
            mapa_id = random.randint(0, len(mapas) - 1)

            # Formato: [jornada, idA, idB, puntosA, puntosB, jugado, mapa_id]
            partido = [jornada, idA, idB, 0, 0, 0, mapa_id]
            partidos.append(partido)

        # Rotación Round-Robin dejando fijo el primer elemento
        ids.insert(1, ids.pop())

    return partidos


def validar_fixture(fixture, cantidad_equipos, cantidad_mapas, reglas):
    """Verifica la estructura, rangos, resultados y cruces únicos del fixture."""
    if not isinstance(fixture, list):
        print("El fixture debe ser una lista de partidos.")
        return False

    total_jornadas = cantidad_equipos - 1
    partidos_por_jornada = cantidad_equipos // 2

    if len(fixture) != total_jornadas * partidos_por_jornada:
        print(f"El fixture debería tener {total_jornadas * partidos_por_jornada} "
              f"partidos y tiene {len(fixture)}.")
        return False

    parejas_vistas = []
    equipos_por_jornada = {}

    for partido in fixture:

        # 1) Estructura de 7 enteros
        if not isinstance(partido, list) or len(partido) != 7:
            print(f"Partido mal formado: {partido}")
            return False

        for valor in partido:
            if not isinstance(valor, int) or isinstance(valor, bool):
                print(f"El partido {partido} tiene un valor que no es entero.")
                return False

        jornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido

        # 2) Rangos válidos de jornada, equipos y mapa
        if jornada < 1 or jornada > total_jornadas:
            print(f"Jornada inválida en {partido}.")
            return False

        if idA < 0 or idA >= cantidad_equipos or idB < 0 or idB >= cantidad_equipos:
            print(f"Hay un id de equipo inexistente en {partido}.")
            return False

        if idA == idB:
            print(f"Un equipo no puede jugar contra sí mismo: {partido}.")
            return False

        if mapa_id < 0 or mapa_id >= cantidad_mapas:
            print(f"El mapa_id de {partido} no existe en la configuración.")
            return False

        # 3) Coherencia entre estado 'jugado' y marcador
        if jugado != 0 and jugado != 1:
            print(f"'jugado' debe ser 0 o 1 en {partido}.")
            return False

        if jugado == 1:
            if puntosA == puntosB or not validar_resultado(puntosA, puntosB, reglas):
                print(f"Resultado inválido en {partido}.")
                return False
        elif puntosA != 0 or puntosB != 0:
            print(f"Un partido no jugado debe tener 0-0: {partido}.")
            return False

        # 4) Sin enfrentamientos repetidos en el torneo
        pareja = (min(idA, idB), max(idA, idB))
        if pareja in parejas_vistas:
            print(f"La pareja {pareja} aparece repetida.")
            return False
        parejas_vistas.append(pareja)

        # 5) Sin equipos repetidos en una misma jornada
        if jornada not in equipos_por_jornada:
            equipos_por_jornada[jornada] = []

        if idA in equipos_por_jornada[jornada] or idB in equipos_por_jornada[jornada]:
            print(f"Un equipo juega dos veces en la jornada {jornada}.")
            return False

        equipos_por_jornada[jornada].append(idA)
        equipos_por_jornada[jornada].append(idB)

    return True


# ============================================================
# EQUIPOS
# ============================================================

def listar_equipos(equipos):
    """Devuelve un texto con el listado numerado de todos los equipos."""
    lineas = []

    for i in range(len(equipos)):
        linea = (
            f"{i}. "
            f"{equipos[i]['nombre']} "
            f"[{equipos[i]['tag']}] - "
            f"{equipos[i]['region']}"
        )

        lineas.append(linea)

    return "\n".join(lineas)


def buscar_equipo(equipos, busqueda):
    """Busca un equipo por ID o tag y devuelve su índice, o -1 si no existe."""
    idEncontrado = -1

    idBuscado = es_numerico(busqueda)

    if idBuscado is not None:
        if 0 <= idBuscado < len(equipos):
            idEncontrado = idBuscado

    else:
        tagNormalizado = normalizar_string(busqueda)

        for i in range(len(equipos)):
            if equipos[i]["tag"] == tagNormalizado:
                idEncontrado = i

    return idEncontrado


def buscar_y_mostrar_equipo(equipos):
    """Solicita un ID o tag por consola y muestra las estadísticas del equipo."""
    busqueda = input("Ingrese ID o tag del equipo a buscar: ").strip()

    idEquipo = buscar_equipo(equipos, busqueda)

    if idEquipo == -1:
        print("No se encontró ningún equipo con ese ID o tag.")
    else:
        print(mostrar_equipo(equipos, idEquipo))


def mostrar_equipo(equipos, idEquipo):
    """Formatea los datos, estadísticas y porcentaje de victorias de un equipo."""
    estadisticas = equipos[idEquipo]["estadisticas"]
    pj = estadisticas["PJ"]
    pg = estadisticas["PG"]
    pp = estadisticas["PP"]
    pts = estadisticas["PTS"]

    porcentaje = (
        (pg / pj * 100)
        if pj > 0
        else 0
    )

    return (
        f"ID {idEquipo}: "
        f"{equipos[idEquipo]['nombre']} "
        f"[{equipos[idEquipo]['tag']}] - "
        f"{equipos[idEquipo]['region']}\n"
        f"PJ:{pj} PG:{pg} PP:{pp} Pts:{pts} | "
        f"% Victorias: {porcentaje:.1f}%"
    )


# ============================================================
# PARTIDOS
# ============================================================

def validar_resultado(puntosA, puntosB, reglas):
    """Verifica que el marcador cumpla los puntos para ganar, diferencia mínima y overtime."""
    puntos_para_ganar = reglas["puntos_para_ganar"]
    dif_min = reglas["diferencia_minima"]
    overtime = reglas["permite_overtime"]

    max_p = max(puntosA, puntosB)
    min_p = min(puntosA, puntosB)
    puntaje_valido = True

    # Puntaje mínimo para ganar
    if max_p < puntos_para_ganar:
        print(f"Error: un equipo debe alcanzar al menos {puntos_para_ganar} "
              f"para ganar.")
        puntaje_valido = False

    # Diferencia mínima en tiempo regular
    if max_p == puntos_para_ganar:
        if min_p > puntos_para_ganar - dif_min:
            print(f"Error: con {puntos_para_ganar} puntos, el rival puede tener "
                  f"como máximo {puntos_para_ganar - dif_min}.")
            puntaje_valido = False

    # Validación de overtime
    if max_p > puntos_para_ganar:
        if not overtime:
            print(f"Error: este juego no tiene overtime, "
                  f"el máximo es {puntos_para_ganar}.")
            puntaje_valido = False
        elif (max_p - min_p) != dif_min:
            print(f"Error: en overtime, la diferencia debe ser exactamente "
                  f"{dif_min}.")
            puntaje_valido = False

    return puntaje_valido


def jornada_actual(fixture):
    """Devuelve el número de la primera jornada con partidos pendientes, o 0 si terminó."""
    for partido in fixture:
        nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido
        if jugado == 0:
            return nJornada
    return 0


def partidos_pendientes(fixture, jornada):
    """Devuelve la lista de partidos no jugados correspondientes a la jornada indicada."""
    pendientes = []
    for partido in fixture:
        nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido
        if nJornada == jornada and jugado == 0:
            pendientes.append(partido)
    return pendientes


def listar_partidos_pendientes(jornada, fixture, equipos):
    """Muestra por consola los enfrentamientos pendientes de la jornada actual."""
    print(
        f"Actualmente se está jugando la jornada N° {jornada}"
    )

    print("Los partidos pendientes son:")

    for partido in partidos_pendientes(fixture, jornada):
        nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido

        print(
            f"{equipos[idA]['nombre']} vs "
            f"{equipos[idB]['nombre']}"
        )


def pedir_puntaje(mensaje):
    """Solicita por consola un número entero hasta recibir un valor válido."""
    puntaje = es_numerico(input(mensaje))

    while puntaje is None:
        print("Error. Debe ingresar un número entero.")
        puntaje = es_numerico(input(mensaje))

    return puntaje


def registrar_resultados(jornada, fixture, equipos, reglas):
    """Carga el resultado del próximo partido pendiente y actualiza las estadísticas."""
    pendientes = partidos_pendientes(fixture, jornada)
    partido_actual = pendientes[0]
    nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido_actual

    equipoA = equipos[idA]["nombre"]
    equipoB = equipos[idB]["nombre"]

    print(
            f"El partido actual es "
            f"{equipoA} vs {equipoB}"
        )

    while True:
            ganadasA = pedir_puntaje(f"Ingrese la puntuación de {equipoA}: ")
            ganadasB = pedir_puntaje(f"Ingrese la puntuación de {equipoB}: ")

            if ganadasA == ganadasB:
                print("Error. No se permiten empates.")

            elif not validar_resultado(ganadasA, ganadasB, reglas):
                print("Por favor, ingrese los puntajes nuevamente.")

            else:
                break

    partido_actual[3] = ganadasA
    partido_actual[4] = ganadasB
    partido_actual[5] = 1

    actualizar_estadisticas(equipos, idA, idB, ganadasA, ganadasB)


def actualizar_estadisticas(equipos, idA, idB, ganadasA, ganadasB):
    """Actualiza PJ, PG, PP y PTS de ambos equipos según el ganador del partido."""
    equipos[idA]["estadisticas"]["PJ"] += 1
    equipos[idB]["estadisticas"]["PJ"] += 1

    if ganadasA > ganadasB:

        equipos[idA]["estadisticas"]["PG"] += 1
        equipos[idB]["estadisticas"]["PP"] += 1
        equipos[idA]["estadisticas"]["PTS"] += 3

    else:

        equipos[idB]["estadisticas"]["PG"] += 1
        equipos[idA]["estadisticas"]["PP"] += 1
        equipos[idB]["estadisticas"]["PTS"] += 3


# ============================================================
# HISTORIAL
# ============================================================

def consultar_historial(fixture, equipos, mapas):
    """Devuelve el listado formateado de todos los partidos disputados."""
    lineas = []

    for partido in fixture:
        nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido
        if jugado == 1:

            equipoA = equipos[idA]["nombre"]
            equipoB = equipos[idB]["nombre"]

            linea = (
                f"Jornada {nJornada}: "
                f"{equipoA} {puntosA} - "
                f"{puntosB} {equipoB} "
                f"(Mapa: {mapas[mapa_id]})"
            )

            lineas.append(linea)

    return "\n".join(lineas)


# ============================================================
# RANKING Y TABLA DE POSICIONES
# ============================================================

def generar_ranking(equipos):
    """Devuelve los IDs de los equipos ordenados de mayor a menor por PTS y PG."""
    indices = list(range(len(equipos)))

    ranking = sorted(
        indices,
        key=lambda i: (
            equipos[i]["estadisticas"]["PTS"],
            equipos[i]["estadisticas"]["PG"]
        ),
        reverse=True
    )

    return ranking


def tabla_de_posiciones(equipos):
    """Genera la tabla de posiciones completa formateada en columnas."""
    ranking = generar_ranking(equipos)

    encabezado = (
        f"{'Pos':<4}"
        f"{'Equipo':<20}"
        f"{'Tag':<8}"
        f"{'Región':<8}"
        f"{'PJ':<5}"
        f"{'PG':<5}"
        f"{'PP':<5}"
        f"{'Pts':<5}"
    )

    lineas = [encabezado]

    for pos, i in enumerate(ranking, start=1):
        est = equipos[i]["estadisticas"]

        linea = (
            f"{pos:<4}"
            f"{equipos[i]['nombre']:<20}"
            f"{equipos[i]['tag']:<8}"
            f"{equipos[i]['region']:<8}"
            f"{est['PJ']:<5}"
            f"{est['PG']:<5}"
            f"{est['PP']:<5}"
            f"{est['PTS']:<5}"
        )

        lineas.append(linea)

    return "\n".join(lineas)


# ============================================================
# FUNCIONES DE INFORME
# ============================================================

def detectar_lideres(equipos):
    """Devuelve los IDs de los equipos que comparten el puntaje máximo."""
    max_puntos = max(e["estadisticas"]["PTS"] for e in equipos)

    lideres = [
        i
        for i in range(len(equipos))
        if equipos[i]["estadisticas"]["PTS"] == max_puntos
    ]

    return lideres


def top_3(equipos):
    """Devuelve los IDs de los primeros 3 equipos del ranking."""
    return generar_ranking(equipos)[:3]


def racha_maxima(partidos, cantidad_equipos):
    """Calcula la mayor racha de victorias seguidas y devuelve (ids_equipos, valor)."""
    racha_actual = [0] * cantidad_equipos
    racha_max = [0] * cantidad_equipos

    for partido in partidos:
        jornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido

        if jugado == 1:
            if puntosA > puntosB:
                ganador, perdedor = idA, idB
            else:
                ganador, perdedor = idB, idA

            racha_actual[ganador] += 1
            racha_actual[perdedor] = 0

            if racha_actual[ganador] > racha_max[ganador]:
                racha_max[ganador] = racha_actual[ganador]

    valor_max = max(racha_max)

    equipos_racha = [
        i
        for i in range(cantidad_equipos)
        if racha_max[i] == valor_max
    ]

    return equipos_racha, valor_max


def equipos_invictos(equipos):
    """Devuelve los nombres de los equipos con PJ > 0 y PP == 0."""
    return [
        equipos[i]["nombre"]
        for i in range(len(equipos))
        if equipos[i]["estadisticas"]["PJ"] > 0
        and equipos[i]["estadisticas"]["PP"] == 0
    ]


def resumen_general(equipos, partidos):
    """Genera un resumen con total de equipos, partidos jugados, promedio de rondas y líderes."""
    partidos_jugados = 0
    total_rounds = 0

    for partido in partidos:
        if partido[5] == 1:
            partidos_jugados += 1
            total_rounds += partido[3] + partido[4]

    if partidos_jugados > 0:
        promedio = total_rounds / partidos_jugados
    else:
        promedio = 0

    lideres = detectar_lideres(equipos)
    nombres = [equipos[i]["nombre"] for i in lideres]

    return (
        f"Equipos registrados: {len(equipos)}\n"
        f"Partidos jugados: {partidos_jugados}\n"
        f"Promedio de puntos por partido: {promedio:.1f}\n"
        f"Líder(es) del torneo: {', '.join(nombres)}"
    )


def informe_lideres(equipos):
    """Devuelve el texto del informe con los líderes actuales del torneo."""
    nombres = [equipos[i]["nombre"] for i in detectar_lideres(equipos)]
    return f"Líder(es) del torneo (máximo puntaje): {', '.join(nombres)}"


def informe_top3(equipos):
    """Devuelve el texto del informe con el Top 3 del torneo."""
    lineas = ["Top 3:"]

    for pos, i in enumerate(top_3(equipos), start=1):
        lineas.append(
            f"{pos}. {equipos[i]['nombre']} [{equipos[i]['tag']}] - "
            f"{equipos[i]['estadisticas']['PTS']} pts"
        )

    return "\n".join(lineas)


def informe_racha(equipos, partidos):
    """Devuelve el texto del informe con la racha de victorias más larga."""
    ids, valor = racha_maxima(partidos, len(equipos))

    if valor == 0:
        return "Todavía no hay rachas de victorias registradas."

    nombres = [equipos[i]["nombre"] for i in ids]

    return (
        f"Racha de victorias más larga: {valor} partidos seguidos "
        f"({', '.join(nombres)})"
    )


def informe_invictos(equipos):
    """Devuelve el texto del informe con los equipos invictos."""
    invictos = equipos_invictos(equipos)

    if not invictos:
        return "No hay equipos invictos."

    return f"Equipos invictos: {', '.join(invictos)}"


def menu_informes():
    """Muestra el submenú de informes y devuelve la opción válida elegida."""
    print("""
--- Informes ---
1. Líder(es) del torneo
2. Top 3
3. Racha de victorias más larga
4. Equipos invictos
5. Resumen general
6. Volver
    """)

    operacion = es_numerico(
        input("Ingrese la operación que desea realizar: ")
    )

    return validacion_de_rango(1, 6, operacion)


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def menu(info):
    """Muestra el menú principal del torneo y devuelve la opción válida elegida."""
    print(f"""
----> {info[0]} - {info[1]} <----
1. Listar equipos
2. Buscar estadisticas de equipo
3. Ver partidos pendientes
4. Cargar resultado
5. Consultar historial
6. Tabla de posiciones
7. Informes 
8. Salir
    """)

    operacion = es_numerico(
        input("Ingrese la operación que desea realizar: ")
    )

    operacion = validacion_de_rango(
        1,
        8,
        operacion
    )

    return operacion