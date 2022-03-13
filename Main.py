import simpy
import random
import Functions as fc

print("Bienvenido al simulador de CPU!")
print("Indique la siguiente informacion antes de empezar:")
numProcess = int(input("Numero de procesos a ejecutar: "))
intervals = int(input("Intervalo para la distribucion exponencial: "))
ramQuantity = int(input("Capacidad de memoria RAM: "))
numCPU = int(input("Numero de procesadores a utilizar: "))
speedCPU = int(input("Instrucciones que el CPU es capaz de ejecutar a la vez: "))

env = simpy.Environment()
RAM = simpy.Container(env, init = ramQuantity ,capacity = ramQuantity)
CPU = simpy.Resource(env, capacity = numCPU)
seed = random.seed(10)
promTime = 0
standDev = 0

for i in range(numProcess):
    arrival = random.expovariate(1.0/intervals)
    numIns = random.randint(1,10)
    ramNeed = random.randint(1,10)
    env.process(fc.process("Proceso #%s" %i, env, RAM, CPU, arrival, numIns, ramNeed, speedCPU, random))
    
input("Presione enter para iniciar la simulacion: ")
env.run()
promTime = fc.getTotalTime()/numProcess
print("\nTiempo promedio: %f segundos" % promTime)

times = fc.getTimes()
suma = 0
for i in times:
    suma += (i - promTime)**2
 
stanDev = (suma/(numProcess-1))**0.5
print("\nDesviacion estandar: %f segundos" % stanDev)