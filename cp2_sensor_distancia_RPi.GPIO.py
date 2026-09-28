import RPi.GPIO as GPIO
import time


PINO_TRIG = 23                        #Definição do pino de trigger so ultrassom no pino 23 da Rabsberry pi
PINO_ECHO = 24                        #Definição do pino de trigger so ultrassom no pino 24 da Rabsberry pi
PINO_LED = 18             

V_SOM = 343.0            
TIMEOUT = 0.04           
N_AMOSTRAS = 5           
LIMIAR_LIGA_CM = 20.0    
LIMIAR_DESLIGA_CM = 25.0 
INTERVALO = 0.1                       #Definição de vaariáveis que serão utilizadas para a lógica do código



def dispara_e_mede():      
  
    GPIO.output(PINO_TRIG, GPIO.LOW)                   #Código utilizado para enviar o pulso de ultrassom
    time.sleep(0.000002)                 
    GPIO.output(PINO_TRIG, GPIO.HIGH)
    time.sleep(0.00001)                  
    GPIO.output(PINO_TRIG, GPIO.LOW)

    t_limite = time.monotonic() + TIMEOUT              #Utilizado para medir duração de tempo na análise, nesse caso tempo inicial
    while GPIO.input(PINO_ECHO) == GPIO.LOW:
        if time.monotonic() > t_limite:
            return None                  
    t_inicio = time.monotonic()

    
    t_limite = time.monotonic() + TIMEOUT              #Utilizado para medir duração de tempo da análise, nesse caso tempo final
    while GPIO.input(PINO_ECHO) == GPIO.HIGH:
        if time.monotonic() > t_limite:
            return None                  
    t_fim = time.monotonic()

    
    t_echo = t_fim - t_inicio                           #Tempo total de eco e recebimento do ultrassom
    distancia_cm = (t_echo * V_SOM / 2) * 100           #Retorna distância percorrida, baseando na velocidade do som
    return distancia_cm


def mede_distancia(n=N_AMOSTRAS):                       #Mede várias vezes a distância amostrada e retorna a medinana para um resultado mais fidedigno

    amostras = []
    for _ in range(n):
        d = dispara_e_mede()
        if d is not None and 2.0 <= d <= 400.0:   
            amostras.append(d)
        time.sleep(0.01)                 
    if not amostras:
        return None
    amostras.sort()
    return amostras[len(amostras) // 2]



GPIO.setmode(GPIO.BCM)                                                
GPIO.setwarnings(False)
GPIO.setup(PINO_TRIG, GPIO.OUT, initial=GPIO.LOW)   
GPIO.setup(PINO_ECHO, GPIO.IN)                      
GPIO.setup(PINO_LED, GPIO.OUT, initial=GPIO.LOW)    

time.sleep(0.5)                          
led_aceso = False

print(f"Medindo distância. O LED acende abaixo de {LIMIAR_LIGA_CM:.0f} cm "
      f"e apaga acima de {LIMIAR_DESLIGA_CM:.0f} cm.")
print("CTRL+C para sair.")

try:
    while True:
        d = mede_distancia()

        if d is None:
            GPIO.output(PINO_LED, GPIO.LOW)         # sem leitura -> apaga
            led_aceso = False
            print("\rSem eco (fora de alcance)          ", end="", flush=True)
        else:
            # Histerese: liga abaixo de um limiar, desliga acima de outro
            if not led_aceso and d < LIMIAR_LIGA_CM:
                GPIO.output(PINO_LED, GPIO.HIGH)
                led_aceso = True
            elif led_aceso and d > LIMIAR_DESLIGA_CM:
                GPIO.output(PINO_LED, GPIO.LOW)
                led_aceso = False

            estado = "LED ACESO " if led_aceso else "LED apagado"
            print(f"\rDistância: {d:6.1f} cm | {estado}", end="", flush=True)

        time.sleep(INTERVALO)
except KeyboardInterrupt:
    print("\nPrograma encerrado.")
finally:
    GPIO.cleanup()                       # libera TRIG, ECHO e LED
    print("GPIO liberada (cleanup).")
    
    
    
    
#esse foi o utilizado no video 1
