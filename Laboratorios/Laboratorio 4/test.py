import os
import servidor_concurrente as servidor


# Marcar tests
def check(nombre, condicion):
    if condicion:
        print(f"[OK]   {nombre}")
    else:
        print(f"[FAIL] {nombre}")


# Limpiar archivos antes de cada test
def limpiar_archivos(bd):
    """Borra el contenido de los archivos del servidor antes de cada test."""
    for archivo in [
        bd.arch_integrales,
        bd.arch_derivadas,
        bd.arch_tesis,
        bd.arch_largo
    ]:
        with open(archivo, "w"):
            pass


# 1) Prueba general ===========================================
def test_end_to_end():
    bd = servidor.BaseDeDatos(max_hilos=3)
    limpiar_archivos(bd)

    tareas = [
        "integral: x**2",
        "derivada: sin(x)",
        "tesis: T1; hola mundo prueba"
    ]
    servidor.procesar_tareas(bd, tareas)

    check("Archivo integrales existe", os.path.exists(bd.arch_integrales))
    check("Archivo derivadas existe", os.path.exists(bd.arch_derivadas))
    check("Archivo tesis existe", os.path.exists(bd.arch_tesis))
    check("Archivo largo existe", os.path.exists(bd.arch_largo))


# 2) Test integral simple =====================================
def test_integral_simple():
    bd = servidor.BaseDeDatos(max_hilos=1)
    limpiar_archivos(bd)

    servidor.procesar_tarea(bd, "integral: x**2")

    with open(bd.arch_integrales) as f:
        contenido = f.read()

    check("Integral x**2 -> x**3/3", "x**3/3" in contenido)


# 3) Test derivada simple ======================================
def test_derivada_simple():
    bd = servidor.BaseDeDatos(max_hilos=1)
    limpiar_archivos(bd)

    servidor.procesar_tarea(bd, "derivada: sin(x)")

    with open(bd.arch_derivadas) as f:
        contenido = f.read()

    check("Derivada sin(x) -> cos(x)", "cos(x)" in contenido)


# 4) Test tesis =================================================
def test_tesis():
    bd = servidor.BaseDeDatos(max_hilos=1)
    limpiar_archivos(bd)

    servidor.procesar_tarea(bd, "tesis: Prueba; hola mundo hola")

    with open(bd.arch_largo) as f:
        total = int(f.read().strip())

    check("Conteo de palabras en tesis (3)", total == 3)


# 5) Test manejo de errores  ===================================
def test_error_integral():
    bd = servidor.BaseDeDatos(max_hilos=1)
    limpiar_archivos(bd)

    servidor.procesar_tarea(bd, "integral: x**2+(")

    check("Log creado", os.path.exists("log.txt"))


# 6) Test concurrencia =========================================
def test_concurrencia():
    bd = servidor.BaseDeDatos(max_hilos=3)
    limpiar_archivos(bd)

    tareas = [f"integral: x**{i}" for i in range(10)]
    servidor.procesar_tareas(bd, tareas)

    with open(bd.arch_integrales) as f:
        lineas = f.read().strip().splitlines()

    check("10 integrales procesadas", len(lineas) == 10)


# MAIN: ejecutar todos los tests ===============================
if __name__ == "__main__":
    print("========== TEST MANUAL DEL SERVIDOR ==========\n")

    test_end_to_end()
    test_integral_simple()
    test_derivada_simple()
    test_tesis()
    test_error_integral()
    test_concurrencia()

    print("\n===============================================")
    print("Testeo finalizado.")
