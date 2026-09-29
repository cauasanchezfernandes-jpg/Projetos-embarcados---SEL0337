import RPi.GPIO as GPIO
import time

PINO_PWM = 18                                                 #Valores definidos que serão utilizados posteriormente para a configuração PWM
FREQ_INICIAL = 50.0     
DUTY_INICIAL = 50.0     

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINO_PWM, GPIO.OUT, initial=GPIO.LOW)

pwm = GPIO.PWM(PINO_PWM, FREQ_INICIAL)                       #cria objeto com frequência inicial definida acima
pwm.start(DUTY_INICIAL)                  

freq = FREQ_INICIAL
duty = DUTY_INICIAL


def fade(passo=2, atraso=0.02):                              #Permite a alteração do duty cicle
    
    for dc in list(range(0, 101, passo)) + list(range(100, -1, -passo)):
        pwm.ChangeDutyCycle(dc)
        time.sleep(atraso)


def mostra_estado():
    periodo_ms = 1000.0 / freq
    t_alto_ms = periodo_ms * duty / 100.0
    print(f"  f = {freq:.1f} Hz | D = {duty:.0f} % | T = {periodo_ms:.2f} ms | "
          f"t_alto = {t_alto_ms:.2f} ms | V_médio ≈ {3.3 * duty / 100:.2f} V")


print("PWM iniciado. Comandos: f <Hz>, d <%>, fade, q")          #Solicita ao usuário os níoveis de frequência e duty cicle
mostra_estado()

try:                                                             #Roda o código até uma interrupção
    while True:
        cmd = input("> ").strip().lower().split()
        if not cmd:
            continue
        try:
            if cmd[0] == "q":
                break
            elif cmd[0] == "fade":
                fade()
                pwm.ChangeDutyCycle(duty)          
            elif cmd[0] == "f" and len(cmd) == 2:
                novo = float(cmd[1])               
                if novo <= 0:
                    print("A frequência deve ser positiva.")
                    continue
                freq = novo
                pwm.ChangeFrequency(freq)
                mostra_estado()
            elif cmd[0] == "d" and len(cmd) == 2:
                novo = float(cmd[1])
                if not 0 <= novo <= 100:
                    print("O duty cycle deve estar entre 0 e 100 %.")
                    continue
                duty = novo
                pwm.ChangeDutyCycle(duty)
                mostra_estado()
            else:
                print("Comando inválido. Use: f <Hz>, d <%>, fade, q")
        except ValueError:
            print("Valor inválido: digite um número.")
except KeyboardInterrupt:
    print("\nInterrompido pelo teclado.")
finally:
    pwm.stop()          
    GPIO.cleanup()
    print("PWM parado e GPIO liberada.")
