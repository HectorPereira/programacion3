# Librerias =====================================================
import threading
import time
import logging
from sympy import symbols, integrate, diff
import os


# Base de datos =================================================
class BaseDeDatos:
    def __init__(self, max_hilos=3):

        # Ruta absoluta de la carpeta donde esta main.py
        self.BASE = os.path.dirname(os.path.abspath(__file__))

        # Semaforo que limita hilos concurrentes
        self.semaforo = threading.Semaphore(max_hilos)

        # Locks
        self.lock_integrales = threading.Lock()
        self.lock_derivadas = threading.Lock()
        self.lock_tesis = threading.Lock()
        self.lock_largo = threading.Lock()

        # Archivos con ruta completa
        self.arch_integrales = os.path.join(self.BASE, "integrales.txt")
        self.arch_derivadas  = os.path.join(self.BASE, "derivadas.txt")
        self.arch_tesis      = os.path.join(self.BASE, "tesis.txt")
        self.arch_largo      = os.path.join(self.BASE, "largo.txt")

        self.crear_archivos()

    def crear_archivos(self):
        for archivo in [
            self.arch_integrales,
            self.arch_derivadas,
            self.arch_tesis,
            self.arch_largo
        ]:
            if not os.path.exists(archivo):
                with open(archivo, "w") as f:
                    pass


# Procesar tarea =================================================
def procesar_tarea(bd: BaseDeDatos, tarea: str):

    with bd.semaforo:
        inicio = time.time()

        try:
            x = symbols('x')

            # ------------------ INTEGRAL ------------------
            if tarea.startswith("integral:"):
                expr = tarea.replace("integral:", "").strip()
                resultado = integrate(expr, x)

                with bd.lock_integrales:
                    with open(bd.arch_integrales, "a") as f:
                        f.write(f"Integral de {expr} = {resultado}\n")

            # ------------------ DERIVADA ------------------
            elif tarea.startswith("derivada:"):
                expr = tarea.replace("derivada:", "").strip()
                resultado = diff(expr, x)

                with bd.lock_derivadas:
                    with open(bd.arch_derivadas, "a") as f:
                        f.write(f"Derivada de {expr} = {resultado}\n")

            # ------------------ TESIS ------------------
            elif tarea.startswith("tesis:"):
                _, resto = tarea.split("tesis:", 1)

                if ";" in resto:
                    titulo, texto = resto.split(";", 1)
                    titulo = titulo.strip()
                    texto = texto.strip()
                else:
                    titulo = "Sin titulo"
                    texto = resto.strip()

                palabras = len(texto.split())

                with bd.lock_tesis:
                    with open(bd.arch_tesis, "a") as f:
                        f.write(f"Tesis: {titulo} -- {texto}\n")

                # Actualizar largo
                with bd.lock_largo:
                    acumulado = 0
                    try:
                        with open(bd.arch_largo, "r") as f:
                            contenido = f.read().strip()
                            if contenido.isdigit():
                                acumulado = int(contenido)
                    except FileNotFoundError:
                        pass  # si no existe toma 0

                    nuevo_total = acumulado + palabras

                    with open(bd.arch_largo, "w") as f:
                        f.write(str(nuevo_total))

            else:
                logging.error(f"Tarea invalida o no reconocida: '{tarea}'")

        except Exception as e:
            logging.error(f"Error procesando tarea '{tarea}': {type(e).__name__} - {e}")

        finally:
            tiempo = time.time() - inicio
            logging.info(f"Tarea '{tarea}' completada en {tiempo:.4f} s")


# Procesar tareas ===============================================
def procesar_tareas(bd: BaseDeDatos, lista_tareas: list):
    hilos = []

    for t in lista_tareas:
        hilo = threading.Thread(target=procesar_tarea, args=(bd, t))
        hilos.append(hilo)
        hilo.start()

    for h in hilos:
        h.join()


    
# 4. Leer demanda =============================================
def leer_tareas():
    BASE = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(BASE, "demanda.txt")

    try:
        with open(ruta, "r") as f:
            contenido = f.readlines()

        tareas = [l.strip() for l in contenido if l.strip()]

        if not tareas:
            raise ValueError("demanda.txt esta vacio")

        return tareas

    except FileNotFoundError:
        logging.error("No se encontro demanda.txt")
        return []

    except Exception as e:
        logging.error(f"Error leyendo demanda.txt: {type(e).__name__} - {e}")
        return []


# Main ===========================================================
if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("Leyendo tareas...")
    tareas = leer_tareas()

    print(f"Se encontraron {len(tareas)} tareas.")

    bd = BaseDeDatos(max_hilos=3)

    print("Procesando tareas...")
    procesar_tareas(bd, tareas)

    print("Finalizado.")
