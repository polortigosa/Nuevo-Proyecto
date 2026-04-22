
import math
from airport import *
import matplotlib.pyplot as plt

class Aircraft:
    def __init__(self, id , origin, time, company):
        self.id = id
        self.origin = origin
        self.time = time
        self.company = company
        self.schengen = False


def LoadArrivals(filename):

    try:
        aircrafts = []
        with open(filename, "r") as F:
            linea = F.readlines()
            for j in linea[1:]:
                lineas = j.strip()
                datos = lineas.split()

                if len(datos) != 4:
                    continue

                id = str(datos[0])
                origin = datos[1]
                time = datos[2]
                company = datos[3]

                if len(origin) != 4 or len(company) != 3:
                    continue

                if ":" not in time:
                    continue

                hora = time.split(":")

                if len(hora) != 2:
                    continue
                h = int(hora[0])
                m = int(hora[1])
                if not (0 <= h < 24 and 0 <= m < 60):

                    continue

                aircraft = Aircraft(id, origin, time, company)
                aircrafts.append(aircraft)

    except FileNotFoundError:
        return  []
    return aircrafts

def PlotArrivals (aircrafts):

    horas = [0]*24
    if not aircrafts:
        print("Error: la llista està buida. (PlotArrivals)")
        messagebox.showwarning("Error", "No hi ha dades per mostrar")
        return

    for a in aircrafts:
        timepos = a.time
        trozos = timepos.split(":")

        if len(trozos) != 2:
            continue
        try:
            hora = int(trozos[0])
        except:
            continue
        if 0 <= hora < 24:
            horas[hora] += 1

    fig = plt.figure()
    plt.bar(range(24), horas)

    plt.xlabel("Hores del dia")
    plt.ylabel("Nombre d'aterratge")
    plt.title("Freqüència d'aterratge")
    plt.xticks(range(24))
    return fig


def SaveFlights(aircrafts, filename):

    if not aircrafts:
        print("Error. Llista buida. (SaveFlights)")

        return -1

    with open(filename, 'w') as aircrafts_file2:
        aircrafts_file2.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")

        for d in aircrafts:
            if d.id:
                id = d.id
            else:
                id = "-"

            if d.origin:
                origin = d.origin
            else:
                origin = "-"

            if d.time:
                time = d.time
            else:
                time = "-"

            if d.company:
                company = d.company
            else:
                company = "-"

            aircrafts_file2.write(f"{id} {origin} {time} {company}\n")
    return 0#mirar cuando usar 0 o -1 y que significan

def PlotAirlines (aircrafts):#contador basico, sin usar ninguna libreria para contar
    if not aircrafts:
        print("Error: la llista està buida.(PlotAirlines)")
        messagebox.showwarning("Error", "No hi ha dades per mostrar")

        return

    airlines = []
    flights = []

    for a in aircrafts:
        airline = a.company

        if airline not in airlines:
            airlines.append(airline)
            flights.append(1)
        else:
            i = 0
            while i < len(airlines):
                if airlines[i] == airline:
                    flights[i] += 1
                    break
                i += 1

    fig= plt.figure()
    plt.bar(airlines, flights)

    plt.xlabel("Aerolínea")
    plt.ylabel("Quantitat de vols")
    plt.title("Vols per aerolínea ")

    return fig

def IsSchengenAircraft(code):
    code_zona = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL',
                 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    if not code or len(code) < 2:
        return False
    return code[0:2] in code_zona


def SetSchengenAircrafts(aircraft):
    aircraft.schengen = IsSchengenAircraft(aircraft.origin)

def PlotFlightsType (aircrafts):
    if not aircrafts:
        print("Error, llista buida(zonas_schengen)")
        messagebox.showwarning("Error", "No hi ha dades per mostrar")
        return
    schengen = 0
    no_schengen = 0
    for a in aircrafts:
        SetSchengenAircrafts(a)  # llamamos esta funcion para saber si es o no schengen
        # no hace falta verificar nada porque ya se ha hecho en la fucnioon de zona_schengen
        if a.schengen:
            schengen += 1
        else:
            no_schengen += 1

    fig = plt.figure()
    plt.bar(["Schengen", "No Schengen"], [schengen, no_schengen], color=['blue', 'red'])
    plt.title("Distribució")
    plt.ylabel("Quantitat")
    return fig

def MapFlights(aircrafts):
    if not aircrafts:
        print("Error: llista buida(Mapflights)")
        messagebox.showwarning("Error", "No hi ha dades per mostrar")
        return
    color_schengen = "ff00ff00"  # verde
    color_no_schengen = "ff0000ff"  # rojo

    #coord de LEBL aeropuerto de llegada
    airports = LoadAirports("Airports.txt")

    destination= Airport( "LEBL",41.29694444444444,  2.0783333333333336)


    with open("flight_map.kml", "w") as f:

        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n')
        for a in aircrafts:
            airport_found = None
            SetSchengenAircrafts(a)
            for ap in airports:
                if ap.icao_code == a.origin:
                    airport_found = ap
                    break


            if airport_found is None:
                continue


            a.longitude = airport_found.longitude
            a.latitude = airport_found.latitude
            f.write(f'  <Placemark>\n')

            if a.schengen:
                f.write(f'  <Style><LineStyle><color>{color_schengen}</color></LineStyle></Style>\n')
            else:
                f.write(f'  <Style><LineStyle><color>{color_no_schengen}</color></LineStyle></Style>\n')

            f.write(f'  <name>Route {a.origin} - LEBL</name>\n')
            f.write(f'  <LineString>\n')
            f.write(f'      <altitudeMode>clampToGround</altitudeMode>\n')#pega la linea al suelo
            f.write(f'      <extrude>1</extrude>\n')  # hace como una pared de la linea al suelo , 1 activado , 0 desactivado
            f.write(f'      <tessellate>1</tessellate>\n')# sige la curvatura de la tierra, sino la atravesara, 1 activado 0 desactivado

#coordenad de  a.long y a.lat desconocidas, son necesarias  pero las listas que tenemos (que nos  dicen de usar en este V2)
# no nos proporciona esa info, he puesto esttas variables para despues acoedarme y cambiarlo, luego,
#la coordenada de llegada si se sabe que es en el aeropuerto LEBL (el de bcn) ya estan declaradas arriba
            f.write(f'          <coordinates>{a.longitude},{a.latitude},0  {destination.longitude},{destination.latitude},0</coordinates>\n')
            f.write(f'  </LineString>\n')
            f.write(f'</Placemark>\n')

        f.write(f'</Document>\n</kml>')
    messagebox.showinfo("Mapa", "Fitxer aircraft.kml generat correctament")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def LongDistanceArrivals(aircrafts):
    vuelos_largos = []
    lat_LEBL = 41.29694444444444
    lon_LEBL = 2.0783333333333336

    if not aircrafts:
        print("Error, llista buida(LongsDistanceArrivals)")
        return []

    for a in aircrafts:
        if a.latitude != None and a.longitude != None:
            distancia = haversine(a.latitude, a.longitude, lat_LEBL, lon_LEBL)
            if distancia > 2000:
                vuelos_largos.append(a)

    return vuelos_largos


