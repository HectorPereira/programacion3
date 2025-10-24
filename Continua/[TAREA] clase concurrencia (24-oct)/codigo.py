import threading
import time
import random

# Recurso compartido: área de pesca
peces_disponibles = 20
mutex = threading.Lock()  # Controla la exclusión mutua

# Clase Pingüino (cada uno es un hilo)
class Pinguino(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.peces_comidos = 0

    def run(self):
        global peces_disponibles
        while True:
            # Intentar acceder al área de pesca
            with mutex:  # Sección crítica
                if peces_disponibles <= 0:
                    # No quedan peces, termina la competencia
                    break
                # Pescar un pez
                peces_disponibles -= 1
                self.peces_comidos += 1
                print(f"{self.nombre} pescó un pez | "
                      f"Quedan {peces_disponibles} peces.")
            # Simular el tiempo de espera antes del siguiente intento
            time.sleep(random.uniform(0.2, 1.0))

# Programa principal
def competencia_pingüinos():
    # Crear varios pingüinos
    nombres = ["Pingu", "Gloton", "Frio", "Nieve", "Tux"]
    pingüinos = [Pinguino(nombre) for nombre in nombres]

    # Iniciar los hilos
    for p in pingüinos:
        p.start()

    # Esperar a que todos terminen
    for p in pingüinos:
        p.join()

    # Mostrar resultados
    print("\n--- RESULTADOS FINALES ---")
    for p in pingüinos:
        print(f"{p.nombre}: {p.peces_comidos} peces comidos")

    # Determinar el ganador
    ganador = max(pingüinos, key=lambda x: x.peces_comidos)
    print(f"\nEl ganador es {ganador.nombre} con {ganador.peces_comidos} peces comidos.")

# Ejecución del programa
if __name__ == "__main__":
    competencia_pingüinos()
