from aircraft import *
if __name__ == "__main__":
    aircrafts = LoadArrivals("arrivals.txt")

    PlotArrivals(aircrafts)
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts)

    largos = LongDistanceArrivals(aircrafts)
    print(f"Vuelos de larga distancia encontrados: {len(largos)}")

    SaveFlights(aircrafts, "vuelos_output.txt")
    MapFlights(aircrafts)

    print("\n--- Operaciones finalizadas ---")
    op = input("Quieres ver el grafico de aerolineas? (s/n): ")
    if op == "s":
        PlotAirlines(aircrafts)