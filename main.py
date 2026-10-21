from operaciones import *

def main():
    # LOGIN
    acceso = False
    intentos = 0

    while not acceso and intentos < 3:
        if login_valido("GameHub/info_usuarios.csv"):
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
    CONFIG = cargar_configuracion("GameHub/config_torneo.json")

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
    ARCH_EQUIPOS = "GameHub/equipos.json"
    ARCH_PARTIDOS = "GameHub/partidos.json"

    EQUIPOS = cargar_datos(ARCH_EQUIPOS, [])
    FIXTURE = cargar_datos(ARCH_PARTIDOS, [])

    if EQUIPOS is None or FIXTURE is None:
        print("No se puede iniciar el programa con archivos de datos dañados.")
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

            while opcion_informe != 6:
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

                opcion_informe = menu_informes()

        valor = menu(INFO_TORNEO)
    print("Saliendo..")
main()
