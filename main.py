import operaciones as op

def main():
    CONFIG_TORNEO = (
        "Copa Buenos Aires 2026",   # nombre del torneo
        "Valorant",                  # juego
        "8 equipos - 7 jornadas - 4 partidos por jornada - todos contra todos"  # formato
    )

    # Tupla de mapas habilitados
    MAPAS = ("Bind", "Haven", "Ascent")

    # 8 equipos, 4 partidos por jornada, 7 jornadas
    # Fixture fijo: [jornada, id_equipoA, id_equipoB, jugado]
    # jugado arranca en 0 (pendiente) y pasa a 1 cuando se carga el resultado.
    fixture = [
        [1, 0, 7, 0], [1, 1, 6, 0], [1, 2, 5, 0], [1, 3, 4, 0],
        [2, 0, 6, 0], [2, 5, 7, 0], [2, 1, 4, 0], [2, 2, 3, 0],
        [3, 0, 5, 0], [3, 4, 6, 0], [3, 3, 7, 0], [3, 1, 2, 0],
        [4, 0, 4, 0], [4, 3, 5, 0], [4, 2, 6, 0], [4, 1, 7, 0],
        [5, 0, 3, 0], [5, 2, 4, 0], [5, 1, 5, 0], [5, 6, 7, 0],
        [6, 0, 2, 0], [6, 1, 3, 0], [6, 4, 7, 0], [6, 5, 6, 0],
        [7, 0, 1, 0], [7, 2, 7, 0], [7, 3, 6, 0], [7, 4, 5, 0],
    ]

    valor = op.menu(CONFIG_TORNEO)
    while valor != 8:
        op.operaciones(valor)
        valor = op.menu(CONFIG_TORNEO)
main()