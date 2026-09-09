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

def normalizar_tag(tag):
    """RF05: normaliza el tag a mayúsculas y sin espacios."""
    return tag.strip().upper().replace(" ", "")

def validar_registro_equipo(liNombres, nombre, tag, liTags, region):
    if len(liNombres) >= 8:
        return False, "Ya se alcanzó el máximo de 8 equipos."

    if nombre.strip() == "":
        return False, "El nombre del equipo no puede estar vacío."

    tagNormalizado = normalizar_tag(tag)

    if tagNormalizado == "":
        return False, "El tag no puede estar vacío."

    if tagNormalizado in liTags:
        return False, f"El tag '{tagNormalizado}' ya está registrado por otro equipo."

    if region.strip() == "":
            return False, "La region no puede estar vacío."
    
    return True, ""

#Operaciones
def registrar(liNombres, liTags, liRegiones, liPosiciones, nombre, tag, region):
    """
    Agrega un equipo nuevo a las listas paralelas y una fila en cero a posiciones.
    El id del equipo queda determinado por su posición (índice) en las listas.
    """
    idNuevo = len(liNombres)

    liNombres.append(nombre.strip())
    liTags.append(normalizar_tag(tag))
    liRegiones.append(region.strip().upper())
    liPosiciones.append([0, 0, 0, 0])  # PJ, PG, PP, puntos

    return idNuevo

def registrar_equipo(liNombres, liTags, liRegiones, liPosiciones):
    """RF04-06: valida antes de registrar un equipo."""
    print("\n--- Registrar equipo ---")
    
    nombre = input("Nombre del equipo: ")
    tag = input("Tag (código corto): ")
    region = input("Región (ej. NA, EU, LATAM): ")

    valido, mensaje = validar_registro_equipo(liNombres, nombre, tag, liTags, region)

    if not valido:
        print(f"Error: {mensaje}")
        return

    idEquipo = registrar(liNombres, liTags, liRegiones, liPosiciones, nombre, tag, region)
    print(f"Equipo '{liNombres[idEquipo]}' registrado con id {idEquipo}.")

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
