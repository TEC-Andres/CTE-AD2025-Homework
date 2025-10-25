"""
lista de estudiantes
    estudiante -> nombre  y 3 calificaciones

menu terminal
    añadir estudiante
    mostrar estudiantes
    mostrar promedio de un estudiante
    salir
"""

def añadir_estudiante_init(lista):
    max_estudiantes = int(input("¿Cuántos estudiantes desea añadir?: "))
    for _ in range(max_estudiantes):
        añadir_estudiante(lista)

def añadir_estudiante(lista):
    nombre = input("Ingrese el nombre del estudiante: ")
    calificaciones = []
    for i in range(3):
        calificacion = float(input(f"Ingrese la calificación {i+1} del estudiante: "))
        calificaciones.append(calificacion)
    estudiante = {"nombre": nombre, "calificaciones": calificaciones}
    lista.append(estudiante)
    print(f"Estudiante {nombre} añadido con éxito.")

def mostrar_estudiantes(lista):
    if not lista:
        print("No hay estudiantes en la lista.")
        return
    for estudiante in lista:
        print(f"Nombre: {estudiante['nombre']}, Calificaciones: {estudiante['calificaciones']}")

def mostrar_promedio_estudiante(lista):
    if not lista:
        print("No hay estudiantes en la lista.")
        return
    nombre = input("Ingrese el nombre del estudiante para mostrar su promedio: ")
    for estudiante in lista:
        if estudiante['nombre'] == nombre:
            promedio = sum(estudiante['calificaciones']) / len(estudiante['calificaciones'])
            print(f"El promedio de {nombre} es: {promedio:.3f}")
            return
    print(f"No se encontró al estudiante {nombre}.")

if __name__ == "__main__":
    lista_estudiantes = []
    añadir_estudiante_init(lista_estudiantes)
    while True:
        print("\nMenú:")
        print("1. Añadir estudiante")
        print("2. Mostrar estudiantes")
        print("3. Mostrar promedio de un estudiante")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            añadir_estudiante(lista_estudiantes)
        elif opcion == '2':
            mostrar_estudiantes(lista_estudiantes)
        elif opcion == '3':
            mostrar_promedio_estudiante(lista_estudiantes)
        elif opcion == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")