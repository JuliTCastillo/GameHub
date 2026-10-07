import re

def normalizar_string(string):
    return re.sub(r"\s+", "", string.upper())


# ============================================================
# VALIDACIONES
# ============================================================

def validacion_de_rango(min, max, valor):
    try:
        while valor < min or valor > max:
            print(f"Error. Ingrese un valor tiene que estar entre {min} a {max}")
            valor = es_numerico(input("Ingrese la operación que desea realizar: "))

        return valor

    except TypeError:
        print(f"ERROR. El valor ingresado no es numerico")


def es_numerico(valor):
    if valor.isdigit():
        return int(valor)


def validar_suficientes_equipos(equipos):
    valido = True

    if len(equipos) < 8:
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

    if " " in tag:
        print("El tag no puede tener espacios en medio.")
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


# ============================================================
# OPERACIONES DE EQUIPOS
# ============================================================

def registrar(equipos, posiciones, nombre, tag, region):
    """
    Agrega un equipo nuevo a la lista de diccionarios
    y una fila en cero a posiciones.

    El id del equipo queda determinado por su posición
    (índice) en la lista.
    """

    idNuevo = len(equipos)

    equipoNuevo = {
        "nombre": nombre,
        "tag": tag,
        "region": region
    }

    equipos.append(equipoNuevo)

    # Por ahora posiciones sigue siendo una matriz independiente.
    posiciones.append([0, 0, 0, 0])

    return idNuevo


def registrar_equipo(equipos, posiciones):
    """RF04-06: valida antes de registrar un equipo."""

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
            posiciones,
            nombre,
            tag,
            region
        )

        print(
            f"El equipo '{equipos[idEquipo]['nombre']}' "
            f"fue registrado correctamente con el id {idEquipo}."
        )


def listar_equipos(equipos):
    """RF11: arma el listado de equipos registrados para mostrar."""

    if len(equipos) == 0:
        return "Todavía no hay equipos registrados."

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


# ============================================================
# FIXTURE
# ============================================================

def validar_partidos_pendientes(fixture):
    jornada = jornada_actual(fixture)

    continua = True

    if jornada == 0:
        continua = False

    return continua


def jornada_actual(fixture):
    for grupoJornada in range(len(fixture)):

        for partido in fixture[grupoJornada]:
            _, _, jugado = partido

            if jugado == 0:
                return grupoJornada + 1

    return 0


def partidos_pendientes(fixture, jornada):
    pendientes = []

    for partido in fixture[jornada - 1]:
        idA, idB, jugado = partido

        if jugado == 0:
            pendientes.append(partido)

    return pendientes


def listar_partidos_pendientes(fixture, equipos):
    jornada = jornada_actual(fixture)

    print(
        f"Actualmente se está jugando la jornada N° {jornada}"
    )

    print("Los partidos pendientes son:")

    for partido in partidos_pendientes(fixture, jornada):

        idA, idB, jugado = partido

        print(
            f"{equipos[idA]['nombre']} vs "
            f"{equipos[idB]['nombre']}"
        )


# ============================================================
# RESULTADOS
# ============================================================

def pedir_puntaje(mensaje):
    puntaje = es_numerico(input(mensaje))

    while puntaje is None:
        print("Error. Debe ingresar un número entero.")
        puntaje = es_numerico(input(mensaje))

    return puntaje


def pedir_mapa(mapasHabilitados):
    mapa = normalizar_string(
        input(f"Ingrese el mapa jugado {mapasHabilitados}: ")
    )

    mapasNormalizados = [
        normalizar_string(m)
        for m in mapasHabilitados
    ]

    while mapa not in mapasNormalizados:
        print(
            f"Mapa inválido. Debe ser uno de: "
            f"{mapasHabilitados}"
        )

        mapa = normalizar_string(
            input("Ingrese el mapa jugado: ")
        )

    return mapa


def registrar_resultados(
    fixture,
    historial,
    posiciones,
    equipos,
    mapasHabilitados
):

    jornada = jornada_actual(fixture)

    partidos = partidos_pendientes(
        fixture,
        jornada
    )

    partido_actual = partidos[0]

    idA, idB, _ = partido_actual

    equipoA = equipos[idA]["nombre"]
    equipoB = equipos[idB]["nombre"]

    print(
        f"El partido actual es "
        f"{equipoA} vs {equipoB}"
    )

    while True:

        puntosA = pedir_puntaje(
            f"Ingrese la puntuación de {equipoA}: "
        )

        puntosB = pedir_puntaje(
            f"Ingrese la puntuación de {equipoB}: "
        )

        if puntosA == puntosB:
            print(
                "Error. No se permiten empates, "
                "los puntajes no pueden ser iguales."
            )

        else:
            break

    mapa = pedir_mapa(mapasHabilitados)

    partido_actual[2] = 1

    historial.append(
        [
            jornada,
            idA,
            idB,
            puntosA,
            puntosB,
            mapa
        ]
    )

    actualizar_posiciones(
        posiciones,
        idA,
        idB,
        puntosA,
        puntosB
    )


def actualizar_posiciones(
    liPosiciones,
    idA,
    idB,
    puntosA,
    puntosB
):
    """
    RF08: actualiza PJ, PG, PP y puntos
    de ambos equipos tras cargar un resultado.
    """

    liPosiciones[idA][0] += 1
    liPosiciones[idB][0] += 1

    if puntosA > puntosB:

        liPosiciones[idA][1] += 1
        liPosiciones[idA][3] += 3
        liPosiciones[idB][2] += 1

    else:

        liPosiciones[idB][1] += 1
        liPosiciones[idB][3] += 3
        liPosiciones[idA][2] += 1


# ============================================================
# HISTORIAL
# ============================================================

def consultar_historial(historial, equipos):
    """
    RF12: arma el listado del historial de partidos jugados,
    traduciendo los ids de equipo a nombres.
    """

    if len(historial) == 0:
        return "Todavía no se jugó ningún partido."

    lineas = []

    for partido in historial:

        jornada, idA, idB, puntosA, puntosB, mapa = partido

        equipoA = equipos[idA]["nombre"]
        equipoB = equipos[idB]["nombre"]

        linea = (
            f"Jornada {jornada}: "
            f"{equipoA} {puntosA} - "
            f"{puntosB} {equipoB} "
            f"(Mapa: {mapa})"
        )

        lineas.append(linea)

    return "\n".join(lineas)


# ============================================================
# RANKING
# ============================================================

def generar_ranking(liPosiciones):
    """
    RF18: genera el orden de los equipos por índice,
    usando lambda.

    Ordena por puntos de mayor a menor,
    y en caso de empate por PG.
    """

    indices = list(range(len(liPosiciones)))

    ranking = sorted(
        indices,
        key=lambda i: (
            liPosiciones[i][3],
            liPosiciones[i][1]
        ),
        reverse=True
    )

    return ranking


def tabla_de_posiciones(equipos, liPosiciones):
    """
    RF13/RF22: arma la tabla de posiciones ordenada
    de mayor a menor puntaje, con desempate por PG.
    """

    if len(equipos) == 0:
        return "Todavía no hay equipos registrados."

    ranking = generar_ranking(liPosiciones)

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

    pos = 1

    for i in ranking:

        pj = liPosiciones[i][0]
        pg = liPosiciones[i][1]
        pp = liPosiciones[i][2]
        pts = liPosiciones[i][3]

        linea = (
            f"{pos:<4}"
            f"{equipos[i]['nombre']:<20}"
            f"{equipos[i]['tag']:<8}"
            f"{equipos[i]['region']:<8}"
            f"{pj:<5}"
            f"{pg:<5}"
            f"{pp:<5}"
            f"{pts:<5}"
        )

        lineas.append(linea)

        pos += 1

    return "\n".join(lineas)


# ============================================================
# BÚSQUEDA Y DETALLE DE EQUIPO
# ============================================================

def buscar_equipo(equipos, busqueda):
    """
    RF13: busca por id (número) o por tag.
    Devuelve el índice, o -1 si no existe.
    """

    if busqueda.isdigit():

        idBuscado = int(busqueda)

        if 0 <= idBuscado < len(equipos):
            return idBuscado

        return -1

    tagNormalizado = normalizar_string(busqueda)

    for i in range(len(equipos)):

        if equipos[i]["tag"] == tagNormalizado:
            return i

    return -1


def mostrar_equipo(equipos, liPosiciones, idEquipo):

    pj, pg, pp, pts = liPosiciones[idEquipo]

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
# FUNCIONES DE INFORME
# ============================================================

def detectar_lideres(liPosiciones):
    """
    RF20: detecta el/los equipo(s) con el máximo puntaje,
    SIN aplicar desempate.
    """

    maxPuntos = max(
        fila[3]
        for fila in liPosiciones
    )

    lideres = [
        i
        for i in range(len(liPosiciones))
        if liPosiciones[i][3] == maxPuntos
    ]

    return lideres


def top_3(liPosiciones):
    """
    RF17/RF19: top 3 del ranking,
    usando lambda en generar_ranking + slicing.
    """

    ranking = generar_ranking(liPosiciones)

    return ranking[:3]


def racha_maxima(historial, cantEquipos):
    """
    RF16: racha de victorias consecutivas más larga
    por equipo.

    Devuelve el/los equipos que la alcanzaron
    y el valor.
    """

    rachaActual = [0] * cantEquipos
    rachaMax = [0] * cantEquipos

    for partido in historial:

        jornada, idA, idB, puntosA, puntosB, mapa = partido

        if puntosA > puntosB:
            ganador, perdedor = idA, idB

        else:
            ganador, perdedor = idB, idA

        rachaActual[ganador] += 1
        rachaActual[perdedor] = 0

        if rachaActual[ganador] > rachaMax[ganador]:
            rachaMax[ganador] = rachaActual[ganador]

    valorMax = (
        max(rachaMax)
        if rachaMax
        else 0
    )

    equiposRacha = [
        i
        for i in range(cantEquipos)
        if rachaMax[i] == valorMax
    ]

    return equiposRacha, valorMax


def equipos_invictos(equipos, liPosiciones):
    """
    RF-invictos: equipos con PJ>0 y PP==0.
    Usa comprensión de listas.
    """

    return [
        equipos[i]["nombre"]
        for i in range(len(equipos))
        if liPosiciones[i][0] > 0
        and liPosiciones[i][2] == 0
    ]


def resumen_general(equipos, liPosiciones, historial):
    """RF21: resumen general del torneo."""

    partidosJugados = len(historial)

    totalRounds = sum(
        p[3] + p[4]
        for p in historial
    )

    promedioRounds = (
        totalRounds / partidosJugados
        if partidosJugados > 0
        else 0
    )

    lideres = detectar_lideres(liPosiciones)

    nombresLideres = [
        equipos[i]["nombre"]
        for i in lideres
    ]

    return (
        f"Equipos registrados: {len(equipos)}\n"
        f"Partidos jugados: {partidosJugados}\n"
        f"Promedio general de rounds por partido: "
        f"{promedioRounds:.1f}\n"
        f"Líder(es) del torneo: "
        f"{', '.join(nombresLideres) if nombresLideres else 'Sin datos'}"
    )


def informe_lideres(equipos, liPosiciones):

    lideres = detectar_lideres(liPosiciones)

    nombres = [
        equipos[i]["nombre"]
        for i in lideres
    ]

    return (
        f"Líder(es) del torneo (máximo puntaje): "
        f"{', '.join(nombres)}"
    )


def informe_top3(equipos, liPosiciones):

    top = top_3(liPosiciones)

    lineas = ["Top 3:"]

    for pos, i in enumerate(top, start=1):

        lineas.append(
            f"{pos}. "
            f"{equipos[i]['nombre']} "
            f"[{equipos[i]['tag']}] - "
            f"{liPosiciones[i][3]} pts"
        )

    return "\n".join(lineas)


def informe_racha(equipos, historial, cantEquipos):

    equiposRacha, valor = racha_maxima(
        historial,
        cantEquipos
    )

    if valor == 0:
        return "Todavía no hay rachas de victorias registradas."

    nombres = [
        equipos[i]["nombre"]
        for i in equiposRacha
    ]

    return (
        f"Racha de victorias más larga: "
        f"{valor} partidos ganados seguidos "
        f"({', '.join(nombres)})"
    )


def informe_invictos(equipos, liPosiciones):

    invictos = equipos_invictos(
        equipos,
        liPosiciones
    )

    if not invictos:
        return "No hay equipos invictos."

    return (
        f"Equipos invictos: "
        f"{', '.join(invictos)}"
    )


# ============================================================
# SUBMENÚ DE INFORMES
# ============================================================

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

    operacion = validacion_de_rango(
        1,
        6,
        operacion
    )

    return operacion


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def menu(info):

    print(f"""
----> {info[0]} - {info[1]} <----
1. Registrar equipo
2. Listar equipos
3. Ver partidos pendientes
4. Cargar resultado
5. Consultar historial
6. Buscar equipo
7. Tabla de posiciones
8. Informes 
9. Salir
    """)

    operacion = es_numerico(
        input("Ingrese la operación que desea realizar: ")
    )

    operacion = validacion_de_rango(
        1,
        9,
        operacion
    )

    return operacion