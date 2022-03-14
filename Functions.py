'''
    Funciones utilizadas para la simulación de CPU
    Programador:
        - Erick Stiv Junior Guerra Muñoz
    Fecha: 12 de marzo de 2022
'''
totalTime = 0 # Tiempo total que duró la simulación
times = [] # Tiempo que duró la ejecución de cada proceso

# Creacion de funciones
def getTotalTime():
    '''
        Devuelve el tiempo total que duró la simulación
    '''
    return totalTime

def getTimes():
    '''
        Devuelve la lista del tiempo utilizado por cada proceso
    '''
    return times

def process(name, env, RAM, CPU, arrival, numIns, ramNeed, speedCPU, random):
    '''
        Crea el proceso con la informacion brindada
        y luego lo ejecuta según el orden de llegada.
    '''
    yield env.timeout(arrival) # Simula la espera hasta la llegada del proceso
    arrivalTime = env.now # Guarda el tiempo en el que llegó el proceso
    
    # Se verifica si el proceso puede recibir la cantidad de memoria que necesita
    print("%s (llegada en %f) requiere %d de memoria RAM, %d disponible. Estado: NEW" %(name,arrival,ramNeed, RAM.level))
    yield RAM.get(ramNeed) # Espera hasta poder obtener la cantidad de memoria RAM solicitada
    print("%s ha recibido %d de memoria RAM, %d disponible. Estado: Admitted" %(name, ramNeed, RAM.level))
    
    # Se ejecutan todas las instrucciones
    while numIns > 0:
        print("%s tiene %d instrucciones pendientes. Estado: READY" %(name, numIns))
        
        with CPU.request() as req:
            yield req # Espera a que el CPU esté disponible
            
            insMade = speedCPU
            numIns = numIns - speedCPU # Se restan la cantidad de instrucciones realizadas
            if numIns < 0:
                insMade = speedCPU + numIns
            yield env.timeout(1) # Simula un ciclo de reloj del CPU
            
            print("%s. El CPU ha ejecutado %d instrucciones correctamente (tiempo actual: %d). Estado: RUNNING" %(name, insMade, env.now))
            print("Ram restante: %d" %(RAM.level)) # Se muestra la cantidad de memoria RAM disponible
        
        if numIns > 0:
            nextAct = random.randint(1,2)
            if nextAct == 1:
                print("%s esta ejecutando instrucciones I/O. Estado: WAITING" %(name))
                yield env.timeout(1) # Simula un ciclo de reloj del CPU
    
    # Al terminar de ejecutar todas las intrucciones:
    yield RAM.put(ramNeed) # Se devuelve la cantidad de memoria RAM utilizada
    print("%s termino su ejecucion en el tiempo: %d. Cantidad de memoria restaurada: %d. Nueva cantidad de memoria disponible: %d. Estado: TERMINATED" % (name, env.now, ramNeed, RAM.level))
    global totalTime
    global times
    times.append(env.now - arrivalTime) # Almacena el tiempo que tomó la ejecución del proceso
    totalTime += env.now - arrivalTime # Suma el tiempo del proceso al tiempo total de la simulación
    print("Tiempo que duro la ejecucion: %d segundos" %(env.now - arrivalTime))