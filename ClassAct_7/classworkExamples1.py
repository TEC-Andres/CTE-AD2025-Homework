nombre = input("\n¿Cómo te llamas, minion? ")
edad = int(input("\n¿Cuántos años tienes? "))

print("Bello", nombre + "!", "Tienes", edad, "años.")

if edad < 18:
    print("Estado: minion en entrenamiento.")
else:
    print("Estado: minion del equipo de Gru.")


# Ejercicio 2: Longitud de una cadena
nombres_minions = []
print("Escribe los nombres de los minions para el grupo de whatsapp.")
print("Escribe 'fin' cuando termines.")
while True:
    nombre_minion = input("Nombre del minion: ")
    if nombre_minion.lower() == 'fin':
        break
    nombres_minions.append(nombre_minion)
    print("Agregando " + nombre_minion)

print("Los nombres de los minions son:")
for nombre in nombres_minions:
    print(nombre, "-", len(nombre), "caracteres.")

def analizar_plan(texto):
    letras_totales = len(texto)

    veces_gru = texto.lower().count('gru')

    palabras = texto.split()
    total_palabras = len(palabras)

    print("Análisis del plan:")
    print("Total de caracteres:", letras_totales)
    print("Total de palabras:", total_palabras)
    print("Veces que aparece 'gru':", veces_gru)

plan = input("\nEscribe el plan maestro de Gru: ")
analizar_plan(plan)