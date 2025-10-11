import threading
import random
import time

# Recurso compartido (la "pista")
lock = threading.Lock()

def corredor(nombre):
    distancia = 0
    while distancia < 100:
        with lock:  # solo un hilo puede entrar aqui
            paso = random.randint(1, 10)
            distancia += paso
            print(f"{nombre} avanza {paso} m (total: {distancia})")
        time.sleep(0.5)  # simula tiempo fuera de la pista

# Creacion de hilos
t1 = threading.Thread(target=corredor, args=("Corredor 1",))
t2 = threading.Thread(target=corredor, args=("Corredor 2",))

t1.start()
t2.start()
t1.join()
t2.join()

print("Carrera terminada.")