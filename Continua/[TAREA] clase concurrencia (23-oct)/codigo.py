# ============================================
# Pizzeria Cosmica - Concurrencia + Grafos
# Programacion 3 - UTEC
# Hector Pereira
# ============================================
import threading
import time
from collections import defaultdict
from random import uniform

# --------------------------------------------
# Definicion de grafo de precedencia
# --------------------------------------------
class GrafoPrecedencia:
    def __init__(self):
        self.dependencias = defaultdict(list)

    def agregar_dependencia(self, tarea, depende_de):
        self.dependencias[tarea].append(depende_de)

    def get_dependencias(self, tarea):
        return self.dependencias[tarea]

# --------------------------------------------
# Tareas de preparacion (simulan trabajo)
# --------------------------------------------
def preparar_masa(pedido_id):
    print(f"[Pedido {pedido_id}] Preparando masa...")
    time.sleep(uniform(0.5, 1.5))
    print(f"[Pedido {pedido_id}] Masa lista.")

def agregar_salsa(pedido_id):
    print(f"[Pedido {pedido_id}] Agregando salsa...")
    time.sleep(uniform(0.5, 1.5))
    print(f"[Pedido {pedido_id}] Salsa lista.")

def agregar_queso(pedido_id):
    print(f"[Pedido {pedido_id}] Agregando queso...")
    time.sleep(uniform(0.5, 1.5))
    print(f"[Pedido {pedido_id}] Queso listo.")

def agregar_pepperoni(pedido_id):
    print(f"[Pedido {pedido_id}] Agregando pepperoni estelar...")
    time.sleep(uniform(0.5, 1.5))
    print(f"[Pedido {pedido_id}] Pepperoni listo.")

def agregar_champinones(pedido_id):
    print(f"[Pedido {pedido_id}] Agregando champinones galacticos...")
    time.sleep(uniform(0.5, 1.5))
    print(f"[Pedido {pedido_id}] Champinones listos.")

def hornear(pedido_id):
    print(f"[Pedido {pedido_id}] Horneando pizza cosmica...")
    time.sleep(uniform(0.5, 1.5))
    print(f"[Pedido {pedido_id}] Pizza lista para servir.")

# Mapeo nombre->funcion
FUNCIONES_TAREAS = {
    "preparar_masa": preparar_masa,
    "agregar_salsa": agregar_salsa,
    "agregar_queso": agregar_queso,
    "agregar_pepperoni": agregar_pepperoni,
    "agregar_champiñones": agregar_champinones,
    "agregar_champinones": agregar_champinones,
    "hornear": hornear
}

# --------------------------------------------
# Ejecutor de pedidos con dependencias
# --------------------------------------------
def ejecutar_pedido(pedido_id, etapas, grafo):
    """
    Ejecuta las tareas (etapas) de un pedido en el orden correcto según sus dependencias.

    Parámetros:
    - pedido_id: identificador del pedido actual.
    - etapas: lista de tareas (etapas) que deben ejecutarse para este pedido.
    - grafo: estructura de dependencias entre tareas (objeto con método get_dependencias()).
    """

    completadas = set()  # Conjunto para guardar las tareas ya finalizadas.

    # Iteramos sobre cada tarea que debe ejecutarse.
    for tarea in etapas:
        # Filtramos las dependencias de la tarea que también pertenecen a este conjunto de etapas.
        dependencias_reales = [
            d for d in grafo.get_dependencias(tarea) if d in etapas
        ]

        # Esperamos hasta que todas las dependencias de esta tarea estén completadas.
        for dependencia in dependencias_reales:
            while dependencia not in completadas:
                time.sleep(0.05)  # Pequeña pausa para no saturar el CPU mientras esperamos.

        # Cuando todas las dependencias están listas, ejecutamos la función correspondiente a la tarea.
        FUNCIONES_TAREAS[tarea](pedido_id)

        # Marcamos la tarea como completada.
        completadas.add(tarea)

# --------------------------------------------
# Programa principal
# --------------------------------------------
if __name__ == "__main__":
    pedidos = [
        ["preparar_masa", "agregar_salsa", "agregar_queso", "hornear"],
        ["preparar_masa", "agregar_salsa", "agregar_queso", "agregar_pepperoni", "hornear"],
        ["preparar_masa", "agregar_salsa", "agregar_queso", "agregar_champinones", "hornear"]
    ]

    grafo = GrafoPrecedencia()
    grafo.agregar_dependencia("agregar_salsa", "preparar_masa")
    grafo.agregar_dependencia("agregar_queso", "agregar_salsa")
    grafo.agregar_dependencia("agregar_pepperoni", "agregar_queso")
    grafo.agregar_dependencia("agregar_champinones", "agregar_queso")
    grafo.agregar_dependencia("hornear", "agregar_queso")
    grafo.agregar_dependencia("hornear", "agregar_pepperoni")
    grafo.agregar_dependencia("hornear", "agregar_champinones")

    hilos = []  # Lista para guardar los objetos Thread creados.

    # Itera sobre cada pedido junto con su índice (empezando desde 1).
    for i, etapas in enumerate(pedidos, start=1):
        # Crea un hilo para ejecutar las etapas del pedido i.
        # 'target' es la función que el hilo ejecutará.
        # 'args' son los argumentos que se pasan a esa función.
        t = threading.Thread(target=ejecutar_pedido, args=(i, etapas, grafo))

        # Guarda el hilo en la lista para poder gestionarlo después.
        hilos.append(t)

        # Inicia el hilo: a partir de aquí 'ejecutar_pedido' comienza a correr en paralelo.
        t.start()

    # Espera a que todos los hilos terminen antes de continuar.
    for h in hilos:
        h.join()


    print("\nTodos los pedidos fueron completados con exito.")
