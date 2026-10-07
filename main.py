from operaciones import *

def main():
    # CONFIGURACION PREVIA
    INFO_TORNEO = (
        "Copa Buenos Aires 2026",   # nombre del torneo
        "Valorant",                  # juego
        "8 equipos - 7 jornadas - 4 partidos por jornada - todos contra todos"  # formato
    )
    cantidad_equipos = 8

    MAPAS = ("Bind", "Haven", "Ascent")

    # REGISTROS
    # En caso de ser definidios previamente el programa no los reescribira, en cambio si estan vacios si.

    # Lista de diccionarios con los 8 equipos ya registrados y sus estadísticas integradas
    equipos = [
        {
            "nombre": "Sentinels", "tag": "SEN", "region": "NA",
            "estadisticas": {"PJ": 7, "PG": 7, "PP": 0, "PTS": 21}
        },
        {
            "nombre": "Loud", "tag": "LOUD", "region": "BR",
            "estadisticas": {"PJ": 7, "PG": 3, "PP": 4, "PTS": 9}
        },
        {
            "nombre": "Fnatic", "tag": "FNC", "region": "EU",
            "estadisticas": {"PJ": 7, "PG": 1, "PP": 6, "PTS": 3}
        },
        {
            "nombre": "NRG", "tag": "NRG", "region": "NA",
            "estadisticas": {"PJ": 7, "PG": 4, "PP": 3, "PTS": 12}
        },
        {
            "nombre": "Paper Rex", "tag": "PRX", "region": "APAC",
            "estadisticas": {"PJ": 7, "PG": 2, "PP": 5, "PTS": 6}
        },
        {
            "nombre": "DRX", "tag": "DRX", "region": "KR",
            "estadisticas": {"PJ": 7, "PG": 4, "PP": 3, "PTS": 12}
        },
        {
            "nombre": "KRÜ Esports", "tag": "KRU", "region": "LATAM",
            "estadisticas": {"PJ": 7, "PG": 2, "PP": 5, "PTS": 6}
        },
        {
            "nombre": "Team Liquid", "tag": "TL", "region": "EU",
            "estadisticas": {"PJ": 7, "PG": 5, "PP": 2, "PTS": 15}
        }
    ]

    # Lista unificada de fixture e historial
    # Formato: [jornada, idA, idB, puntosA, puntosB, jugado, mapa_id]
    partidos = [
        # Jornada 1
        [1, 0, 7, 13, 5, 1, 0],
        [1, 1, 6, 13, 9, 1, 1],
        [1, 2, 5, 7, 13, 1, 2],
        [1, 3, 4, 13, 10, 1, 0],
        
        # Jornada 2
        [2, 0, 6, 13, 2, 1, 1],
        [2, 7, 5, 13, 6, 1, 2],
        [2, 1, 4, 8, 13, 1, 0],
        [2, 2, 3, 13, 11, 1, 1],
        
        # Jornada 3
        [3, 0, 5, 13, 8, 1, 2],
        [3, 6, 4, 13, 7, 1, 0],
        [3, 7, 3, 13, 9, 1, 1],
        [3, 1, 2, 13, 10, 1, 2],
        
        # Jornada 4
        [4, 0, 4, 13, 11, 1, 0],
        [4, 5, 3, 9, 13, 1, 1],
        [4, 6, 2, 13, 5, 1, 2],
        [4, 7, 1, 10, 13, 1, 0],
        
        # Jornada 5
        [5, 0, 3, 13, 6, 1, 1],
        [5, 4, 2, 13, 1, 1, 2],
        [5, 5, 1, 13, 11, 1, 0],
        [5, 6, 7, 8, 13, 1, 1],
        
        # Jornada 6
        [6, 0, 2, 13, 4, 1, 2],
        [6, 3, 1, 13, 10, 1, 0],
        [6, 4, 7, 7, 13, 1, 1],
        [6, 5, 6, 13, 11, 1, 2],
        
        # Jornada 7
        [7, 0, 1, 13, 9, 1, 0],
        [7, 2, 7, 5, 13, 1, 1],
        [7, 3, 6, 13, 8, 1, 2],
        [7, 4, 5, 10, 13, 1, 0]
    ]

    # PROGRAMA
    while not validar_suficientes_equipos(equipos, cantidad_equipos):
        print(f"Cantidad actual de equipos {len(equipos)} / {cantidad_equipos}")
        registrar_equipo(equipos)

    print("Se ha completado el registro de equipos")

    if len(partidos) == 0:
        partidos = generar_partidos(cantidad_equipos, MAPAS)
    
    valor = menu(INFO_TORNEO)
    
    while valor != 8:
        jornada = jornada_actual(partidos)
        if valor == 1:
            print(listar_equipos(equipos))

        if valor == 2:
            buscar_y_mostrar_equipo(equipos)

        if valor == 3:
            if jornada != 0:
                listar_partidos_pendientes(jornada, partidos, equipos)
            else:
                print("El torneo ya terminó, no quedan partidos pendientes.")

        if valor == 4:
            if jornada != 0:
                registrar_resultados(jornada, partidos, equipos)
            else:
                print("El torneo ya terminó, no quedan partidos a los que cargarle resultados.")

        if valor == 5:
            historial = consultar_historial(partidos, equipos, MAPAS)
            if historial == "":
                print("Todavía no se jugó ningún partido.")
            else:
                print(historial)

        if valor == 6:
            print(tabla_de_posiciones(equipos))

        if valor == 7:
            opcion_informe = menu_informes()

            while opcion_informe != 6:
                if opcion_informe == 1:
                    print(informe_lideres(equipos))

                if opcion_informe == 2:
                    print(informe_top3(equipos))

                if opcion_informe == 3:
                    print(informe_racha(equipos, partidos))

                if opcion_informe == 4:
                    print(informe_invictos(equipos))

                if opcion_informe == 5:
                    print(resumen_general(equipos, partidos))

                opcion_informe = menu_informes()

        valor = menu(INFO_TORNEO)
    print("Saliendo..")
main()
