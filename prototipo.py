import datetime
from enum import Enum

class EstadoEnvio(Enum):
    RECIBIDO = "Recibimos tu envío"
    EN_TRANSITO_AEREO = "En reparto aéreo"
    EN_TRANSITO_TERRESTRE = "Viajando a tu destino"
    EN_CENTRO_LOGISTICO = "En centro logístico (bodega)"
    EN_CAMINO = "En camino hacia ti"
    ENTREGADO = "Entregado"

class Rol(Enum):
    PERSONAL_LOGISTICA = "Personal de logística"
    GERENTE_COMERCIAL = "Gerente Comercial"
    DESTINATARIO = "Destinatario"
    CONDUCTOR = "Conductor"
    CLIENTE = "Cliente"
    QUIMICO = "Químico"

class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

class Cliente(Usuario):
    def __init__(self, nombre, identificador):
        super().__init__(nombre, Rol.CLIENTE)
        self.identificador = identificador
        self.envios = []

class Transportista(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, Rol.CONDUCTOR)

class Quimico(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, Rol.QUIMICO)

class CambioEstado:
    def __init__(self, estado, fecha, ubicacion):
        self.estado = estado
        self.fecha = fecha
        self.ubicacion = ubicacion

class Envio:
    def __init__(self, id_job, guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega, transportista=None):
        self.id_job = id_job
        self.guia_aerea = guia_aerea
        self.cliente = cliente
        self.tipo_producto = tipo_producto
        self.destino = destino
        self.temperatura = temperatura
        self.hora_entrega = hora_entrega
        self.transportista = transportista
        self.estado_actual = EstadoEnvio.RECIBIDO
        self.historial_estados = [CambioEstado(EstadoEnvio.RECIBIDO, datetime.datetime.now(), "Centro de distribución")]
        self.ubicacion_actual = "Centro de distribución"

    def actualizar_estado(self, nuevo_estado, ubicacion):
        self.estado_actual = nuevo_estado
        self.ubicacion_actual = ubicacion
        self.historial_estados.append(CambioEstado(nuevo_estado, datetime.datetime.now(), ubicacion))

    def asignar_transportista(self, transportista):
        self.transportista = transportista

class SistemaSeguimiento:
    def __init__(self):
        self.envios = {}
        self.usuarios = {}
        self.clientes = {}
        self.transportistas = []
        self.quimicos = []

    def agregar_usuario(self, usuario):
        self.usuarios[usuario.nombre] = usuario
        if isinstance(usuario, Cliente):
            self.clientes[usuario.identificador] = usuario
        elif isinstance(usuario, Transportista):
            self.transportistas.append(usuario)
        elif isinstance(usuario, Quimico):
            self.quimicos.append(usuario)

    def crear_envio(self, guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega):
        id_job = f"JOB{len(self.envios) + 1:03}"
        nuevo_envio = Envio(id_job, guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega)
        self.envios[id_job] = nuevo_envio
        cliente.envios.append(nuevo_envio)
        return id_job

    def actualizar_estado_envio(self, id_job, nuevo_estado, ubicacion):
        if id_job in self.envios:
            self.envios[id_job].actualizar_estado(nuevo_estado, ubicacion)
            return True
        return False

    def obtener_info_envio(self, id_job):
        if id_job in self.envios:
            envio = self.envios[id_job]
            return f"JOB: {envio.id_job}, Guía Aérea: {envio.guia_aerea}, Cliente: {envio.cliente.nombre}, " \
                   f"Tipo: {envio.tipo_producto}, Destino: {envio.destino}, Estado: {envio.estado_actual.value}, " \
                   f"Temperatura: {envio.temperatura}, Hora de entrega: {envio.hora_entrega}, " \
                   f"Ubicación actual: {envio.ubicacion_actual}"
        return "Envío no encontrado"

    def obtener_historial_envio(self, id_job):
        if id_job in self.envios:
            envio = self.envios[id_job]
            historial = [f"{cambio.fecha} - {cambio.estado.value} en {cambio.ubicacion}" for cambio in envio.historial_estados]
            return "\n".join(historial)
        return "Envío no encontrado"

def menu_cliente(sistema, cliente):
    while True:
        print("\n--- Menú Cliente ---")
        print("1. Ver mis pedidos")
        print("2. Ver estado de un envío")
        print("3. Ver historial de un envío")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            if cliente.envios:
                for envio in cliente.envios:
                    print(sistema.obtener_info_envio(envio.id_job))
            else:
                print("No tiene pedidos registrados.")
        elif opcion == "2" or opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            if opcion == "2":
                print(sistema.obtener_info_envio(id_job))
            else:
                print(sistema.obtener_historial_envio(id_job))
        elif opcion == "4":
            break
        else:
            print("Opción no válida")

def menu_destinatario(sistema):
    while True:
        print("\n--- Menú Destinatario ---")
        print("1. Ver estado de un envío")
        print("2. Ver historial de un envío")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1" or opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            if opcion == "1":
                print(sistema.obtener_info_envio(id_job))
            else:
                print(sistema.obtener_historial_envio(id_job))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_transportista(sistema, transportista):
    while True:
        print("\n--- Menú Transportista ---")
        print("1. Editar estado del envío")
        print("2. Ver información del envío")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_job = input("Ingrese el ID del envío: ")
            nuevo_estado = input("Ingrese el nuevo estado (RECIBIDO, EN_TRANSITO_AEREO, EN_TRANSITO_TERRESTRE, EN_CENTRO_LOGISTICO, EN_CAMINO, ENTREGADO): ")
            ubicacion = input("Ingrese la ubicación actual: ")
            if sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion):
                print("Estado actualizado con éxito")
            else:
                print("No se pudo actualizar el estado")
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_logistica(sistema):
    while True:
        print("\n--- Menú Logística ---")
        print("1. Ingresar nuevo cliente")
        print("2. Crear nuevo envío")
        print("3. Ver información del envío")
        print("4. Agregar empleado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese el nombre del cliente: ")
            identificador = input("Ingrese el identificador del cliente: ")
            nuevo_cliente = Cliente(nombre, identificador)
            sistema.agregar_usuario(nuevo_cliente)
            print(f"Nuevo cliente {nombre} ingresado")
        elif opcion == "2":
            identificador_cliente = input("Ingrese el identificador del cliente: ")
            if identificador_cliente in sistema.clientes:
                cliente = sistema.clientes[identificador_cliente]
                guia_aerea = input("Ingrese el número de guía aérea: ")
                tipo_producto = input("Ingrese el tipo de producto: ")
                destino = input("Ingrese el destino: ")
                temperatura = input("Ingrese la temperatura requerida: ")
                hora_entrega = input("Ingrese la hora de entrega (YYYY-MM-DD HH:MM): ")
                hora_entrega = datetime.datetime.strptime(hora_entrega, "%Y-%m-%d %H:%M")
                id_job = sistema.crear_envio(guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega)
                print(f"Nuevo envío creado con ID: {id_job}")
            else:
                print("Cliente no encontrado")
        elif opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "4":
            nombre = input("Ingrese el nombre del empleado: ")
            rol = input("Ingrese el rol del empleado (CONDUCTOR/QUIMICO): ")
            if rol == "CONDUCTOR":
                nuevo_empleado = Transportista(nombre)
            elif rol == "QUIMICO":
                nuevo_empleado = Quimico(nombre)
            else:
                print("Rol no válido")
                continue
            sistema.agregar_usuario(nuevo_empleado)
            print(f"Nuevo empleado {nombre} ingresado como {rol}")
        elif opcion == "5":
            break
        else:
            print("Opción no válida")

def menu_quimico(sistema, quimico):
    while True:
        print("\n--- Menú Químico ---")
        print("1. Editar estado del envío")
        print("2. Ver información del envío")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_job = input("Ingrese el ID del envío: ")
            nuevo_estado = input("Ingrese el nuevo estado (RECIBIDO, EN_TRANSITO_AEREO, EN_TRANSITO_TERRESTRE, EN_CENTRO_LOGISTICO, EN_CAMINO, ENTREGADO): ")
            ubicacion = input("Ingrese la ubicación actual: ")
            if sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion):
                print("Estado actualizado con éxito")
            else:
                print("No se pudo actualizar el estado")
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_principal():
    sistema = SistemaSeguimiento()
    
    while True:
        print("\n--- Sistema de Seguimiento ---")
        print("1. Cliente")
        print("2. Destinatario")
        print("3. Transportista")
        print("4. Logística")
        print("5. Químico")
        print("6. Salir")
        opcion = input("Seleccione su tipo de usuario: ")
        
        if opcion == "1":
            identificador = input("Ingrese su identificador de cliente: ")
            if identificador in sistema.clientes:
                menu_cliente(sistema, sistema.clientes[identificador])
            else:
                print("Cliente no encontrado")
        elif opcion == "2":
            menu_destinatario(sistema)
        elif opcion == "3":
            if sistema.transportistas:
                print("Transportistas disponibles:")
                for i, transportista in enumerate(sistema.transportistas):
                    print(f"{i+1}. {transportista.nombre}")
                seleccion = int(input("Seleccione un transportista: ")) - 1
                if 0 <= seleccion < len(sistema.transportistas):
                    menu_transportista(sistema, sistema.transportistas[seleccion])
                else:
                    print("Selección no válida")
            else:
                print("No hay personal de transporte registrado")
        elif opcion == "4":
            menu_logistica(sistema)
        elif opcion == "5":
            if sistema.quimicos:
                print("Químicos disponibles:")
                for i, quimico in enumerate(sistema.quimicos):
                    print(f"{i+1}. {quimico.nombre}")
                seleccion = int(input("Seleccione un químico: ")) - 1
                if 0 <= seleccion < len(sistema.quimicos):
                    menu_quimico(sistema, sistema.quimicos[seleccion])
                else:
                    print("Selección no válida")
            else:
                print("No hay personal químico registrado")
        elif opcion == "6":
            print("Gracias por usar el Sistema de Seguimiento")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu_principal()