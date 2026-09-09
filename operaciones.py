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

#Operaciones
def registrarEquipo():
    print("Registro")        

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

def operaciones(valor):
    if valor == 1:
        print("Registrar equipo")
    elif valor == 2:
        print("Listar equipo")
    elif valor == 3:
        print("Ver partidos pendientes/cargar resultado")
    elif valor == 4:
        print("Consultar historial")
    elif valor == 5:
        print("Buscar equipo")
    elif valor == 6:
        print("Tabla de posiciones")
    elif valor == 7:
        #En informe tiene que elegir entre (líder, Top 3, racha máxima, invictos, resumen general)
        print("Informe")