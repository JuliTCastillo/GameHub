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
    validar_formato_tag,
    validar_formato_nombre,
    parsear_linea_usuario,
    cargar_usuarios,
    estadisticas_por_region,
    filtrar_equipos_por_region,
    generar_alertas,
    guardar_reporte,
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


# ============================================================
# PRUEBAS DE LAS FUNCIONALIDADES NUEVAS (correcciones Etapa 2)
# ============================================================

# 9. Validación de formato del tag con expresión regular
def test_formato_tag_regex():
    assert validar_formato_tag("SEN") == True
    assert validar_formato_tag("T1") == True
    assert validar_formato_tag("S") == False         # muy corto
    assert validar_formato_tag("ABCDEF") == False    # muy largo
    assert validar_formato_tag("SE!") == False       # carácter no permitido


# 10. Validación de formato del nombre con expresión regular
def test_formato_nombre_regex():
    assert validar_formato_nombre("KRÜ Esports") == True
    assert validar_formato_nombre("Team Liquid") == True
    assert validar_formato_nombre("A") == False                      # muy corto
    assert validar_formato_nombre("Equipo@#") == False               # caracteres no permitidos
    assert validar_formato_nombre("Un nombre demasiado largo") == False


# 11. Validación incorrecta que genera una excepción: línea de usuario sin coma
def test_linea_usuario_invalida_genera_excepcion():
    try:
        parsear_linea_usuario("adminsinclave")
        genero_excepcion = False
    except ValueError:
        genero_excepcion = True

    assert genero_excepcion == True

    # Con el formato correcto no hay excepción y se obtiene la tupla
    assert parsear_linea_usuario("admin,1234\n") == ("admin", "1234")


# 12. Lectura del archivo de usuarios: archivo inexistente y líneas mal formadas
def test_cargar_usuarios():
    # Archivo inexistente: no corta el programa, devuelve None
    assert cargar_usuarios("archivo_que_no_existe.csv") is None

    # Archivo con líneas rotas: se saltean y se cargan las válidas
    with open("usuarios_prueba.csv", "w", encoding="utf-8") as arch:
        arch.write("admin,1234\nlinea_rota\nad min,1234\njuli,abcd\n")

    assert cargar_usuarios("usuarios_prueba.csv") == [("admin", "1234"), ("juli", "abcd")]


# 13. Diccionario acumulador: indicadores agrupados por región
def test_estadisticas_por_region():
    equipos = [
        {"nombre": "Sentinels", "tag": "SEN", "region": "NA",
         "estadisticas": {"PJ": 4, "PG": 4, "PP": 0, "PTS": 12}},
        {"nombre": "Fnatic", "tag": "FNC", "region": "EU",
         "estadisticas": {"PJ": 4, "PG": 1, "PP": 3, "PTS": 3}},
        {"nombre": "NRG", "tag": "NRG", "region": "NA",
         "estadisticas": {"PJ": 4, "PG": 1, "PP": 3, "PTS": 3}},
    ]

    acumulador = estadisticas_por_region(equipos)

    assert acumulador["NA"] == {"equipos": 2, "PJ": 8, "PG": 5, "PP": 3, "PTS": 15}
    assert acumulador["EU"] == {"equipos": 1, "PJ": 4, "PG": 1, "PP": 3, "PTS": 3}


# 14. Reporte filtrado por región y alertas
def test_filtro_por_region_y_alertas():
    equipos = [
        {"nombre": "Sentinels", "tag": "SEN", "region": "NA",
         "estadisticas": {"PJ": 1, "PG": 1, "PP": 0, "PTS": 3}},
        {"nombre": "Fnatic", "tag": "FNC", "region": "EU",
         "estadisticas": {"PJ": 1, "PG": 0, "PP": 1, "PTS": 0}},
    ]
    fixture = [[1, 0, 1, 13, 5, 1, 0]]

    assert filtrar_equipos_por_region(equipos, "na") == [0]
    assert filtrar_equipos_por_region(equipos, "KR") == []

    alertas = generar_alertas(equipos, fixture)
    assert "El torneo finalizó: no quedan partidos pendientes." in alertas
    assert "Sentinels está invicto (1 victorias)." in alertas


# 15. Generación del archivo de texto con el reporte
def test_guardar_reporte():
    assert guardar_reporte("reporte_prueba.txt", "REPORTE DE PRUEBA", "Contenido del reporte") == True

    with open("reporte_prueba.txt", "r", encoding="utf-8") as arch:
        contenido = arch.read()

    assert "REPORTE DE PRUEBA" in contenido
    assert "Contenido del reporte" in contenido