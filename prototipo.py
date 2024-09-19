import datetime
from enum import Enum

class EstadoEnvio(Enum):
    RECIBIDO = "Recibimos tu envío"
    EN_REPARTO_AEREO = "En reparto aéreo"
    VIAJANDO_A_TU_DESTINO = "Viajando a tu destino"
    EN_CENTRO_LOGISTICO = "En centro logístico (bodega)"
    EN_CAMINO_HACIA_TI = "En camino hacia ti"
    ENTREGADO = "Entregado"
    EN_RETRASO="En retraso"

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

class GerenteComercial(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, Rol.GERENTE_COMERCIAL)

class CambioEstado:
    def __init__(self, estado, fecha, ubicacion):
        self.estado = estado
        self.fecha = fecha
        self.ubicacion = ubicacion

class Envio:
    def __init__(self, id_job, guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega, transportista=None,accidente=None):
        self.id_job = id_job
        self.guia_aerea = guia_aerea
        self.cliente = cliente
        self.tipo_producto = tipo_producto
        self.destino = destino
        self.temperatura = temperatura
        self.hora_entrega = hora_entrega
        self.transportista = transportista #NO SE ESTÁ USANDO
        self.estado_actual = EstadoEnvio.RECIBIDO
        self.historial_estados = [CambioEstado(EstadoEnvio.RECIBIDO, datetime.datetime.now(), "Aeropuerto El Dorado")]
        self.ubicacion_actual = "Aeropuerto El Dorado"
        self.accidente=accidente

    def actualizar_estado(self, nuevo_estado, ubicacion):
        self.estado_actual = nuevo_estado
        self.ubicacion_actual = ubicacion
        self.historial_estados.append(CambioEstado(nuevo_estado, datetime.datetime.now(), ubicacion))

    #NO SE ESTÁ USANDO
    #def asignar_transportista(self, transportista):
     #   self.transportista = transportista

class SistemaSeguimiento:
    def __init__(self):
        self.envios = {}
        self.usuarios = {}
        self.clientes = {}
        self.transportistas = []
        self.quimicos = []
        self.gerentes_comerciales = []

    def agregar_usuario(self, usuario):
        self.usuarios[usuario.nombre] = usuario
        if isinstance(usuario, Cliente):
            self.clientes[usuario.identificador] = usuario
        elif isinstance(usuario, Transportista):
            self.transportistas.append(usuario)
        elif isinstance(usuario, Quimico):
            self.quimicos.append(usuario)
        elif isinstance(usuario, GerenteComercial):
            self.gerentes_comerciales.append(usuario)

    def crear_envio(self, guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega):
        id_job = f"JOB{len(self.envios) + 1:03}"
        nuevo_envio = Envio(id_job, guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega)
        self.envios[id_job] = nuevo_envio
        cliente.envios.append(nuevo_envio)
        return id_job

    def actualizar_estado_envio(self, id_job, nuevo_estado, ubicacion):
        if id_job in self.envios:
            self.envios[id_job].actualizar_estado(nuevo_estado, ubicacion)
            if nuevo_estado != EstadoEnvio["EN_RETRASO"]:
                self.envios[id_job].accidente=None
            return True
        return False

    def obtener_info_envio(self, id_job):
        if id_job in self.envios:
            envio = self.envios[id_job]
            if envio.accidente == None:
                return f"JOB: {envio.id_job}, Guía Aérea: {envio.guia_aerea}, Cliente: {envio.cliente.nombre}, " \
                       f"Tipo: {envio.tipo_producto}, Destino: {envio.destino}, Estado: {envio.estado_actual.value}, " \
                       f"Temperatura: {envio.temperatura}, Hora de entrega: {envio.hora_entrega}, " \
                       f"Ubicación actual: {envio.ubicacion_actual}"
            else:
                return f"JOB: {envio.id_job}, Guía Aérea: {envio.guia_aerea}, Cliente: {envio.cliente.nombre}, " \
                       f"Tipo: {envio.tipo_producto}, Destino: {envio.destino}, Estado: {envio.estado_actual.value}, " \
                       f"Temperatura: {envio.temperatura}, Hora de entrega: {envio.hora_entrega}, " \
                       f"Ubicación actual: {envio.ubicacion_actual}, "\
                       f"Accidente:{envio.accidente}"

        return "Envío no encontrado"

    def obtener_historial_envio(self, id_job):
        if id_job in self.envios:
            envio = self.envios[id_job]
            historial = [f"{cambio.fecha} - {cambio.estado.value} en {cambio.ubicacion}" for cambio in envio.historial_estados]
            return "\n".join(historial)
        return "Envío no encontrado"

def menu_cliente(sistema):
    while True:
        print("\n--- Menú Cliente ---")
        print("1. Ver mis pedidos")
        print("2. Ver estado de un envío")
        print("3. Ver historial de un envío")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            identificador = input("\nIngrese su identificador de cliente: ")
            if identificador in sistema.clientes:
                cliente=sistema.clientes[identificador]
                if cliente.envios:
                    for envio in cliente.envios:
                        print(sistema.obtener_info_envio(envio.id_job))
                else:
                    print("No tiene pedidos registrados.")
            else:
                print("Cliente no encontrado")

        elif opcion == "2" or opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
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
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
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
        print("3. Reportar accidente")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            nuevo_estado = input("Ingrese el nuevo estado (RECIBIDO, EN_REPARTO_AEREO, VIAJANDO_A_TU_DESTINO, EN_CENTRO_LOGISTICO, EN_CAMINO_HACIA_TI, ENTREGADO, EN_RETRASO): ") 
            if nuevo_estado == "RECIBIDO":
                pass
            elif nuevo_estado == "EN_REPARTO_AEREO":
                pass
            elif nuevo_estado == "VIAJANDO_A_TU_DESTINO":
                pass
            elif nuevo_estado == "EN_CENTRO_LOGISTICO":
                pass
            elif nuevo_estado == "EN_CAMINO_HACIA_TI":
                pass
            elif nuevo_estado == "ENTREGADO":
                pass
            elif nuevo_estado == "EN_RETRASO":
                pass
            else:
                print("Estado no válido")
                continue
            
            ubicacion = input("Ingrese la ubicación actual: ")
            if sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion):
                print("Estado actualizado con éxito")
            else:
                print("No se pudo actualizar el estado")
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            ubicacion=input("Ingrese ubicación del accidente: ")
            detalle=input("Ingrese detalle del accidente (puntual/corto): ")
            envio = sistema.envios[id_job]
            envio.accidente=detalle
            sistema.actualizar_estado_envio(id_job, EstadoEnvio["EN_RETRASO"], ubicacion)
            print("Accidente ingresado con éxito y estado cambiado a: En retraso ")
        elif opcion == "4":
            break
        else:
            print("Opción no válida")

def menu_logistica(sistema):
    while True:
        print("\n--- Menú Logística ---")
        print("1. Editar estado del envío")
        print("2. Modificar datos de envío")
        print("3. Ver información del envío")
        print("4. Agregar empleado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")


        if opcion == "1":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            nuevo_estado = input("Ingrese el nuevo estado (RECIBIDO, EN_REPARTO_AEREO, VIAJANDO_A_TU_DESTINO, EN_CENTRO_LOGISTICO, EN_CAMINO_HACIA_TI, ENTREGADO, EN_RETRASO): ") 
            if nuevo_estado == "RECIBIDO":
                pass
            elif nuevo_estado == "EN_REPARTO_AEREO":
                pass
            elif nuevo_estado == "VIAJANDO_A_TU_DESTINO":
                pass
            elif nuevo_estado == "EN_CENTRO_LOGISTICO":
                pass
            elif nuevo_estado == "EN_CAMINO_HACIA_TI":
                pass
            elif nuevo_estado == "ENTREGADO":
                pass
            elif nuevo_estado == "EN_RETRASO":
                pass
            else:
                print("Estado no válido")
                continue
            ubicacion = input("Ingrese la ubicación actual: ")
            if sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion):
                print("Estado actualizado con éxito")
            else:
                print("No se pudo actualizar el estado")
        
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío a modificar: ")
            if id_job not in sistema.envios:
                print (f'No se ha encontrado ningún envío con el {id_job}')
                break
            if id_job in sistema.envios:
                envio = sistema.envios[id_job]
                print("Datos actuales del envío:")
                print(sistema.obtener_info_envio(id_job))
                tipo_producto = input("Nuevo tipo de producto (deje en blanco para no modificar): ")
                if tipo_producto:
                    envio.tipo_producto = tipo_producto
                
                destino = input("Nuevo destino (deje en blanco para no modificar): ")
                if destino:
                    envio.destino = destino
                
                temperatura = input("Nueva temperatura (deje en blanco para no modificar): ")
                if temperatura:
                    envio.temperatura = temperatura
                
                hora_entrega = input("Nueva hora de entrega (YYYY-MM-DD HH:MM) (deje en blanco para no modificar): ")
                if hora_entrega:
                    envio.hora_entrega = datetime.datetime.strptime(hora_entrega, "%Y-%m-%d %H:%M")
                
                print("Datos del envío actualizados:")
                print(sistema.obtener_info_envio(id_job))
            else:
                print("Envío no encontrado")
        elif opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "4":
            nombre = input("\nIngrese el nombre del empleado: ")
            rol = input("Ingrese el rol del empleado (TRANSPORTISTA/QUIMICO/GERENTE_COMERCIAL): ")
            if rol == "TRANSPORTISTA":
                nuevo_empleado = Transportista(nombre)
            elif rol == "QUIMICO":
                nuevo_empleado = Quimico(nombre)
            elif rol == "GERENTE_COMERCIAL":
                nuevo_empleado = GerenteComercial(nombre)
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
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            nuevo_estado = input("Ingrese el nuevo estado (RECIBIDO, EN_REPARTO_AEREO, VIAJANDO_A_TU_DESTINO, EN_CENTRO_LOGISTICO, EN_CAMINO_HACIA_TI, ENTREGADO, EN_RETRASO): ") 
            if nuevo_estado == "RECIBIDO":
                pass
            elif nuevo_estado == "EN_REPARTO_AEREO":
                pass
            elif nuevo_estado == "VIAJANDO_A_TU_DESTINO":
                pass
            elif nuevo_estado == "EN_CENTRO_LOGISTICO":
                pass
            elif nuevo_estado == "EN_CAMINO_HACIA_TI":
                pass
            elif nuevo_estado == "ENTREGADO":
                pass
            elif nuevo_estado == "EN_RETRASO":
                pass
            else:
                print("Estado no válido")
                continue
            ubicacion = input("Ingrese la ubicación actual: ")
            if sistema.actualizar_estado_envio(id_job, EstadoEnvio[nuevo_estado], ubicacion):
                print("Estado actualizado con éxito")
            else:
                print("No se pudo actualizar el estado")
        elif opcion == "2":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def menu_gerente_comercial(sistema, gerente):
    while True:
        print("\n--- Menú Gerente Comercial ---")
        print("1. Ingresar nuevo cliente")
        print("2. Crear nuevo envío")
        print("3. Ver información del envío")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese el nombre del cliente: ")
            if isinstance (nombre, str):
                pass
            else:
                print("Debes ingresar un nombre")
            identificador = input("Ingrese el identificador del cliente: ")
            try:
                numero = int(identificador)  
            except ValueError:
                print("Debes ingresar un valor numérico")
                return
            if identificador not in sistema.clientes:
                nuevo_cliente = Cliente(nombre, identificador)
                sistema.agregar_usuario(nuevo_cliente)
                print(f"Nuevo cliente {nombre} ingresado")
            else: 
                print('El cliente ya se encuentra registrado')
        elif opcion == "2":
            identificador_cliente = input("Ingrese el identificador del cliente: ")
            if identificador_cliente in sistema.clientes:
                cliente = sistema.clientes[identificador_cliente]
                guia_aerea = input("Ingrese el número de guía aérea(si aplica): ")
                tipo_producto = input("Ingrese el tipo de producto: ")
                destino = input("Ingrese el destino: ")
                temperatura = input("Ingrese la temperatura requerida: ")
                #hora_entrega = input("Ingrese la hora de entrega (YYYY-MM-DD HH:MM): ")
                while True:
                    hora_entrega = input("Ingrese la fecha y hora de entrega (YYYY-MM-DD HH:MM): ")
                    try:
                        hora_entrega = datetime.datetime.strptime(hora_entrega, "%Y-%m-%d %H:%M")
                        print("Formato válido!")
                        break
                    except ValueError:
                        print("Error: Formato inválido. Ingrese formato válido (YYYY-MM-DD HH:MM)")

                id_job = sistema.crear_envio(guia_aerea, cliente, tipo_producto, destino, temperatura, hora_entrega)
                print(f"Nuevo envío creado con ID: {id_job}")
            else:
                print("Cliente no encontrado")
        elif opcion == "3":
            id_job = input("Ingrese el ID del envío: ")
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "4":
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
        print("6. Gerente Comercial")
        print("7. Salir")
        opcion = input("Seleccione su tipo de usuario: ")
        
        if opcion == "1":
            menu_cliente(sistema)
        elif opcion == "2":
            menu_destinatario(sistema)
        elif opcion == "3":
            if sistema.transportistas:
                print("\nTransportistas disponibles:")
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
                print("\nQuímicos disponibles:")
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
            if sistema.usuarios:
                gerentes = [usuario for usuario in sistema.usuarios.values() if usuario.rol == Rol.GERENTE_COMERCIAL]
                if gerentes:
                    print("\nGerentes Comerciales disponibles:")
                    for i, gerente in enumerate(gerentes):
                        print(f"{i+1}. {gerente.nombre}")
                    seleccion = int(input("Seleccione un Gerente Comercial: ")) - 1
                    if 0 <= seleccion < len(gerentes):
                        menu_gerente_comercial(sistema, gerentes[seleccion])
                    else:
                        print("Selección no válida")
                else:
                    print("No hay Gerentes Comerciales registrados")
            else:
                print("No hay usuarios registrados en el sistema")
        elif opcion == "7":
            print("Gracias por usar el Sistema de Seguimiento")
            break
        else:
            print("Opción no válida")

def menu_gerente_comercial(sistema, gerente):
    while True:
        print("\n--- Menú Gerente Comercial ---")
        print("1. Registrar nuevo cliente")
        print("2. Crear nuevo envío")
        print("3. Ver información de un envío")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese el nombre del cliente: ")
            identificador = input("Ingrese el identificador del cliente: ")
            try:
                numero = int(identificador)  
            except ValueError:
                print("Debes ingresar un valor numérico")
                return
            if identificador not in sistema.clientes:
                nuevo_cliente = Cliente(nombre, identificador)
                sistema.agregar_usuario(nuevo_cliente)
                print(f"Nuevo cliente {nombre} ingresado")
            else: 
                print('El cliente ya se encuentra registrado')
        elif opcion == "2":
            identificador_cliente = input("Ingrese el identificador del cliente: ")
            if identificador_cliente in sistema.clientes:
                cliente = sistema.clientes[identificador_cliente]
                guia_aerea = input("Ingrese el número de guía aérea(SI ES SU CASO): ")
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
            if id_job in sistema.envios:
                pass
            else:
                print(f'No se ha encontrado ningún envío con el {id_job}')
                break
            print(sistema.obtener_info_envio(id_job))
        elif opcion == "4":
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu_principal()