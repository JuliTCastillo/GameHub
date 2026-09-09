#Validaciones
def validacionDeRango(min, max, valor):
    try:
        while valor < min or valor > max:
            print(f"Error. Ingrese un valor tiene que estar entre {min} a {max}")
            valor = esNumerico(input("Ingrese la operación que desea realizar: "))

        return valor
    except TypeError:
        print(f"ERROR. El valor ingresado no es numerico")

def esNumerico(valor):
    if valor.isdigit():
        return int(valor)

def normalizar_tag(tag):
    """RF05: normaliza el tag a mayúsculas y sin espacios."""
    return tag.strip().upper().replace(" ", "")

def validarRegistroEquipo(nombres, nombre, tag, tags, region):
    if len(nombres) >= 8:
        return False, "Ya se alcanzó el máximo de 8 equipos."

    if nombre.strip() == "":
        return False, "El nombre del equipo no puede estar vacío."

    tag_normalizado = normalizar_tag(tag)

    if tag_normalizado == "":
        return False, "El tag no puede estar vacío."

    if tag_normalizado in tags:
        return False, f"El tag '{tag_normalizado}' ya está registrado por otro equipo."

    if region.strip() == "":
            return False, "La region no puede estar vacío."
    
    return True, ""

#Operaciones
def registrar(liNombres, liTags, liRegiones, liPosiciones, nombre, tag, region):
    """
    Agrega un equipo nuevo a las listas paralelas y una fila en cero a posiciones.
    El id del equipo queda determinado por su posición (índice) en las listas.
    """
    id_nuevo = len(liNombres)

    liNombres.append(nombre.strip())
    liTags.append(normalizar_tag(tag))
    liRegiones.append(region.strip().upper())
    liPosiciones.append([0, 0, 0, 0])  # PJ, PG, PP, puntos

    return id_nuevo

def registrarEquipo(liNombres, liTags, liRegiones, liPosiciones):
    """RF04-06: valida antes de registrar un equipo."""
    print("\n--- Registrar equipo ---")
    
    nombre = input("Nombre del equipo: ")
    tag = input("Tag (código corto): ")
    region = input("Región (ej. NA, EU, LATAM): ")

    valido, mensaje = validarRegistroEquipo(liNombres, nombre, tag, liTags, region)

    if not valido:
        print(f"Error: {mensaje}")
        return

    id_equipo = registrar(liNombres, liTags, liRegiones, liPosiciones, nombre, tag, region)
    print(f"Equipo '{liNombres[id_equipo]}' registrado con id {id_equipo}.")

def listar_equipos(nombres, tags, regiones):
    """RF11: arma el listado de equipos registrados para mostrar."""
    if len(nombres) == 0:
        return "Todavía no hay equipos registrados."

    lineas = []
    for i in range(len(nombres)):
        linea = f"{i}. {nombres[i]} [{tags[i]}] - {regiones[i]}"
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

    operacion = esNumerico(input("Ingrese la operación que desea realizar: "))
    operacion = validacionDeRango(1, 8,operacion)

    return operacion
