from tkinter import *
from tkinter import filedialog, messagebox
from aircraft import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# DATOS GLOBALES de aircrafts y de airports
llista_aeroports = []
llista_vuelos = []

current_canvas = None  # para controlar el gráfico al iniciar, = ninguno

#para Airport.py--------------------------------------------------------------------------------------------------------
def carregar_aeroports():
    global llista_aeroports
    nom_fitxer = filedialog.askopenfilename()
    if nom_fitxer:
        llista_aeroports = LoadAirports(nom_fitxer)
        for a in llista_aeroports:
            SetSchengenAirports(a)
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_aeroports)} aeroports.")


def generar_kml():
    if llista_aeroports:
        MapAirports(llista_aeroports)
        messagebox.showinfo("Mapa", "Fitxer airports_map.kml generat correctament")

#para Aircraft.py---------------------------------------------------------------------------------------------------
def carregar_vuelos():
    global llista_vuelos
    nom_fitxer = filedialog.askopenfilename()
    if nom_fitxer:
        llista_vuelos = LoadArrivals(nom_fitxer)
        for a in llista_vuelos:
            SetSchengenAircrafts(a)
        messagebox.showinfo("Èxit", f"S'han carregat {len(llista_vuelos)} vols .")


# Parte de graficos  (EMBED)
def mostrar_figura(fig):
    global current_canvas# que al inicio es none

    # limpiar gráfico anterior
    for widget in graph_frame.winfo_children(): #por todos los elementos que estan dentro de la zona de graficos
        widget.destroy()#destruye esos elementos

    current_canvas = FigureCanvasTkAgg(fig, master=graph_frame)#el grafico sera, dentro del tk, figura, dentro de la zona de graficos
    current_canvas.draw()#muestra el grafico
    current_canvas.get_tk_widget().pack(fill=BOTH, expand=True)#expande el grafico en todos lados y si se modifica las diemnsiones de la pestaña, el grafico tambien


def PlotAirports_embedded():
    fig = PlotAirports(llista_aeroports)  # debe devolver fig
    mostrar_figura(fig)


def PlotArrivals_embedded():
    fig = PlotArrivals(llista_vuelos)
    mostrar_figura(fig)


def PlotAirlines_embedded():
    fig = PlotAirlines(llista_vuelos)
    mostrar_figura(fig)


def PlotFlightsType_embedded():
    fig = PlotFlightsType(llista_vuelos)
    mostrar_figura(fig)


def clear_graph():
    for widget in graph_frame.winfo_children():
        widget.destroy()
    Label(graph_frame, text="(Aquí aparecerán los gráficos)", font=("Arial", 14)).pack(expand=True)



# interfaz grafica
window = Tk()
window.title("EETAC Dashboard")
window.geometry("1500x900")

window.rowconfigure(0, weight=3)  # zona de gráficos
window.rowconfigure(1, weight=2)  # panel inferior para botones, etc
window.columnconfigure(0, weight=1)



# zona donde esta el grafico (zona superior)

graph_frame = Frame(window, bg="white", relief="solid", bd=2)#relief soft signnifica q tendra borde delimitado
graph_frame.grid(row=0, column=0, sticky="nsew")

Label(graph_frame, text=" visualiçasio", font=("Arial", 16)).pack(expand=True)


# parte inferior
bottom_frame = Frame(window)
bottom_frame.grid(row=1, column=0, sticky="nsew")

bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)
bottom_frame.columnconfigure(2, weight=1)
bottom_frame.rowconfigure(0, weight=1)


# subtema de descargar archivos
download_frame = LabelFrame(bottom_frame, text="Descarregar archius", padx=10, pady=10)
download_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

Button(download_frame, text="Carregar base d'aeroports", command=carregar_aeroports).pack(fill=X,pady = 4, ipady=16)
Button(download_frame, text="Carregar vols diaris", command=carregar_vuelos).pack(fill=X,pady = 4, ipady=16)
Button(download_frame, text="Exportar Google Earth", command=generar_kml).pack(fill=X,pady = 4, ipady=16)
Button(download_frame,text="Generar mapa KML",command=lambda: MapFlights(llista_vuelos)).pack(fill=X, pady=4, ipady=5)

# subtema de botones
charts_frame = LabelFrame(bottom_frame, text="Botons", padx=10, pady=10)
charts_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

Button(charts_frame, text="Veure Estadístiques", command=PlotAirports_embedded).pack(fill=X,pady = 4, ipady=16)
Button(charts_frame, text="Mostrar Histograma Horari", command=PlotArrivals_embedded).pack(fill=X,pady = 4, ipady=16)
Button(charts_frame, text="Gràfic per Aerolínia", command=PlotAirlines_embedded).pack(fill=X,pady = 4, ipady=16)
Button(charts_frame, text="Vols procedents de països Schengen", command=PlotFlightsType_embedded).pack(fill=X,pady = 4, ipady=16)
Button(charts_frame, text="Vuidar grafic", command=clear_graph).pack(fill=X,pady = 4, ipady=16)


# SALIR
exit_frame = Frame(bottom_frame)
exit_frame.grid(row=0, column=2, sticky="se")

Button(exit_frame, text="Sortir", bg="red", fg="white", command=window.destroy).pack(anchor="se")#lugar de posicion  sur-este


# iniciar vacío
clear_graph()

window.mainloop()