#Validaciones
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

def normalizar_string(string):
    """RF05: normaliza el tag a mayúsculas y sin espacios."""
    return string.upper().replace(" ", "")


def validar_registro_equipo(liNombres, liTags, nombre, tag, region):

    regionesValidas = ("NA", "EU", "LATAM", "APAC", "KR", "BR", "OCE")
    valido = True

    if len(liNombres) >= 8:
        print("Ya se alcanzó el máximo de 8 equipos.")
        valido = False

    if nombre == "":
        print("El nombre del equipo no puede estar vacío.")
        valido = False

    if "  " in nombre:
        print("El nombre no puede tener espacios dobles o de más.")
        valido = False

    nombreNormalizado = normalizar_string(nombre)
    for nombreExistente in liNombres:
        if normalizar_string(nombreExistente) == nombreNormalizado:
            print(f"El nombre de equipo ya está registrado.")
            valido = False

    if tag == "":
        print("El tag no puede estar vacío.")
        valido = False

    if " " in tag:
        print("El tag no puede tener espacios en medio.")
        valido = False

    tagNormalizado = normalizar_string(tag)
    if tagNormalizado in liTags:
        print("El tag ya está registrado por otro equipo.")
        valido = False

    if region == "":
        print("La región no puede estar vacía.")
        valido = False

    regionNormalizada = normalizar_string(region)
    if regionNormalizada not in regionesValidas:
        print(f"Región inválida. Las regiones permitidas son: {regionesValidas}.")
        valido = False

    return valido

def validar_suficientes_equipos(LiNombres):
    valido = True
    if len(LiNombres) < 8:
        valido = False
    return valido


#Operaciones
def registrar(liNombres, liTags, liRegiones, liPosiciones, nombre, tag, region):
    """
    Agrega un equipo nuevo a las listas paralelas y una fila en cero a posiciones.
    El id del equipo queda determinado por su posición (índice) en las listas.
    """
    idNuevo = len(liNombres)

    liNombres.append(nombre)
    liTags.append(tag)
    liRegiones.append(region)
    liPosiciones.append([0, 0, 0, 0])  # PJ, PG, PP, puntos

    return idNuevo

def registrar_equipo(liNombres, liTags, liRegiones, liPosiciones):
    """RF04-06: valida antes de registrar un equipo."""
    print("\n--- Registrar equipo ---")
    
    nombre = (input("Nombre del equipo: ")).strip()
    tag = normalizar_string(input("Tag (código corto): "))
    region = normalizar_string(input('Región("NA", "EU", "LATAM", "APAC", "KR", "BR", "OCE"): ' ))

    valido = validar_registro_equipo(liNombres, liTags, nombre, tag, region)
    
    if not valido:
        print("No se registro el equipo.")

    else:
        idEquipo = registrar(liNombres, liTags, liRegiones, liPosiciones, nombre, tag, region)
        print(f"El equipo '{liNombres[idEquipo]}' fue registrado correctamente con el id {idEquipo}.")

def listar_equipos(liNombres, liTags, liRegiones):
    """RF11: arma el listado de equipos registrados para mostrar."""
    if len(liNombres) == 0:
        return "Todavía no hay equipos registrados."

    lineas = []
    for i in range(len(liNombres)):
        linea = f"{i}. {liNombres[i]} [{liTags[i]}] - {liRegiones[i]}"
        lineas.append(linea)

    return "\n".join(lineas)

def jornada_actual(fixture):
    for grupoJornada in range(len(fixture)):
        for partido in fixture[grupoJornada]:
            _, _, jugado = partido
            if jugado == 0:
                return grupoJornada + 1

    return 0  # si no hay ningún 0, ya se jugaron todos los partidos

def partidos_pendientes(fixture, jornada):
    pendientes = []
    for partido in fixture[jornada - 1]:
        idA, idB, jugado = partido
        if jugado == 0:
            pendientes.append(partido)

    return pendientes

def listar_partidos_pendientes(fixture, liNombres):
    jornada = jornada_actual(fixture)

    if jornada == 0:
        print("El torneo ya terminó, no quedan partidos pendientes.")
        return

    print(f"Actualmente se está jugando la jornada N° {jornada}")
    print("Los partidos pendientes son:")

    for partido in partidos_pendientes(fixture, jornada):
        idA, idB, jugado = partido
        print(f"{liNombres[idA]} vs {liNombres[idB]}")

def pedir_puntaje(mensaje):
    puntaje = es_numerico(input(mensaje))
    while puntaje is None:
        print("Error. Debe ingresar un número entero.")
        puntaje = es_numerico(input(mensaje))
    return puntaje

def registrar_resultados(fixture, historial, LiNombres):
    jornada = jornada_actual(fixture)
    partidos = partidos_pendientes(fixture, jornada)
    partido_actual = partidos[0]
    idA, idB, _ = partido_actual
    equipoA = LiNombres[idA]
    equipoB = LiNombres[idB]

    print(f"El partido actual es {equipoA} vs {equipoB}")

    while True:
        puntosA = pedir_puntaje(f"Ingrese la puntuación de {equipoA}: ")
        puntosB = pedir_puntaje(f"Ingrese la puntuación de {equipoB}: ")

        if puntosA == puntosB:
            print("Error. No se permiten empates, los puntajes no pueden ser iguales.")
        else:
            break

    mapa = input("Ingrese el nombre del mapa: ")
    partido_actual[2] = 1
    historial.append([jornada, idA, idB, puntosA, puntosB, mapa])

def consultar_historial(historial, LiNombres):
    """RF12: arma el listado del historial de partidos jugados,
    traduciendo los ids de equipo a nombres."""
    if len(historial) == 0:
        return "Todavía no se jugó ningún partido."

    lineas = []
    for partido in historial:
        jornada, idA, idB, puntosA, puntosB, mapa = partido
        equipoA = LiNombres[idA]
        equipoB = LiNombres[idB]
        linea = f"Jornada {jornada}: {equipoA} {puntosA} - {puntosB} {equipoB} (Mapa: {mapa})"
        lineas.append(linea)

    return "\n".join(lineas)

def generar_ranking(liPosiciones):
    """RF18: genera el orden de los equipos por índice, usando lambda.
    Ordena por puntos de mayor a menor, y en caso de empate por PG (partidos ganados)."""
    indices = list(range(len(liPosiciones)))
    ranking = sorted(indices, key=lambda i: (liPosiciones[i][3], liPosiciones[i][1]), reverse=True)
    return ranking


def tabla_de_posiciones(liNombres, liTags, liRegiones, liPosiciones):
    """RF13/RF22: arma la tabla de posiciones ordenada de mayor a menor puntaje,
    con desempate por PG, para mostrarla como informe."""
    if len(liNombres) == 0:
        return "Todavía no hay equipos registrados."

    ranking = generar_ranking(liPosiciones)

    encabezado = f"{'Pos':<4}{'Equipo':<20}{'Tag':<8}{'Región':<8}{'PJ':<5}{'PG':<5}{'PP':<5}{'Pts':<5}"
    lineas = [encabezado]

    pos = 1
    for i in ranking:
        pj = liPosiciones[i][0]
        pg = liPosiciones[i][1]
        pp = liPosiciones[i][2]
        pts = liPosiciones[i][3]
        linea = f"{pos:<4}{liNombres[i]:<20}{liTags[i]:<8}{liRegiones[i]:<8}{pj:<5}{pg:<5}{pp:<5}{pts:<5}"
        lineas.append(linea)
        pos += 1

    return "\n".join(lineas)

#MENU
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

    operacion = es_numerico(input("Ingrese la operación que desea realizar: "))
    operacion = validacion_de_rango(1, 9, operacion)

    return operacion
