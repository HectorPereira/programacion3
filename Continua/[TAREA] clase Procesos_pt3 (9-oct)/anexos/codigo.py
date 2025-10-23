import threading
import random
import time

# Pista compartida entre los corredores
# El Lock evita que dos hilos accedan al mismo recurso al mismo tiempo
lock = threading.Lock()

def corredor(nombre):
    # Cada hilo representa un corredor
    distancia = 0
    while distancia < 100:
        with lock:    # Solo un hilo puede entrar en esta seccion a la vez
            
            paso = random.randint(1, 10) # El corredor avanza una distancia aleatoria
            distancia += paso

            # Muestra el progreso actual del corredor
            print(f"{nombre} avanza {paso} m (total: {distancia})")
        
        # Simula tiempo de espera antes del siguiente intento
        # durante este tiempo la pista puede ser usada por otro hilo
        time.sleep(0.5)

# Creacion de los hilos (dos corredores)
t1 = threading.Thread(target=corredor, args=("Corredor A",))
t2 = threading.Thread(target=corredor, args=("Corredor B",))

# Inicio de los hilos
t1.start()
t2.start()

# Espera a que ambos corredores terminen la carrera
t1.join()
t2.join()

print("Carrera terminada.")