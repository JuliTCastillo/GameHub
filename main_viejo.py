from operaciones_viejo import *

def main():
    CONFIG_TORNEO = (
        "Copa Buenos Aires 2026",   # nombre del torneo
        "Valorant",                  # juego
        "8 equipos - 7 jornadas - 4 partidos por jornada - todos contra todos"  # formato
    )

    # Tupla de mapas habilitados
    MAPAS = ("Bind", "Haven", "Ascent")



    #Lista de diccionarios
    equipos = [
    {"nombre": "Sentinels", "tag": "SEN", "region": "NA"},
    {"nombre": "Loud", "tag": "LOUD", "region": "BR"},
    {"nombre": "Fnatic", "tag": "FNC", "region": "EU"},
    {"nombre": "NRG", "tag": "NRG", "region": "NA"},
    {"nombre": "Paper Rex", "tag": "PRX", "region": "APAC"},
    {"nombre": "DRX", "tag": "DRX", "region": "KR"},
    {"nombre": "KRÜ Esports", "tag": "KRU", "region": "LATAM"},
    {"nombre": "Team Liquid", "tag": "TL", "region": "EU"}
    ]


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
        [[0, 7, 0], [1, 6, 0], [2, 5, 0], [3, 4, 0]],  # jornada 1 - jugada
        [[0, 6, 0], [5, 7, 0], [1, 4, 0], [2, 3, 0]],  # jornada 2 - jugada
        [[0, 5, 0], [4, 6, 0], [3, 7, 0], [1, 2, 0]],  # jornada 3 - jugada
        [[0, 4, 0], [3, 5, 0], [2, 6, 0], [1, 7, 0]],  # jornada 4 - pendiente
        [[0, 3, 0], [2, 4, 0], [1, 5, 0], [6, 7, 0]],  # jornada 5 - pendiente
        [[0, 2, 0], [1, 3, 0], [4, 7, 0], [5, 6, 0]],  # jornada 6 - pendiente
        [[0, 1, 0], [2, 7, 0], [3, 6, 0], [4, 5, 0]],  # jornada 7 - pendiente
    ]


    # Cada fila tiene: [jornada, idA, idB, puntosA, puntosB, mapa]
    # mapa ya viene guardado como texto (ej. "Bind"), no hace falta traducirlo
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
            if validar_suficientes_equipos(equipos):
                print("Ya se alcanzo el maximo de 8 equipos.")
            else:
                registrar_equipo(equipos, posiciones)

        elif valor == 2:
            print(listar_equipos(equipos))

        elif valor == 3:
            if validar_suficientes_equipos(equipos):
                if validar_partidos_pendientes(fixture):
                    listar_partidos_pendientes(fixture, equipos)
                else:
                    print("El torneo ya terminó, no quedan partidos pendientes.")
            else:
                print(
                    f"Todavía no están los 8 equipos registrados "
                    f"(hay {len(equipos)})."
                )

        elif valor == 4:
            if validar_suficientes_equipos(equipos):
                if validar_partidos_pendientes(fixture):
                    registrar_resultados(
                        fixture, historial, posiciones, equipos, MAPAS
                    )
                else:
                    print(
                        "El torneo ya terminó, no quedan partidos "
                        "a los que cargarle resultados."
                    )
            else:
                print(
                    f"Todavía no están los 8 equipos registrados "
                    f"(hay {len(equipos)})."
                )

        elif valor == 5:
            print(consultar_historial(historial, equipos))

        elif valor == 6:
            busqueda = input("Ingrese ID o tag del equipo a buscar: ").strip()
            idEquipo = buscar_equipo(equipos, busqueda)

            if idEquipo == -1:
                print("No se encontró ningún equipo con ese ID o tag.")
            else:
                print(mostrar_equipo(equipos, posiciones, idEquipo))

        elif valor == 7:
            print(tabla_de_posiciones(equipos, posiciones))

        elif valor == 8:
            # En informe tiene que elegir entre:
            # líder, Top 3, racha máxima, invictos, resumen general.
            opcionInforme = menu_informes()

            while opcionInforme != 6:
                if opcionInforme == 1:
                    print(informe_lideres(equipos, posiciones))

                elif opcionInforme == 2:
                    print(informe_top3(equipos, posiciones))

                elif opcionInforme == 3:
                    print(informe_racha(equipos, historial, len(equipos)))

                elif opcionInforme == 4:
                    print(informe_invictos(equipos, posiciones))

                elif opcionInforme == 5:
                    print(resumen_general(equipos, posiciones, historial))

                opcionInforme = menu_informes()

        valor = menu(CONFIG_TORNEO)

main()