from operaciones import (
    normalizar_string,
    validar_resultado,
    validar_registro_equipo,
    validar_suficientes_equipos,
    actualizar_estadisticas,
    generar_ranking,
    detectar_lideres,
    equipos_invictos,
    jornada_actual,
)


# 1. Validación correcta de un resultado de partido
def test_validar_resultado_correcto():
    reglas = {
        "puntos_para_ganar": 13,
        "diferencia_minima": 2,
        "permite_overtime": True,
    }
    assert validar_resultado(13, 8, reglas) == True


# 2. Validación incorrecta cuando no se cumple la diferencia mínima
def test_validar_resultado_incorrecto():
    reglas = {
        "puntos_para_ganar": 13,
        "diferencia_minima": 2,
        "permite_overtime": True,
    }
    assert validar_resultado(13, 12, reglas) == False


# 3. Validación de registro de equipo (rechazo por tag repetido y aceptación de equipo válido)
def test_validar_registro_equipo():
    equipos = [
        {
            "nombre": "Sentinels",
            "tag": "SEN",
            "region": "NA",
            "estadisticas": {"PJ": 0, "PG": 0, "PP": 0, "PTS": 0},
        }
    ]
    regiones_validas = ["NA", "EU", "LATAM", "BR"]

    assert validar_registro_equipo(equipos, "Fnatic", "SEN", "EU", regiones_validas) == False
    assert validar_registro_equipo(equipos, "Fnatic", "FNC", "EU", regiones_validas) == True


# 4. Operación simple con resultado conocido (normalización de texto)
def test_normalizar_string():
    assert normalizar_string("  krü esports ") == "KRÜESPORTS"


# 5. Acumulación por clave en las estadísticas de los equipos tras un partido
def test_actualizar_estadisticas():
    equipos = [
        {
            "nombre": "Sentinels",
            "tag": "SEN",
            "region": "NA",
            "estadisticas": {"PJ": 1, "PG": 1, "PP": 0, "PTS": 3},
        },
        {
            "nombre": "KRÜ Esports",
            "tag": "KRU",
            "region": "LATAM",
            "estadisticas": {"PJ": 1, "PG": 0, "PP": 1, "PTS": 0},
        },
    ]

    actualizar_estadisticas(equipos, 0, 1, 13, 9)

    assert equipos[0]["estadisticas"] == {"PJ": 2, "PG": 2, "PP": 0, "PTS": 6}
    assert equipos[1]["estadisticas"] == {"PJ": 2, "PG": 0, "PP": 2, "PTS": 0}


# 6. Cálculo de ranking con criterio de desempate por partidos ganados (PG)
def test_generar_ranking_con_desempate():
    equipos = [
        {
            "nombre": "Equipo A",
            "tag": "EQA",
            "region": "NA",
            "estadisticas": {"PJ": 3, "PG": 1, "PP": 2, "PTS": 6},
        },
        {
            "nombre": "Equipo B",
            "tag": "EQB",
            "region": "EU",
            "estadisticas": {"PJ": 3, "PG": 2, "PP": 1, "PTS": 6},
        },
        {
            "nombre": "Equipo C",
            "tag": "EQC",
            "region": "BR",
            "estadisticas": {"PJ": 3, "PG": 3, "PP": 0, "PTS": 9},
        },
    ]

    assert generar_ranking(equipos) == [2, 1, 0]


# 7. Detección de condiciones críticas: líderes empatados y fin del torneo
def test_deteccion_lideres_y_fin_de_torneo():
    equipos = [
        {
            "nombre": "Sentinels",
            "tag": "SEN",
            "region": "NA",
            "estadisticas": {"PJ": 4, "PG": 3, "PP": 1, "PTS": 9},
        },
        {
            "nombre": "Loud",
            "tag": "LOUD",
            "region": "BR",
            "estadisticas": {"PJ": 4, "PG": 3, "PP": 1, "PTS": 9},
        },
        {
            "nombre": "Fnatic",
            "tag": "FNC",
            "region": "EU",
            "estadisticas": {"PJ": 4, "PG": 1, "PP": 3, "PTS": 3},
        },
    ]
    fixture_terminado = [
        [1, 0, 1, 13, 10, 1, 0],
        [2, 1, 2, 13, 7, 1, 1],
    ]

    assert detectar_lideres(equipos) == [0, 1]
    assert jornada_actual(fixture_terminado) == 0


# 8. Casos límite: colección vacía y valores exactamente en el límite permitido
def test_casos_limite():
    reglas = {
        "puntos_para_ganar": 13,
        "diferencia_minima": 2,
        "permite_overtime": True,
    }
    equipos = [{"nombre": "A"}, {"nombre": "B"}]

    # Colección vacía
    assert equipos_invictos([]) == []
    # Cantidad de equipos exactamente igual al límite requerido (2)
    assert validar_suficientes_equipos(equipos, 2) == True
    # Resultado con el puntaje exacto para ganar (13) y diferencia mínima exacta (2 -> 13 a 11)
    assert validar_resultado(13, 11, reglas) == True