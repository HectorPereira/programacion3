import time, random
from concurrent.futures import ThreadPoolExecutor

def corredor(nombre):
    distancia = 0
    for s in range(5): # 5 pasos
        # Avance aleatorio para cada corredor
        distancia += random.randint(1, 5)
        print(f"[{nombre}] Segundo {s+1}: total {distancia} m")
        time.sleep(1) 
    return nombre, distancia

with ThreadPoolExecutor(2) as pool:
    print("Comienza la carrera\n")
    # Inciar threads
    resultados = pool.map(corredor, ["Corredor A", "Corredor B"])

print("\nCarrera finalizada")
for nombre, d in resultados:
    print(f"{nombre} recorrio {d} metros.")
