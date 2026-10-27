import os
from operaciones import *


def main():
    # RUTAS
    # Se arman a partir de la carpeta donde está main.py (os.path, autorizado por la profe),
    # así el programa encuentra sus archivos aunque se ejecute desde otra carpeta
    # y sin importar si la carpeta se llama GameHub, GameHub-main, etc.
    CARPETA = os.path.dirname(os.path.abspath(__file__))

    ARCH_USUARIOS = os.path.join(CARPETA, "info_usuarios.csv")
    ARCH_CONFIG = os.path.join(CARPETA, "config_torneo.json")
    ARCH_EQUIPOS = os.path.join(CARPETA, "equipos.json")
    ARCH_PARTIDOS = os.path.join(CARPETA, "partidos.json")
    ARCH_REPORTES = os.path.join(CARPETA, "reportes.txt")

    # LOGIN
    USUARIOS = cargar_usuarios(ARCH_USUARIOS)

    if USUARIOS is None:
        print("No se puede iniciar sesión sin un archivo de usuarios válido.")
        return

    acceso = False
    intentos = 0

    while not acceso and intentos < 3:
        if login_valido(USUARIOS):
            acceso = True
        else:
            print("Usuario o contraseña incorrectos. Verificá los datos ingresados e intentá nuevamente.")
            print()
            intentos += 1

    if not acceso:
        print("Demasiados intentos fallidos. Saliendo..")
        print()
        return

    print("Inicio de sesión exitoso.")
    print()

    # CONFIGURACION
    CONFIG = cargar_configuracion(ARCH_CONFIG)

    if CONFIG is None or not validar_configuracion(CONFIG):
        print("No se puede iniciar el programa sin una configuración válida.")
        return

    CANT_EQUIPOS = CONFIG["torneo"]["cantidad_equipos"]
    INFO_TORNEO = (
        CONFIG["torneo"]["nombre"],
        CONFIG["torneo"]["juego"],
        f"{CANT_EQUIPOS} equipos - todos contra todos")
    REGIONES_VALIDAS = CONFIG["regiones_validas"]
    MAPAS = CONFIG["mapas"]
    REGLAS = CONFIG["reglas"]

    # REGISTROS
    EQUIPOS = cargar_datos(ARCH_EQUIPOS, [])
    FIXTURE = cargar_datos(ARCH_PARTIDOS, [])

    if EQUIPOS is None or FIXTURE is None:
        print("No se puede iniciar el programa con archivos de datos dañados.")
        return

    if not validar_formato_equipos(EQUIPOS, CANT_EQUIPOS, REGIONES_VALIDAS):
        print("El archivo de equipos tiene un formato incorrecto. "
              "Corríjalo o bórrelo para reiniciar el torneo.")
        return

    # PROGRAMA
    while not validar_suficientes_equipos(EQUIPOS, CANT_EQUIPOS):
        print(f"Cantidad actual de equipos {len(EQUIPOS)} / {CANT_EQUIPOS}")
        registrar_equipo(EQUIPOS, REGIONES_VALIDAS)
    guardar_datos(ARCH_EQUIPOS, EQUIPOS)
    print("Se ha completado el registro de equipos")

    if len(FIXTURE) == 0:
        FIXTURE = generar_partidos(CANT_EQUIPOS, MAPAS)
        guardar_fixture(ARCH_PARTIDOS, FIXTURE)

    elif (not validar_fixture(FIXTURE, CANT_EQUIPOS, len(MAPAS), REGLAS)
          or not validar_estadisticas(EQUIPOS, FIXTURE, CANT_EQUIPOS)):
        print("Los archivos de datos no son consistentes con la configuración. "
              "Corríjalos o bórrelos para reiniciar el torneo.")
        return

    valor = menu(INFO_TORNEO)

    while valor != 8:
        jornada = jornada_actual(FIXTURE)
        if valor == 1:
            print(listar_equipos(EQUIPOS))

        if valor == 2:
            buscar_y_mostrar_equipo(EQUIPOS)

        if valor == 3:
            if jornada != 0:
                listar_partidos_pendientes(jornada, FIXTURE, EQUIPOS)
            else:
                print("El torneo ya terminó, no quedan partidos pendientes.")

        if valor == 4:
            if jornada != 0:
                registrar_resultados(jornada, FIXTURE, EQUIPOS, REGLAS)
                guardar_fixture(ARCH_PARTIDOS, FIXTURE)
                guardar_datos(ARCH_EQUIPOS, EQUIPOS)
            else:
                print("El torneo ya terminó, no quedan partidos a los que cargarle resultados.")

        if valor == 5:
            historial = consultar_historial(FIXTURE, EQUIPOS, MAPAS)
            if historial == "":
                print("Todavía no se jugó ningún partido.")
            else:
                print(historial)

        if valor == 6:
            print(tabla_de_posiciones(EQUIPOS))

        if valor == 7:
            opcion_informe = menu_informes()

            while opcion_informe != 9:
                if opcion_informe == 1:
                    print(informe_lideres(EQUIPOS))

                if opcion_informe == 2:
                    print(informe_top3(EQUIPOS))

                if opcion_informe == 3:
                    print(informe_racha(EQUIPOS, FIXTURE))

                if opcion_informe == 4:
                    print(informe_invictos(EQUIPOS))

                if opcion_informe == 5:
                    print(resumen_general(EQUIPOS, FIXTURE))

                if opcion_informe == 6:
                    print(informe_por_region(EQUIPOS))

                if opcion_informe == 7:
                    region = normalizar_string(
                        input(f"Región a filtrar ({', '.join(REGIONES_VALIDAS)}): "))

                    if region not in REGIONES_VALIDAS:
                        print("Región inválida.")
                    else:
                        reporte = reporte_filtrado_region(EQUIPOS, region)
                        print(reporte)
                        if guardar_reporte(ARCH_REPORTES, f"REPORTE FILTRADO - REGIÓN {region}", reporte):
                            print("El reporte se guardó en 'reportes.txt'.")

                if opcion_informe == 8:
                    reporte = reporte_completo(EQUIPOS, FIXTURE)
                    print(reporte)
                    if guardar_reporte(ARCH_REPORTES, "REPORTE GENERAL Y ALERTAS", reporte):
                        print("El reporte se guardó en 'reportes.txt'.")

                opcion_informe = menu_informes()

        valor = menu(INFO_TORNEO)
    print("Saliendo..")


main()