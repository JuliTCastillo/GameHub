from operaciones import *

def main():
    CONFIG_TORNEO = (
        "Copa Buenos Aires 2026",   # nombre del torneo
        "Valorant",                  # juego
        "8 equipos - 7 jornadas - 4 partidos por jornada - todos contra todos"  # formato
    )

    # Tupla de mapas habilitados
    MAPAS = ("Bind", "Haven", "Ascent")

    #Listas paralelas
    nombres  = []
    tags     = []
    regiones = []
    posiciones = []

    # 8 equipos, 4 partidos por jornada, 7 jornadas
    # Fixture fijo: [id_equipoA, id_equipoB, jugado]
    # jugado arranca en 0 (pendiente) y pasa a 1 cuando se carga el resultado.
    fixture = [
    [[0, 7, 0], [1, 6, 0], [2, 5, 0], [3, 4, 0]],
    [[0, 6, 0], [5, 7, 0], [1, 4, 0], [2, 3, 0]],
    [[0, 5, 0], [4, 6, 0], [3, 7, 0], [1, 2, 0]],
    [[0, 4, 0], [3, 5, 0], [2, 6, 0], [1, 7, 0]],
    [[0, 3, 0], [2, 4, 0], [1, 5, 0], [6, 7, 0]],
    [[0, 2, 0], [1, 3, 0], [4, 7, 0], [5, 6, 0]],
    [[0, 1, 0], [2, 7, 0], [3, 6, 0], [4, 5, 0]],
]
    # Cada fila tiene: [jornada, idA, idB, puntosA, puntosB, mapa]
    # mapa ya viene guardado como texto (ej. "Bind"), no hace falta traducirlo
    historial=[]

    valor = menu(CONFIG_TORNEO)
    while valor != 9:
        if valor == 1:
            registrar_equipo(nombres, tags, regiones, posiciones)
        elif valor == 2:
            print(listar_equipos(nombres, tags, regiones))
        elif valor == 3:
            if validar_suficientes_equipos(nombres):
                listar_partidos_pendientes(fixture, nombres)
            else:
                print(f"Todavía no están los 8 equipos registrados (hay {len(nombres)}).")
        elif valor == 4:
            if validar_suficientes_equipos(nombres):
                registrar_resultados(fixture, historial, nombres)
            else:
                print(f"Todavía no están los 8 equipos registrados (hay {len(nombres)}).")
        elif valor == 5:
            print(consultar_historial(historial, nombres))
        elif valor == 6:
            busqueda = input("Ingrese ID o tag del equipo a buscar: ").strip()
            idEquipo = buscar_equipo(nombres, tags, busqueda)
            if idEquipo == -1:
                print("No se encontró ningún equipo con ese ID o tag.")
            else:
              print(mostrar_equipo(nombres, tags, regiones, posiciones, idEquipo))
        elif valor == 7:
            print(tabla_de_posiciones(nombres, tags, regiones, posiciones))
        elif valor == 8:
            #En informe tiene que elegir entre (líder, Top 3, racha máxima, invictos, resumen general)
            print("Informe")
        valor = menu(CONFIG_TORNEO)
main()