import csv
import random
import string

def generar_password(longitud=8):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for i in range(longitud))

def generar_usuarios(num_usuarios):
    with open('usuarios_prueba.csv', 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        for i in range(1, num_usuarios + 1):
            email = f"usuario{i}@prueba.com"
            password = generar_password()
            writer.writerow([email, password])

generar_usuarios(10000)