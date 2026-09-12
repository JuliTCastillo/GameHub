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

def registrar_resultados(fixture, historial, LiNombres):
    jornada = jornada_actual(fixture)
    partidos = partidos_pendientes(fixture,jornada)
    idA, idB, jugado = partidos[0]
    equipoA = LiNombres[idA]
    equipoB = LiNombres[idB]
    print(f"El partido actual es {equipoA} vs {equipoB}")
    puntosA = int(input(f"Ingrese la puntuacion de {equipoA}: "))
    puntosB = int(input(f"Ingrese la puntuacion del {equipoB}: "))
    mapa = input("Ingrese el nombre del mapa: ")
    jugado = 1
    historial.append([jornada, idA, idB, puntosA, puntosB, mapa])

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
    operacion = validacion_de_rango(1, 8, operacion)

    return operacion
