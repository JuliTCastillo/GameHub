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

#MENU
def menu(info):
    print(f"""
----> {info[0]} - {info[1]} <----
1. Registrar equipo
2. Listar equipos
3. Ver partidos pendientes / cargar resultado
4. Consultar historial
5. Buscar equipo
6. Tabla de posiciones
7. Informes 
8. Salir
    """)

    operacion = es_numerico(input("Ingrese la operación que desea realizar: "))
    operacion = validacion_de_rango(1, 8, operacion)

    return operacion
