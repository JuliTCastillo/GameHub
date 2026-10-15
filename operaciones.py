import re
import random
import json

def normalizar_string(string):
    return re.sub(r"\s+", "", string.upper())


# ============================================================
# CONFIGURACION DE TORNEO
# ============================================================

def cargar_configuracion(nombre_archivo):
    """Lee un archivo JSON y devuelve su contenido como diccionario.
    Si algo falla, avisa y devuelve None."""
    try:
        # "with" abre el archivo y lo cierra solo al terminar el bloque
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
    """Chequea que la configuración tenga todo lo necesario."""

    # 0) Que el JSON sea un diccionario (podría ser una lista, por ejemplo)
    if not isinstance(config, dict):
        print("La configuración debe ser un objeto JSON { ... }.")
        return False

    valida = True

    # 1) Que existan las secciones principales
    secciones = ("torneo", "reglas", "regiones_validas", "mapas")
    for seccion in secciones:
        if seccion not in config:
            print(f"Falta la sección '{seccion}' en la configuración.")
            valida = False

    if not valida:
        return valida

    # 2) Que torneo y reglas sean diccionarios y tengan todas sus claves
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

    # 3) Tipos de los valores
    # (bool es un subtipo de int en Python, por eso se excluye aparte)
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

    # Si los tipos están mal, comparar números podría fallar
    if not valida:
        return valida

    # 4) Rangos y coherencia de los números
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

    # 5) Mapas: lista no vacía
    if not isinstance(config["mapas"], list) or len(config["mapas"]) == 0:
        print("'mapas' debe ser una lista con al menos un mapa.")
        valida = False

    # 6) Regiones: lista no vacía, y cada una ya normalizada
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
    """Lee un JSON. Si el archivo no existe (primera vez), devuelve
    el valor por defecto. Si está dañado, avisa y devuelve None."""
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as arch:
            return json.load(arch)

    except FileNotFoundError:
        return valor_por_defecto

    except json.JSONDecodeError:
        print(f"Error: '{nombre_archivo}' está dañado o no es un JSON válido.")
        return None


def guardar_datos(nombre_archivo, datos):
    """Escribe los datos en un archivo JSON."""
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as arch:
            json.dump(datos, arch, indent=4, ensure_ascii=False)

    except OSError:
        print(f"Error: no se pudo guardar '{nombre_archivo}'.")

# ============================================================
# VALIDACIONES
# ============================================================

def es_numerico(valor):
    if valor.isdigit():
        return int(valor)


def validacion_de_rango(min, max, valor):
    try:
        while valor < min or valor > max:
            print(f"Error. Ingrese un valor entre {min} a {max}")
            valor = es_numerico(input("Ingrese la operación que desea realizar: "))

        return valor

    except TypeError:
        print(f"ERROR. El valor ingresado no es numerico")


def validar_estadisticas(equipos, fixture, cantidad_equipos):
    """Recalcula PJ, PG, PP y PTS desde el fixture y los compara
    con lo que dice equipos.json."""

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
    valido = True

    if len(equipos) < cantidad:
        valido = False

    return valido


def validar_registro_equipo(equipos, nombre, tag, region, regionesValidas):
    valido = True

    # Validar nombre
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

    # Validar tag
    if tag == "":
        print("El tag no puede estar vacío.")
        valido = False

    tagNormalizado = normalizar_string(tag)

    for equipo in equipos:
        if equipo["tag"] == tagNormalizado:
            print("El tag ya está registrado por otro equipo.")
            valido = False

    # Validar región
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
    partidos = []
    ids = list(range(cantidad_equipos))
    
    # En un formato todos contra todos, la cantidad de jornadas es N - 1
    total_jornadas = cantidad_equipos - 1
    partidos_por_jornada = cantidad_equipos // 2

    for jornada in range(1, total_jornadas + 1):
        for i in range(partidos_por_jornada):
            idA = ids[i]
            # Emparejamos el primero con el último, el segundo con el penúltimo, etc.
            idB = ids[(cantidad_equipos - 1) - i]
            
            # Sorteamos el índice del mapa
            mapa_id = random.randint(0, len(mapas) - 1)
            
            # Estructura: [jornada, idA, idB, puntosA, puntosB, jugado, mapa_id]
            partido = [jornada, idA, idB, 0, 0, 0, mapa_id]
            partidos.append(partido)

        # Rotación del algoritmo Round-Robin: 
        # El equipo en el índice 0 queda fijo, el último pasa a la posición 1.
        ids.insert(1, ids.pop())

    return partidos


def validar_fixture(fixture, cantidad_equipos, cantidad_mapas, reglas):
    """Revisa que un fixture cargado desde archivo sea usable."""

    if not isinstance(fixture, list):
        print("El fixture debe ser una lista de partidos.")
        return False

    total_jornadas = cantidad_equipos - 1
    partidos_por_jornada = cantidad_equipos // 2

    # Cantidad total esperada de partidos
    if len(fixture) != total_jornadas * partidos_por_jornada:
        print(f"El fixture debería tener {total_jornadas * partidos_por_jornada} "
              f"partidos y tiene {len(fixture)}.")
        return False

    parejas_vistas = []
    equipos_por_jornada = {}   # jornada -> ids que ya juegan en esa jornada

    for partido in fixture:

        # 1) Estructura: lista de 7 enteros
        if not isinstance(partido, list) or len(partido) != 7:
            print(f"Partido mal formado: {partido}")
            return False

        for valor in partido:
            if not isinstance(valor, int) or isinstance(valor, bool):
                print(f"El partido {partido} tiene un valor que no es entero.")
                return False

        jornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido

        # 2) Rangos
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

        # 3) Resultado coherente con el estado "jugado"
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

        # 4) Cada pareja juega una sola vez
        pareja = (min(idA, idB), max(idA, idB))
        if pareja in parejas_vistas:
            print(f"La pareja {pareja} aparece repetida.")
            return False
        parejas_vistas.append(pareja)

        # 5) Un equipo no juega dos veces en la misma jornada
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
    busqueda = input("Ingrese ID o tag del equipo a buscar: ").strip()
    
    idEquipo = buscar_equipo(equipos, busqueda)

    if idEquipo == -1:
        print("No se encontró ningún equipo con ese ID o tag.")
    else:
        print(mostrar_equipo(equipos, idEquipo))


def mostrar_equipo(equipos, idEquipo):
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
    puntos_para_ganar = reglas["puntos_para_ganar"]
    dif_min = reglas["diferencia_minima"]
    overtime = reglas["permite_overtime"]

    max_p = max(puntosA, puntosB)
    min_p = min(puntosA, puntosB)
    puntaje_valido = True

    # Regla 1: alguien tiene que llegar al objetivo sí o sí
    if max_p < puntos_para_ganar:
        print(f"Error: un equipo debe alcanzar al menos {puntos_para_ganar} "
              f"para ganar.")
        puntaje_valido = False

    # Regla 2: si el ganador llegó justo al objetivo, el perdedor debe quedar
    # a la diferencia mínima o más lejos
    if max_p == puntos_para_ganar:
        if min_p > puntos_para_ganar - dif_min:
            print(f"Error: con {puntos_para_ganar} puntos, el rival puede tener "
                  f"como máximo {puntos_para_ganar - dif_min}.")
            puntaje_valido = False

    # Regla 3: pasar el objetivo solo se permite si hay overtime
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
    for partido in fixture:
        nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido
        if jugado == 0:
            return nJornada
    return 0


def partidos_pendientes(fixture, jornada):
    pendientes = []
    for partido in fixture:
        nJornada, idA, idB, puntosA, puntosB, jugado, mapa_id = partido
        if nJornada == jornada and jugado == 0:
            pendientes.append(partido)
    return pendientes


def listar_partidos_pendientes(jornada, fixture, equipos):
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
    puntaje = es_numerico(input(mensaje))

    while puntaje is None:
        print("Error. Debe ingresar un número entero.")
        puntaje = es_numerico(input(mensaje))

    return puntaje


def registrar_resultados(jornada, fixture, equipos, reglas):
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
    """Ids de los equipos con el máximo de puntos (sin desempate)."""
    max_puntos = max(e["estadisticas"]["PTS"] for e in equipos)

    lideres = [
        i
        for i in range(len(equipos))
        if equipos[i]["estadisticas"]["PTS"] == max_puntos
    ]

    return lideres


def top_3(equipos):
    return generar_ranking(equipos)[:3]


def racha_maxima(partidos, cantidad_equipos):
    """Racha más larga de victorias seguidas. Devuelve (ids, valor)."""
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
    """Nombres de los equipos con PJ > 0 y PP == 0."""
    return [
        equipos[i]["nombre"]
        for i in range(len(equipos))
        if equipos[i]["estadisticas"]["PJ"] > 0
        and equipos[i]["estadisticas"]["PP"] == 0
    ]


def resumen_general(equipos, partidos):
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
    nombres = [equipos[i]["nombre"] for i in detectar_lideres(equipos)]
    return f"Líder(es) del torneo (máximo puntaje): {', '.join(nombres)}"


def informe_top3(equipos):
    lineas = ["Top 3:"]

    for pos, i in enumerate(top_3(equipos), start=1):
        lineas.append(
            f"{pos}. {equipos[i]['nombre']} [{equipos[i]['tag']}] - "
            f"{equipos[i]['estadisticas']['PTS']} pts"
        )

    return "\n".join(lineas)


def informe_racha(equipos, partidos):
    ids, valor = racha_maxima(partidos, len(equipos))

    if valor == 0:
        return "Todavía no hay rachas de victorias registradas."

    nombres = [equipos[i]["nombre"] for i in ids]

    return (
        f"Racha de victorias más larga: {valor} partidos seguidos "
        f"({', '.join(nombres)})"
    )


def informe_invictos(equipos):
    invictos = equipos_invictos(equipos)

    if not invictos:
        return "No hay equipos invictos."

    return f"Equipos invictos: {', '.join(invictos)}"


def menu_informes():
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