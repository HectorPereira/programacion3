from multiprocessing import Process, Queue
import time

def proceso_receptor(cola):
    # Recibe el mensaje desde la cola y 
    # termina el proceso cuando encuentra "salir"
    while True:
        mensaje = cola.get()
        if mensaje.lower() == "salir":
            print("[Receptor] El emisor cerro la comunicacion.")
            break
        print(f"[Receptor] Mensaje recibido: {mensaje}")


if __name__ == "__main__":
    cola_compartida = Queue()


    receptor = Process(target=proceso_receptor, args=(cola_compartida,))
    receptor.start()

    print("[Emisor] Escribe un mensaje y presiona Enter ('salir' para terminar):")
    

    while True:
        mensaje = input("> ")  

        if not mensaje.strip():
            continue

        cola_compartida.put(mensaje)
        if mensaje.lower() == "salir":
            break
        time.sleep(0.1)

    receptor.join()
    print("[Sistema] Chat finalizado.")
