from multiprocessing import Process, Queue, current_process
import re

def evaluar_expresion(expr, valores, q):
    # Reemplazar el operador lógico "xor" por el símbolo equivalente de Python (^)
    expr = expr.replace("xor", "^")

    # Sustituir las variables (a, b, c, d) por sus valores booleanos (True / False)
    # El patrón evita reemplazar letras dentro de otras palabras o nombres más largos.
    for var, val in valores.items():
        expr = re.sub(fr"(?<![a-zA-Z0-9_]){var}(?![a-zA-Z0-9_])", str(val), expr)

    try:
        # Evaluar la proposición lógica con los valores reemplazados
        resultado = eval(expr)
    except Exception as e:
        # Si ocurre un error de sintaxis o variable inexistente, se guarda el mensaje
        resultado = f"Error: {e}"

    # Enviar el resultado a la cola con el nombre del proceso
    q.put((current_process().name, resultado))


def leer_y_crear_procesos(nombre_archivo, q, valores):
    # Leer todas las proposiciones del archivo, omitiendo líneas vacías
    with open(nombre_archivo) as f:
        lineas = [line.strip() for line in f if line.strip()]

    procesos = []
    for i, expr in enumerate(lineas):
        # Crear un proceso independiente para cada línea (proposición)
        p = Process(target=evaluar_expresion, args=(expr, valores, q), name=f"Linea-{i+1}")
        p.start()
        procesos.append(p)

    return procesos


if __name__ == "__main__":
    q = Queue()              # Cola compartida para enviar resultados desde los procesos hijos
    valores_globales = {}    # Diccionario con los valores lógicos definidos por el usuario

    # Solicitar los valores de las variables antes de crear los procesos
    variables = ["a", "b", "c", "d"]
    print("Ingrese los valores lógicos para las variables (0 = False, 1 = True):")
    for v in variables:
        valores_globales[v] = bool(int(input(f"{v}: ")))

    # Crear y lanzar los procesos según las líneas del archivo de proposiciones
    procesos = leer_y_crear_procesos("Continua/[TAREA] clase concurrencia (30y31-oct)/proposiciones.txt",
                                     q, valores_globales)

    # Esperar a que todos los procesos terminen antes de mostrar resultados
    for p in procesos:
        p.join()

    # Extraer y mostrar los resultados almacenados en la cola
    print("\n=== Resultados ===")
    while not q.empty():
        pid, res = q.get()
        print(f"{pid}: {res}")
