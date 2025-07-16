from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocalizador = Nominatim(user_agent="medidor_distancia")

print("Bienvenido al medidor de distancia entre ciudades.\n")
print("Puedes salir en cualquier momento escribiendo 's' o 'si'.\n")

while True:
    #Datos solicitados a usuario
    origen = input("Ingrese la Ciudad de origen: ")
    if origen.lower() in ["s", "si"]:
        print("Saliendo del programa...")
        break

    destino = input("Ingrese la Ciudad de destino: ")
    if destino.lower() in ["s", "si"]:
        print("Saliendo del programa...")
        break

    #Validacion de si existen las cuidades
    ubicacion_origen = geolocalizador.geocode(origen)
    ubicacion_destino = geolocalizador.geocode(destino)

    if ubicacion_origen and ubicacion_destino:
        coord_origen = (ubicacion_origen.latitude, ubicacion_origen.longitude)
        coord_destino = (ubicacion_destino.latitude, ubicacion_destino.longitude)

        distancia_km = geodesic(coord_origen, coord_destino).kilometers
        distancia_mi = geodesic(coord_origen, coord_destino).miles

        #Medio de transporte
        print("\nSeleccione el medio de transporte:")
        print("1. Auto")
        print("2. Bus")
        print("3. Avión")

        opcion = input("Ingrese el número correspondiente: ")
        if opcion.lower() in ["s", "si"]:
            print("Saliendo del programa...")
            break

        if opcion == "1":
            medio = "automóvil"
            velocidad_kmh = 90
        elif opcion == "2":
            medio = "bus"
            velocidad_kmh = 80
        elif opcion == "3":
            medio = "avión"
            velocidad_kmh = 700
        else:
            print("Opción no válida. Se asumirá viaje en automóvil.")
            medio = "automóvil"
            velocidad_kmh = 90

        #Velocidades
        duracion_horas = distancia_km / velocidad_kmh
        horas = int(duracion_horas)
        minutos = int((duracion_horas - horas) * 60)

        # Mostrar dirección detectada
        print(f"\n Dirección detectada para origen: {ubicacion_origen.address}")
        print(f" Dirección detectada para destino: {ubicacion_destino.address}")

        # Resultados
        print(f"\n Distancia entre {origen} y {destino}:")
        print(f"- {distancia_km:.2f} kilómetros")
        print(f"- {distancia_mi:.2f} millas")
        print(f"- Duración estimada en {medio}: {horas} horas y {minutos} minutos")

        # Narrativa del viaje
        print("\n Narrativa del viaje:")
        print(f"El viaje comienza en la ciudad de {origen.capitalize()}, y se dirige hacia {destino.capitalize()}.")
        print(f"La distancia entre ambas ciudades es de aproximadamente {distancia_km:.2f} km ({distancia_mi:.2f} millas).")
        print(f"Usando {medio}, este trayecto puede tomar alrededor de {horas} horas y {minutos} minutos, considerando una velocidad promedio de {velocidad_kmh} km/h.")
        print("Durante el recorrido, se pueden atravesar distintas zonas geográficas, con paisajes urbanos o rurales según la ruta elegida.")

    else:
        print(" No se pudo encontrar una o ambas ciudades. Verifique los nombres e intente nuevamente.")
