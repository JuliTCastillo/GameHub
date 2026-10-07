import re
import random


def normalizar_string(string):
    return re.sub(r"\s+", "", string.upper())


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


# ============================================================
# REGISTRO
# ============================================================

def validar_suficientes_equipos(equipos, cantidad):
    valido = True

    if len(equipos) < cantidad:
        valido = False

    return valido


def validar_registro_equipo(equipos, nombre, tag, region):
    regionesValidas = ("NA", "EU", "LATAM", "APAC", "KR", "BR", "OCE")
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
            f"{regionesValidas}."
        )
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


def registrar_equipo(equipos):
    print("\n--- Registrar equipo ---")

    nombre = input("Nombre del equipo: ").strip()

    tag = normalizar_string(
        input("Tag (código corto): ")
    )

    region = normalizar_string(
        input(
            'Región("NA", "EU", "LATAM", "APAC", "KR", "BR", "OCE"): '
        )
    )

    valido = validar_registro_equipo(
        equipos,
        nombre,
        tag,
        region
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

def validar_resultado_valorant(puntosA, puntosB):
    max_p = max(puntosA, puntosB)
    min_p = min(puntosA, puntosB)
    puntaje_valido = True
    # Regla 1: Alguien tiene que llegar a 13 sí o sí
    if max_p < 13:
        print("Error: Un equipo debe alcanzar al menos 13 rondas para ganar (ej: 13-8).")
        puntaje_valido = False
        
    # Regla 2: Si el ganador tiene 13, el perdedor debe tener 11 o menos
    if max_p == 13:
        if min_p > 11:
            print("Error: Si llegan a 12-12, hay Overtime. El resultado no puede ser 13-12.")
            puntaje_valido = False
            
    # Regla 3: Si hay Overtime (más de 13 puntos), la diferencia DEBE ser exactamente 2
    if max_p > 13:
        if (max_p - min_p) != 2:
            print("Error: En Overtime, se debe ganar por una diferencia exacta de 2 puntos (ej: 14-12, 16-14).")
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


def registrar_resultados(jornada, fixture, equipos):
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
                print("Error. No se permiten empates en Valorant.")
            
            elif not validar_resultado_valorant(ganadasA, ganadasB):
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

def consultar_historial(fixture, equipos, MAPAS):
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
                f"(Mapa: {MAPAS[mapa_id]})"
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
        f"Promedio de rounds por partido: {promedio:.1f}\n"
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