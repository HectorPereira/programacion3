import os
import multiprocessing

def count_words(filename, result_queue):
    """Cuenta las palabras en un archivo de texto y envía el resultado a la cola."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        word_count = len(content.split())
        result_queue.put((filename, word_count))
    except Exception as e:
        result_queue.put((filename, f"Error: {e}"))

def main():
    # Directorio con archivos de texto
    input_dir = "C:/Users/hecto/OneDrive/Desktop/Github UTEC/programacion3/Laboratorios/Laboratorio 3/anexos/archivos_texto"  # cambia esta ruta a la carpeta donde tengas los .txt

    # Crear lista con los archivos de texto
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.txt')]

    # Crear la cola para recibir resultados
    result_queue = multiprocessing.Queue()

    # Crear y lanzar un proceso por archivo
    processes = []
    for filename in files:
        p = multiprocessing.Process(target=count_words, args=(filename, result_queue))
        processes.append(p)
        p.start()

    # Esperar que terminen todos los procesos
    for p in processes:
        p.join()

    # Recolectar los resultados de la cola
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # Mostrar resultados
    print("\n📊 Resultados de conteo de palabras:")
    for filename, count in results:
        print(f" - {os.path.basename(filename)} → {count} palabras")

if __name__ == "__main__":
    main()
