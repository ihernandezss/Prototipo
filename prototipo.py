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

class Envio:
    def __init__(self, id_job, tipo_producto, destino, temperatura, hora_entrega):
        self.id_job = id_job
        self.tipo_producto = tipo_producto
        self.destino = destino
        self.temperatura = temperatura
        self.hora_entrega = hora_entrega
        self.estado = EstadoEnvio.RECIBIDO
        self.ubicacion_actual = ""
        self.guia_aerea = None

    def actualizar_estado(self, nuevo_estado, ubicacion=""):
        self.estado = nuevo_estado
        self.ubicacion_actual = ubicacion

    def agregar_guia_aerea(self, guia_aerea):
        self.guia_aerea = guia_aerea

class SistemaSeguimiento:
    def __init__(self):
        self.envios = {}
        self.usuarios = {}

    def agregar_envio(self, envio):
        self.envios[envio.id_job] = envio

    def agregar_usuario(self, usuario):
        self.usuarios[usuario.nombre] = usuario

    def actualizar_estado_envio(self, id_job, nuevo_estado, ubicacion="", usuario=None):
        if id_job in self.envios:
            if usuario and usuario.rol in [Rol.PERSONAL_LOGISTICA, Rol.GERENTE_COMERCIAL, Rol.CONDUCTOR, Rol.QUIMICO]:
                self.envios[id_job].actualizar_estado(nuevo_estado, ubicacion)
                print(f"Envío {id_job} actualizado a {nuevo_estado.value} por {usuario.nombre}")
            else:
                print("No autorizado para actualizar el estado del envío")
        else:
            print("Envío no encontrado")

    def obtener_info_envio(self, id_job, usuario):
        if id_job in self.envios:
            envio = self.envios[id_job]
            if usuario.rol in [Rol.CLIENTE, Rol.DESTINATARIO]:
                return f"JOB: {envio.id_job}, Estado: {envio.estado.value}, Temperatura: {envio.temperatura}, Hora de entrega: {envio.hora_entrega}"
            elif usuario.rol in [Rol.PERSONAL_LOGISTICA, Rol.GERENTE_COMERCIAL, Rol.CONDUCTOR, Rol.QUIMICO]:
                return f"JOB: {envio.id_job}, Tipo: {envio.tipo_producto}, Destino: {envio.destino}, Estado: {envio.estado.value}, Temperatura: {envio.temperatura}, Hora de entrega: {envio.hora_entrega}, Ubicación actual: {envio.ubicacion_actual}"
            else:
                return "No autorizado para ver la información del envío"
        else:
            return "Envío no encontrado"

    def agregar_guia_aerea(self, id_job, guia_aerea, usuario):
        if id_job in self.envios and usuario.rol in [Rol.PERSONAL_LOGISTICA, Rol.GERENTE_COMERCIAL]:
            self.envios[id_job].agregar_guia_aerea(guia_aerea)
            print(f"Guía aérea agregada al envío {id_job}")
        else:
            print("No autorizado para agregar guía aérea o envío no encontrado")

def menu_destinatario(sistema, usuario):
    while True:
        print("\n--- Menú Destinatario ---")
        print("1. Observar estado del envío")
        print("2. Ver información del producto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1" or opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job, usuario))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_transportista(sistema, usuario):
    while True:
        print("\n--- Menú Transportista ---")
        print("1. Editar estado del envío")
        print("2. Ver información del cliente")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_job = input("Ingrese el ID del envío: ")
            nuevo_estado = input("Ingrese el nuevo estado (RECIBIDO, EN_TRANSITO_AEREO, EN_TRANSITO_TERRESTRE, EN_CENTRO_LOGISTICO, EN_CAMINO, ENTREGADO): ")
            ubicacion = input("Ingrese la ubicación actual: ")
            sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion, usuario)
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job, usuario))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_logistica(sistema, usuario):
    while True:
        print("\n--- Menú Logística ---")
        print("1. Ingresar nuevo pedido")
        print("2. Ingresar nuevo cliente")
        print("3. Ver información del envío")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_job = input("Ingrese el ID del envío: ")
            tipo_producto = input("Ingrese el tipo de producto: ")
            destino = input("Ingrese el destino: ")
            temperatura = input("Ingrese la temperatura requerida: ")
            hora_entrega = input("Ingrese la hora de entrega (YYYY-MM-DD HH:MM): ")
            hora_entrega = datetime.datetime.strptime(hora_entrega, "%Y-%m-%d %H:%M")
            nuevo_envio = Envio(id_job, tipo_producto, destino, temperatura, hora_entrega)
            sistema.agregar_envio(nuevo_envio)
            print(f"Nuevo envío {id_job} ingresado")
        elif opcion == "2":
            nombre = input("Ingrese el nombre del cliente: ")
            nuevo_cliente = Usuario(nombre, Rol.CLIENTE)
            sistema.agregar_usuario(nuevo_cliente)
            print(f"Nuevo cliente {nombre} ingresado")
        elif opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job, usuario))
        elif opcion == "4":
            break
        else:
            print("Opción no válida")

def menu_quimico(sistema, usuario):
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
            sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion, usuario)
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job, usuario))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_principal():
    sistema = SistemaSeguimiento()
    
    # Agregar algunos usuarios de ejemplo
    sistema.agregar_usuario(Usuario("Juan", Rol.DESTINATARIO))
    sistema.agregar_usuario(Usuario("Maria", Rol.CONDUCTOR))
    sistema.agregar_usuario(Usuario("Carlos", Rol.PERSONAL_LOGISTICA))
    sistema.agregar_usuario(Usuario("Ana", Rol.QUIMICO))

    while True:
        print("\n--- Sistema de Seguimiento ---")
        print("1. Iniciar sesión")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese su nombre: ")
            if nombre in sistema.usuarios:
                usuario = sistema.usuarios[nombre]
                if usuario.rol == Rol.DESTINATARIO:
                    menu_destinatario(sistema, usuario)
                elif usuario.rol == Rol.CONDUCTOR:
                    menu_transportista(sistema, usuario)
                elif usuario.rol == Rol.PERSONAL_LOGISTICA:
                    menu_logistica(sistema, usuario)
                elif usuario.rol == Rol.QUIMICO:
                    menu_quimico(sistema, usuario)
                else:
                    print("Rol no reconocido")
            else:
                print("Usuario no encontrado")
        elif opcion == "2":
            print("Gracias por usar el Sistema de Seguimiento")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu_principal()