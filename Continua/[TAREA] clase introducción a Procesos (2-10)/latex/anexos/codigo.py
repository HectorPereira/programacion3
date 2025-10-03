from multiprocessing import Process, Queue
import time

# --- Funcion del emisor ---
def proceso_emisor(cola):
    while True:
        mensaje = input("Escribe un mensaje (o 'salir' para terminar): ")
        cola.put(mensaje)
        if mensaje.lower() == "salir":
            break
        time.sleep(0.1)  # pausa para no saturar

# --- Funcion del receptor ---
def proceso_receptor(cola):
    while True:
        mensaje = cola.get()   # Espera a recibir mensaje
        if mensaje.lower() == "salir":
            print("El emisor cerro la comunicacion.")
            break
        print(f"[Receptor] Mensaje recibido: {mensaje}")

# --- Programa principal ---
if __name__ == "__main__":
    # 3. Crear cola compartida
    cola_compartida = Queue()

    # 4. Crear procesos
    emisor = Process(target=proceso_emisor, args=(cola_compartida,))
    receptor = Process(target=proceso_receptor, args=(cola_compartida,))

    # 5. Iniciar procesos
    emisor.start()
    receptor.start()

    # Esperar a que terminen
    emisor.join()
    receptor.join()

    print("Chat finalizado.")
