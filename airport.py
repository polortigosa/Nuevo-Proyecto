import matplotlib.pyplot as plt  # Teoria BLO5: Per a gràfics
from tkinter import  messagebox


# ==========================================================
# PAS 1, 2 i 3: CODI ORIGINAL DEL TEU COMPANY (Sense tocar res)
# ==========================================================


class Airport:
    def __init__(self, icao_code, latitude, longitude):
        self.icao_code = icao_code
        self.latitude = latitude
        self.longitude = longitude
        self.schengen = False


def IsSchengenAirport(code):
    if not code or len(code) < 2:
        return False
    code_zona = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL',
                 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    return code[0:2] in code_zona


def SetSchengenAirports(airport):
    airport.schengen = IsSchengenAirport(airport.icao_code)


def PrintAirport(airport):
    print(f"Icao Code: {airport.icao_code}")
    print(f"Coordenadas: ({airport.latitude}, {airport.longitude})")
    print(f"Schengen: {'Yes' if airport.schengen else 'No'}")


def LoadAirports(filename):

    try:
        airports = []
        with open(filename, "r") as F:
            linea = F.readlines()
            for j in linea[1:]:
                lineas = j.replace("\n", "")
                datos = lineas.split(" ")
                code = datos[0]
                lat = datos[1]
                lon = datos[2]
                direccion_lat = lat[0]
                direccion_lon = lon[0]
                grados_lat = int(lat[1:3])
                grados_lon = int(lon[1:4])
                minutos_lat = int(lat[3:5])
                minutos_lon = int(lon[4:6])
                seg_lat = int(lat[5:7])
                seg_lon = int(lon[6:8])
                lat_decimal = grados_lat + minutos_lat / 60 + seg_lat / 3600
                lon_decimal = grados_lon + minutos_lon / 60 + seg_lon / 3600
                if direccion_lat == 'S':
                    lat_decimal = -lat_decimal
                if direccion_lon == 'W':
                    lon_decimal = -lon_decimal
                airport = Airport(code, lat_decimal, lon_decimal)
                airport.lat_str = lat  # Guardem el text original per al Save
                airport.lon_str = lon
                airports.append(airport)
    except FileNotFoundError:
        pass
    return airports


def SaveSchengenAirports(airports, filename):
    if not any(d.schengen for d in airports):
        return None
    with open(filename, 'w') as airports_file2:
        airports_file2.write("CODE LAT LON\n")
        for d in airports:
            if d.schengen:
                airports_file2.write(f"{d.icao_code} {d.lat_str} {d.lon_str}\n")


# ==========================================================
# PAS 4: GESTIÓ DE LLISTES (Modificat el mínim per a ser compatible)
# ==========================================================

def AddAirport(airports, airport):
    # Teoria BLO3: Recorrem la llista per evitar duplicats pel codi ICAO
    for a in airports:
        if a.icao_code == airport.icao_code:
            return  # Ja existeix, no fem res
    # Teoria BLO4: Si és nou, l'afegim al vector
    airports.append(airport)


def RemoveAirport(airports, code):
    # Teoria BLO3: Busquem l'objecte que volem eliminar
    for a in airports:
        if a.icao_code == code:
            # Teoria BLO4: Eliminem l'element trobat de la llista
            airports.remove(a)
            return True
    return False


# ==========================================================
# PAS 5: VISUALITZACIÓ
# ==========================================================

def PlotAirports(airports):
    # Teoria BLO2: Comptadors per l'esquema de recorregut
    if len(airports) > 0:
        schengen = 0
        no_schengen = 0
        for a in airports:
            if a.schengen:
                schengen += 1
            else:
                no_schengen += 1

    # Teoria BLO5: Creem el gràfic de barres (Passem etiquetes i després valors)
        fig = plt.figure()
        plt.bar(["Schengen", "No Schengen"], [schengen, no_schengen], color=['blue', 'red'])
        plt.title("Distribució d'Aeroports")
        plt.ylabel("Quantitat")
        return fig
    else:
        messagebox.showwarning("Error", "No hi ha dades per mostrar")

def MapAirports(airports):
    f = open("airports_map.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n')

    color_schengen = "ff00ff00"      # verde
    color_no_schengen = "ff0000ff"   # rojo

    for a in airports:
        f.write('<Placemark>\n')

        if a.schengen:
            f.write(f'  <Style><IconStyle><color>{color_schengen}</color></IconStyle></Style>\n')
        else:
            f.write(f'  <Style><IconStyle><color>{color_no_schengen}</color></IconStyle></Style>\n')

        f.write(f'  <name>{a.icao_code}</name>\n')
        f.write(f'  <Point><coordinates>{a.longitude},{a.latitude},0</coordinates></Point>\n')
        f.write('</Placemark>\n')

    f.write('</Document>\n</kml>')
    f.close()

