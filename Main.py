'''
    Programa que simula la ejecución de procesos en un CPU
    Programador:
        - Erick Stiv Junior Guerra Muñoz
    Fecha: 12 de marzo de 2022
'''

# Importación de módulos
import simpy
import random
import Functions as fc

# Interfaz con el usuario
print("Bienvenido al simulador de CPU!") # Mensaje de bienvienida
print("Indique la siguiente informacion antes de empezar:")
numProcess = int(input("Numero de procesos a ejecutar: ")) # Se solicita el número de procesos a ejecutar en la simulación
intervals = int(input("Intervalo para la distribucion exponencial: ")) # Se solicita el número de intervalos a utilizar
ramQuantity = int(input("Capacidad de memoria RAM: ")) # Se solicita la capacidad de memoria RAM
numCPU = int(input("Numero de procesadores a utilizar: ")) # Se solicita el número de CPUs a utilizar
speedCPU = int(input("Instrucciones que el CPU es capaz de ejecutar a la vez: ")) # Se solicita la velocidad de cada CPU

# Inicialización de variables
env = simpy.Environment() # Se crea el ambiente de simulación
RAM = simpy.Container(env, init = ramQuantity ,capacity = ramQuantity)
CPU = simpy.Resource(env, capacity = numCPU)
random.seed(666) # Semilla que se utilizará durante toda la simulación
promTime = 0
standDev = 0

# Creación de procesos
for i in range(numProcess):
    arrival = random.expovariate(1.0/intervals) # Tiempo en el que llega el proceso al CPU
    numIns = random.randint(1,10) # Número de instrucciones que realizará el proceso
    ramNeed = random.randint(1,10) # Memoria RAM que necesita el proceso
    env.process(fc.process("Proceso # %s" %i, env, RAM, CPU, arrival, numIns, ramNeed, speedCPU, random)) # Se crea el proceso con la información creada
    
# Da inicio a la simulación
input("Presione enter para iniciar la simulacion: ")
env.run()

# Se calcula e imprime el tiempo promedio que consumio cada proceso
promTime = fc.getTotalTime()/numProcess
print("\nTiempo promedio: %f segundos" % promTime)

# Se calcula e imprime la desviación estándar de los tiempos.
times = fc.getTimes()
suma = 0
for i in times:
    suma += (i - promTime)**2
 
stanDev = (suma/(numProcess-1))**0.5
print("\nDesviacion estandar: %f segundos" % stanDev)

# Se muestra la información general que se utilizó en la simulacion
print("Process: %d, Intervals: %d, RAM: %d, CPU: %d, Speed: %d" %(numProcess, intervals, ramQuantity, numCPU, speedCPU))