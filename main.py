from operaciones import *

def main():
    CONFIG_TORNEO = (
        "Copa Buenos Aires 2026",   # nombre del torneo
        "Valorant",                  # juego
        "8 equipos - 7 jornadas - 4 partidos por jornada - todos contra todos"  # formato
    )

    # Tupla de mapas habilitados
    MAPAS = ("Bind", "Haven", "Ascent")
    """
    #Listas paralelas
    nombres  = []
    tags     = []
    regiones = []
    posiciones = []
    """

    # Listas paralelas
    nombres  = ["Sentinels", "Loud", "Fnatic", "NRG", "Paper Rex", "DRX", "KRÜ Esports", "Team Liquid"]
    tags     = ["SEN", "LOUD", "FNC", "NRG", "PRX", "DRX", "KRU", "TL"]
    regiones = ["NA", "BR", "EU", "NA", "APAC", "KR", "LATAM", "EU"]

    # Matriz de posiciones (arranca en cero para los 8 equipos, misma cantidad de filas que equipos)
    posiciones = [
        [3, 3, 0, 9],  # id 0 - Sentinels (invicto, líder)
        [3, 2, 1, 6],  # id 1 - Loud
        [3, 1, 2, 3],  # id 2 - Fnatic
        [3, 2, 1, 6],  # id 3 - NRG
        [3, 2, 1, 6],  # id 4 - Paper Rex
        [3, 2, 1, 6],  # id 5 - DRX
        [3, 0, 3, 0],  # id 6 - KRÜ Esports
        [3, 0, 3, 0],  # id 7 - Team Liquid
    ]

    # 8 equipos, 4 partidos por jornada, 7 jornadas
    # Fixture fijo: [id_equipoA, id_equipoB, jugado]
    # jugado arranca en 0 (pendiente) y pasa a 1 cuando se carga el resultado.
    fixture = [
        [[0, 7, 1], [1, 6, 1], [2, 5, 1], [3, 4, 1]],  # jornada 1 - jugada
        [[0, 6, 1], [5, 7, 1], [1, 4, 1], [2, 3, 1]],  # jornada 2 - jugada
        [[0, 5, 1], [4, 6, 1], [3, 7, 1], [1, 2, 1]],  # jornada 3 - jugada
        [[0, 4, 0], [3, 5, 0], [2, 6, 0], [1, 7, 0]],  # jornada 4 - pendiente
        [[0, 3, 0], [2, 4, 0], [1, 5, 0], [6, 7, 0]],  # jornada 5 - pendiente
        [[0, 2, 0], [1, 3, 0], [4, 7, 0], [5, 6, 0]],  # jornada 6 - pendiente
        [[0, 1, 0], [2, 7, 0], [3, 6, 0], [4, 5, 0]],  # jornada 7 - pendiente
    ]   
    # Cada fila tiene: [jornada, idA, idB, puntosA, puntosB, mapa]
    # mapa ya viene guardado como texto (ej. "Bind"), no hace falta traducirlo
    #historial=[]

    historial = [
        [1, 0, 7, 13, 5,  "BIND"],
        [1, 1, 6, 13, 9,  "HAVEN"],
        [1, 2, 5, 7,  13, "ASCENT"],
        [1, 3, 4, 13, 10, "BIND"],
        [2, 0, 6, 13, 2,  "HAVEN"],
        [2, 5, 7, 13, 6,  "ASCENT"],
        [2, 1, 4, 8,  13, "BIND"],
        [2, 2, 3, 13, 11, "HAVEN"],
        [3, 0, 5, 13, 8,  "ASCENT"],
        [3, 4, 6, 13, 7,  "BIND"],
        [3, 3, 7, 13, 9,  "HAVEN"],
        [3, 1, 2, 13, 10, "ASCENT"],
    ]

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
                registrar_resultados(fixture, historial, posiciones, nombres,MAPAS)
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
            opcionInforme = menu_informes()
            while opcionInforme != 6:
                if opcionInforme == 1:
                    print(informe_lideres(nombres, posiciones))
                elif opcionInforme == 2:
                    print(informe_top3(nombres, tags, posiciones))
                elif opcionInforme == 3:
                    print(informe_racha(nombres, historial, len(nombres)))
                elif opcionInforme == 4:
                    print(informe_invictos(nombres, posiciones))
                elif opcionInforme == 5:
                    print(resumen_general(nombres, posiciones, historial))
                opcionInforme = menu_informes()
        valor = menu(CONFIG_TORNEO)
main()