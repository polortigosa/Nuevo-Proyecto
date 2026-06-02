from aircraft import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []

class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []

class BoardingArea:
    def __init__(self, name, type):
        self.name = name
        self.type = type #si es schengen o no
        self.gates = []

class Gate:
    def __init__(self, name, numero):
        self.name = name
        self.occupied = False
        self.aircraft_id =""
        self.numero = numero

def SetGates (area, init_gate, end_gate, prefix): #nombre de cada una de las puertas en una lista
    if end_gate <= init_gate:
        return -1

    area.gates = []#lista de las puertas

    for numero in range(init_gate, end_gate + 1): # +1 porque en el range no se tiene en cuenta el ultimio valor
        gate_name = f"{prefix}{numero}"# el nombe de cada puerta
        gate = Gate(gate_name,numero)
        area.gates.append(gate)# mete en una lista, las puertas que hay metiendo en la lista toda la informacion en la clase
    return 0

def LoadAirlines (terminal, t_name):# guarda los icao de esa terminal en una lista en el apartado (la clase)  de termianl
    #abre el archido de la terminal correspondiente,
    # mira el  code icao de cada una de las compañias que estan en ese archido y ,por lo tanto, son de en esa terminal
    #guarda la informacion en una lista que esta en la classe de termianl
    filename = f"{t_name}_Airlines.txt" #para que abra el archivo de la terminal determinada T1 /T2

    try:
        file = open(filename, "r")
    except FileNotFoundError:
        return -1

    airlines_temp = []

    for line in file: #que de cada linea del archivo y que elimine espacios y saltos de linea
        line = line.strip()
        if line == "": #si esta vacia
            continue
        parts = line.split()
        airline_code = parts[-1]# ICAO code siempre esta al final
        airlines_temp.append(airline_code)
    file.close()
    terminal.airlines = airlines_temp
    return 0

def LoadAirportStructure (filename):# devuelve Un objeto BarcelonaAP que contiene el código del aeropuerto  (LEBL)
    # , una lista de terminales, y cada terminal incluye aerolíneas (LoadAirlines) y
    # áreas de embarque, donde cada área tiene su tipo (Schengen/no Schengen), su rango de puertas y las puertas creadas (SetGates).

    # abre el archivo y mira que informacion del aeropuertos hay
    # el codigo del aeropuerto, cuantas terminales hay, etc
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        return -1

    first_line = file.readline().strip().split()
    airport_code = first_line[0]
    bcn = BarcelonaAP(airport_code)# es bcn porque sabemos que el codigo de aeropuerto en este caso es LEBL que es el de bcn
    lines = file.readlines()

    i = 0
    while i < len(lines):
        parts = lines[i].strip().split()
        if parts[0] == "Terminal":
            terminal_name = parts[1] #guarda el nombre de la terminal T1/T2
            num_areas = int(parts[2]) #guarda cuantas areas tiene
            terminal = Terminal(terminal_name) #mete la info guardada en la clase

            LoadAirlines(terminal, terminal_name) #ejecuta la funcion para leer el archivo correspondiente a esa terminal

            for j in range(num_areas):
                i += 1
                area_line = lines[i].strip().split()
                area_name = area_line[1]# si es A B C D ...
                area_type = area_line[2] # si es schengen o no
                init_gate = int(area_line[4]) # la inicial
                end_gate = int(area_line[6])# la final

                boarding_area = BoardingArea(area_name, area_type)#guarda los datos con la clase
                prefix = f"{terminal_name}{area_name}G"#genera el nombre de la puerta sin tener la posicon en esa terminal

                SetGates(boarding_area, init_gate, end_gate, prefix) #ejecuta la funcion para tener la infromacion completa de cada puerta
                terminal.boarding_areas.append(boarding_area)#dentro de el objeto terminal, en la lsita de boarding_areas, mete la info
            bcn.terminals.append(terminal)# mete la ppsicon de la terminal dnetro del aeropuerto
        i += 1
    file.close()
    return bcn

def GateOccupancy (bcn):#genera una lista con el lugar exacto d ela puertta, su estado,  y el id si esta ocupado
    occupancy_list = []
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                if gate.occupied:
                    status = "Occupied"
                else:
                    status = "Free"
                occupancy_list.append([gate.name, status, gate.aircraft_id])
    return occupancy_list

def IsAirlineInTerminal (terminal, name):#mira si despeus de verificar, si esta la aerolinea en esa terminal
    if name == "": #  nombre de al aerolinea interesada
        return False
    if len(terminal.airlines) == 0: # si esta vacio el archivo de informacion de la terminal especifica--> no tiene aerolineas esa terminal
        return False

    return name in terminal.airlines# si tenemos aerolinea interesada y lista no esta vacia, mirar si esta dentro de la lista --> true/false

def SearchTerminal (bcn, name): # mira si esta la aerolinea en alguna de las terminales, y si esta te dice cual
    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name
    return ""

def AssignGate(bcn, aircraft):#te dice el nombre y especificaciones si estaba vacia y pasa a ocuparla, si estava ocupada no la puede ocupar
    terminal_name = SearchTerminal(bcn, aircraft.company)

    if terminal_name == "":# si no esta la aerolinea en ninguna terminal, esta vacia y si esta vacia, -1
        return -1# no encontrado
    SetSchengenAircrafts(aircraft)#llamamos a la funcion para poder determinar el tipo de avion schenguen o no
    if aircraft.schengen:
        flight_type = "Schengen"
    else:
        flight_type = "non-Schengen"
    for terminal in bcn.terminals:
        if terminal.name == terminal_name:
            for area in terminal.boarding_areas:
                if area.type == flight_type:
                    for gate in area.gates:# por cada puerta en el area de puertas
                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            return gate.name
    return -1





def PlotTerminal_visual(bcn, name):
    # Busca la terminal por nombre
    terminal = None
    for t in bcn.terminals:
        if t.name == name:
            terminal = t
    if not terminal:
        return None

    areas = terminal.boarding_areas
    num_areas = len(areas)

    # Dimensiones generales del canvas
    fig_width = max(14, num_areas * 4.5)
    fig, ax = plt.subplots(figsize=(fig_width, 7))  # Reducido un poco el alto para ajustarse a la proporción
    ax.set_xlim(0, fig_width)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Fondo blanco limpio como la imagen de referencia
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Color azul corporativo de la imagen
    azul_terminal = '#346182'

    # Texto de la Terminal arriba a la izquierda (ej: "T1")
    ax.text(fig_width/2, 8.5+1/2, f"Terminal: {name}", ha='center', va='center', fontsize=28, color='black', zorder=4)

    # Barra superior de la terminal (el techo horizontal plano)
    terminal_bar_y = 8.5
    bar_height = 1
    ax.add_patch(mpatches.Rectangle((0.5, terminal_bar_y), fig_width - 1.0, bar_height,
                                    linewidth=0, facecolor=azul_terminal, zorder=3))

    # Distribuye las boarding areas horizontalmente
    area_spacing = (fig_width - 1.0) / num_areas
    area_col_x = [0.5 + area_spacing * i + area_spacing / 2 for i in range(num_areas)]

    trunk_width = 0.45  # Más grueso como en la foto
    gate_w = 0.9  # Rectángulo de estado
    gate_h = 0.25
    gate_arm_len = 0.6  # Longitud del brazo horizontal azul
    trunk_top_y = terminal_bar_y + 0.1  # Conexión perfecta con la barra superior
    trunk_bot_y = 1.5

    for idx, area in enumerate(areas):
        cx = area_col_x[idx]  # Centro horizontal de esta boarding area

        # Tronco vertical plano de la boarding area
        ax.add_patch(mpatches.Rectangle(
            (cx - trunk_width / 2, trunk_bot_y), trunk_width, trunk_top_y - trunk_bot_y,
            linewidth=0, facecolor=azul_terminal, zorder=2))

        # Etiqueta del nombre del area debajo del tronco (ej: "T1BAa")
        ax.text(cx, trunk_bot_y - 0.4, f"{name}BA{area.name}",
                ha='center', va='top', fontsize=16, color='black')

        # Distribuye los gates a lo largo del tronco
        num_gates = len(area.gates)
        if num_gates == 0:
            continue

        # Espacio disponible para los gates
        usable_top = terminal_bar_y - 0.6
        usable_bot = trunk_bot_y + 0.5
        usable_h = usable_top - usable_bot

        if num_gates == 1:
            gate_ys = [(usable_top + usable_bot) / 2]
        else:
            step = usable_h / (num_gates - 1) if num_gates > 1 else 0
            gate_ys = [usable_top - i * step for i in range(num_gates)]

        # Alterna lado izquierdo / derecho para los gates
        for gi, gate in enumerate(area.gates):
            gy = gate_ys[gi]
            side = 1 if gi % 2 == 0 else -1  # 1=derecha, -1=izquierda

            # Brazo horizontal grueso desde el tronco
            arm_x_start = cx + side * (trunk_width / 2)
            arm_x_end = cx + side * (trunk_width / 2 + gate_arm_len)
            ax.plot([arm_x_start, arm_x_end], [gy, gy],
                    color=azul_terminal, linewidth=4, zorder=2)  # Más grueso

            # Color plano sin bordes según ocupación
            if gate.occupied:
                gate_color = '#e74c3c'  # Rojo plano
            else:
                gate_color = '#5cb85c'  # Verde plano de la foto

            # Ajustar ancho del rectángulo según el texto
            current_gate_w = gate_w

            if gate.occupied and gate.aircraft_id:
                current_gate_w = 0.18 * len(gate.aircraft_id)

            # Rectángulo indicador de estado (separado un poquito del brazo)
            gap = 0.15 # separacion del cubo con el brazo
            rect_x = arm_x_end + gap if side == 1 else arm_x_end - current_gate_w  - gap

            rect = mpatches.Rectangle(
                (rect_x, gy - gate_h / 2), current_gate_w , gate_h,
                linewidth=0, facecolor=gate_color, zorder=3)
            ax.add_patch(rect)

            # Nombre de la puerta justo encima del brazo horizontal
            label_x = arm_x_start + side * 0.1
            ha_align = 'left' if side == 1 else 'right'
            ax.text(label_x, gy +0.03,f"{gate.numero}G" , ha=ha_align, va='bottom',
                    fontsize=9, color='black', fontweight='normal', zorder=4)

            # Si está ocupado, el ID del avión (DALEN) se muestra en negro/gris al lado izquierdo del bloque rojo
            if gate.occupied and gate.aircraft_id:
                id_x = rect_x + 0.1 if side == 1 else rect_x + current_gate_w  - 0.1  # Ajustado a la izquierda del rectángulo rojo
                ax.text(id_x, gy, gate.aircraft_id, ha= 'left' if side == 1 else 'right' , va='center', fontsize= 9, color='black', zorder=4)

    plt.tight_layout()
    return fig

def FreeGate(bcn, aircraft_id):
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                if gate.occupied and gate.aircraft_id == aircraft_id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    return 1
    return -1

def AssignNightGates(bcn, night_aircrafts):
    # Si la lista está vacía devolvemos error
    if not night_aircrafts:
        return -1

    for ac in night_aircrafts:

        # Solo deben procesarse vuelos nocturnos de salida.
        # Si tiene datos de llegada se ignora.
        if ac.time:
            continue

        # Para que la función AssignGate funcione con aviones nocturnos:
        # como no tienen un 'origin' inicial ya que se han quedado
        # en el aeropuerto por la noche, copiamos temporalmente su
        # 'destino' al 'origin' para estudiar correctamente si van
        # a zona Schengen o No-Schengen al despegar.
        original_origin = ac.origin
        ac.origin = ac.destino
        AssignGate(bcn, ac)
        ac.origin = original_origin

    return 1


def AssignGatesAtTime(bcn, movements, h):
    vuelos_sin_gate = 0

    # 1. Liberar puertas de los aviones que despegan a la hora 'h'
    for ac in movements:
        if ac.salida:
            try:
                hour_salida = int(ac.salida.split(":")[0])
                if hour_salida == h:
                    FreeGate(bcn, ac.id)
            except:
                pass

    # 2. Asignar puertas a los aviones que aterrizan a la hora 'h'
    for ac in movements:
        if ac.time:
            try:
                hour_arrival = int(ac.time.split(":")[0])
                if hour_arrival == h:
                    resultado = AssignGate(bcn, ac)
                    if resultado == -1:
                        vuelos_sin_gate += 1
            except:
                pass

    return vuelos_sin_gate

def BuildAirportStateAtHour(bcn, movements, hour):

    # Reiniciar todas las puertas
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate.occupied = False
                gate.aircraft_id = ""

    # Ubicar los aviones nocturnos que ya están en las puertas al inicio del día
    nocturnos = NightAircraft(movements)

    if nocturnos != -1:
        AssignNightGates(bcn, nocturnos)

    # Ejecutar la simulación desde las 00:00 hasta la hora indicada
    for h in range(hour + 1):
        AssignGatesAtTime(bcn, movements, h)
    return bcn

def PlotTerminalAtHour(bcn, movements, terminal_name, hour):
    BuildAirportStateAtHour(bcn, movements, hour)

    return PlotTerminal_visual(bcn, terminal_name)

def PlotDayOccupancy(bcn, movements):

    # Reiniciar todas las puertas a libres antes de simular las 24 horas
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate.occupied = False
                gate.aircraft_id = ""

    # Ubicar los aviones nocturnos que ya están en las puertas al inicio del día
    nocturnos = NightAircraft(movements)

    if nocturnos != -1:
        AssignNightGates(bcn, nocturnos)

    ocupacion_por_hora = []
    vuelos_sin_gate_por_hora = []

    # Ejecutar la simulación paso a paso de 0 a 23 horas
    for h in range(24):

        rechazados = AssignGatesAtTime(bcn, movements, h)

        # Contar cuántas puertas están ocupadas al terminar la hora actual
        count = 0

        for terminal in bcn.terminals:
            for area in terminal.boarding_areas:
                for gate in area.gates:
                    if gate.occupied:
                        count += 1

        ocupacion_por_hora.append(count)
        vuelos_sin_gate_por_hora.append(rechazados)

    # Generar la gráfica solicitada
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(range(24),ocupacion_por_hora,alpha=0.5,label='Puertas Ocupadas')

    ax.plot(range(24),ocupacion_por_hora,marker='o',linewidth=2,label='Evolución Temporal')

    ax.plot(range(24),vuelos_sin_gate_por_hora,marker='s',linewidth=2,label='Aviones sin gate')

    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Cantidad")
    ax.set_title("Ocupación Dinámica del Aeropuerto LEBL (24h)")
    ax.set_xticks(range(24))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    return fig


def PlotControlTowerDashboard(bcn, movements):

    # Reiniciamos todas las puertas
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate.occupied = False
                gate.aircraft_id = ""

    total_gates = 0

    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            total_gates += len(area.gates)

    if total_gates == 0:
        return None

    # Aviones nocturnos
    nocturnos = NightAircraft(movements)

    if nocturnos != -1:
        AssignNightGates(bcn, nocturnos)

    ocupacion_por_hora = []
    vuelos_sin_gate_por_hora = []

    for h in range(24):

        vuelos_sin_gate = AssignGatesAtTime(bcn, movements, h)

        ocupados = 0

        for terminal in bcn.terminals:
            for area in terminal.boarding_areas:
                for gate in area.gates:
                    if gate.occupied:
                        ocupados += 1

        ocupacion_por_hora.append(ocupados)
        vuelos_sin_gate_por_hora.append(vuelos_sin_gate)

    max_ocupacion = max(ocupacion_por_hora)
    hora_pico = ocupacion_por_hora.index(max_ocupacion)

    saturacion = (max_ocupacion / total_gates) * 100
    total_sin_gate = sum(vuelos_sin_gate_por_hora)

    # Gráfico
    fig = plt.figure(figsize=(13, 7))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.bar(range(24), ocupacion_por_hora)
    ax1.plot(range(24), ocupacion_por_hora, marker="o")
    ax1.axvline(hora_pico, linestyle="--")
    ax1.set_title("Ocupació de gates durant el dia")
    ax1.set_xlabel("Hora")
    ax1.set_ylabel("Gates ocupats")
    ax1.set_xticks(range(24))
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.bar(range(24), vuelos_sin_gate_por_hora)
    ax2.set_title("Vols sense gate assignada")
    ax2.set_xlabel("Hora")
    ax2.set_ylabel("Vols rebutjats")
    ax2.set_xticks(range(24))
    ax2.grid(True, linestyle="--", alpha=0.4)

    # Ocupación por terminal al final de la simulación
    terminal_names = []
    terminal_values = []

    for terminal in bcn.terminals:

        ocupados_terminal = 0

        for area in terminal.boarding_areas:
            for gate in area.gates:
                if gate.occupied:
                    ocupados_terminal += 1

        terminal_names.append(terminal.name)
        terminal_values.append(ocupados_terminal)

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.bar(terminal_names, terminal_values)
    ax3.set_title("Ocupació final per terminal")
    ax3.set_xlabel("Terminal")
    ax3.set_ylabel("Gates ocupats")
    ax3.grid(True, axis="y", linestyle="--", alpha=0.4)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis("off")

    texto = ("CONTROL TOWER DASHBOARD\n\n"f"Hora crítica: {hora_pico}:00\n\n"f"Màxima ocupació: {max_ocupacion}/{total_gates} gates\n\n"
        f"Saturació màxima: {saturacion:.1f}%\n\n"f"Vols sense gate: {total_sin_gate}")

    ax4.text(0.05,0.95,texto,va="top",ha="left",fontsize=13,bbox=dict(boxstyle="round",facecolor="#f2f2f2",edgecolor="black"))

    fig.suptitle("Control Tower Dashboard - Aeroport LEBL",fontsize=16,fontweight="bold")
    plt.tight_layout()
    return fig

def ResetAirport(bcn):
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate.occupied = False
                gate.aircraft_id = ""