print("instalacion")
nombre = input("instalar")
import time
import sys

for i in range(101):
    sys.stdout.write(f"\rCargando... {i}%")
    sys.stdout.flush()
    time.sleep(0.05)
    print("instalando")

    print("instalado")

import time
import sys

print("Se cierra en 5 segundos...")

time.sleep(5)

sys.exit()