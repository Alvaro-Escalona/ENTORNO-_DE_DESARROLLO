import time
import sys
import random

# Configuración inicial de datos
NUM_FINCAS = 100000
# Generamos los datos base (pesos entre 50 y 500 kg)
datos_fincas = [random.randint(50, 500) for _ in range(NUM_FINCAS)]

def calcular_con_incremento(valor):
    return valor * 1.10

# 1. LISTA TRADICIONAL
inicio = time.time()
total_tradicional = 0
lista_tradicional = []
for peso in datos_fincas:
    lista_tradicional.append(calcular_con_incremento(peso))
total_tradicional = sum(lista_tradicional)
fin = time.time()
tiempo_tradicional = fin - inicio

print("LISTA TRADICIONAL")
print(f"Total: {total_tradicional:.2f} kg")
print(f"Tiempo: {tiempo_tradicional:.6f} segundos\n")

# 2. LIST COMPREHENSION
inicio = time.time()
lista_comprension = [calcular_con_incremento(peso) for peso in datos_fincas]
total_comprension = sum(lista_comprension)
fin = time.time()
tiempo_comprension = fin - inicio

print("LIST COMPREHENSION")
print(f"Total: {total_comprension:.2f} kg")
print(f"Tiempo: {tiempo_comprension:.6f} segundos\n")

# 3. GENERADOR
inicio = time.time()
# Usamos paréntesis para crear un generador (no ocupa memoria para todos los elementos a la vez)
generador = (calcular_con_incremento(peso) for peso in datos_fincas)
total_generador = sum(generador)
fin = time.time()
tiempo_generador = fin - inicio

print("GENERADOR")
print(f"Total: {total_generador:.2f} kg")
print(f"Tiempo: {tiempo_generador:.6f} segundos\n")
