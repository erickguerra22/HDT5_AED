totalTime = 0
def getTotalTime():
    return totalTime

def process(name, env, RAM, CPU, arrival, numIns, ramNeed, speedCPU, random):
    yield env.timeout(arrival)
    arrivalTime = env.now
    
    print("%s (llegada en %f) requiere %d de memoria RAM, %d disponible. Estado: NEW" %(name,arrival,ramNeed, RAM.level))
    yield RAM.get(ramNeed)
    print("%s ha recibido %d de memoria RAM, %d disponible. Estado: Admitted" %(name, ramNeed, RAM.level))
    
    while numIns > 0:
        print("%s tiene %d instrucciones pendientes. Estado: READY" %(name, numIns))
        
        with CPU.request() as req:
            yield req
            
            insMade = 0
            numIns = numIns - speedCPU
            if numIns < 0:
                insMade = speedCPU + numIns
            else:
                insMade = speedCPU
            yield env.timeout(1)
            
            print("%s. El CPU ha ejecutado %d instrucciones correctamente (tiempo actual: %d). Estado: RUNNING" %(name, insMade, env.now))
            print("Ram restante: %d" %(RAM.level))
        
        if numIns > 0:
            nextAct = random.randint(1,2)
            if nextAct == 1:
                print("%s esta ejecutando instrucciones I/O. Estado: WAITING" %(name))
                yield env.timeout(1)
    
    yield RAM.put(ramNeed)
    print("%s termino su ejecucion en el tiempo: %d. Nueva cantidad de memoria disponible: %d. Estado: TERMINATED" % (name, env.now, RAM.level))
    global totalTime
    totalTime += env.now - arrivalTime
    print("Tiempo que duro la ejecucion: %d" %(env.now - arrivalTime))