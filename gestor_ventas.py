import mysql.connector
from mysql.connector import Error
from decouple import config
from datetime import datetime
from venta import Venta

class GestorVentas:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

        self.cursor = self.connection.cursor() if self.connection else None
        self.__ventas = self.cargar_ventas()
        self.__contador_id = self.obtener_contador_id()

    def crear_venta(self, venta):
        try:
            venta_dict = venta.to_dict()
            print(f"Venta dict: {venta_dict}")
            productos = ', '.join(venta_dict['productos'])
            query = "INSERT INTO Venta (Fecha, Cliente, Productos) VALUES (%s, %s, %s)"
            values = (venta_dict['fecha'], venta_dict['cliente'], productos)
            self.cursor.execute(query, values)
            self.connection.commit()
            self.recargar_ventas()
            print(f"Venta registrada exitosamente con el ID {self.__contador_id}")
        
        except Exception as e:
            print(f"Error al crear la venta: {e}")

    @property
    def contador(self):
        return self.__contador_id
    
    @contador.getter
    def contador(self):
        return self.__contador_id

    def recargar_ventas(self):
        self.__ventas = self.cargar_ventas()

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def cargar_ventas(self):
        ventas = {}
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.execute('SELECT id, Fecha, Cliente, Productos FROM Venta')
                for row in self.cursor.fetchall():
                    ventas[str(row[0])] = {
                        'id': row[0],
                        'fecha': row[1],
                        'cliente': row[2],
                        'productos': row[3]
                    }
            else:
                print("No se pudo establecer la conexión para cargar ventas.")
        except Error as e:
            print(f"Error al cargar las ventas: {e}")
        return ventas

    def obtener_contador_id(self):
        if self.__ventas:
            return max(int(id_venta) for id_venta in self.__ventas.keys())
        return 0

    def generar_id_venta(self):
        self.__contador_id += 1
        return str(self.__contador_id)

    def leer_venta(self, id_venta):
        try:
            if id_venta not in self.__ventas:
                print("Venta no encontrada.")
                return None
            return self.__ventas[id_venta]
        except Exception as e:
            print(f"Error al leer la venta: {e}")
            return None

    def actualizar_venta(self, id_venta, nueva_venta):
        try:
            if not isinstance(nueva_venta, Venta):
                raise ValueError("El objeto no es una instancia de la clase Venta.")
            if id_venta not in self.__ventas:
                print("Venta no encontrada.")
                return
            
            self.__ventas[id_venta] = nueva_venta.to_dict()
            print("Venta actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar la venta: {e}")

    def eliminar_venta(self, id_venta):
        try:
            if id_venta not in self.__ventas:
                print("Venta no encontrada.")
                return
            del self.__ventas[id_venta]
            print("Venta eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la venta: {e}")

    def buscar_ventas_por_fecha(self, fecha):
        ventas_encontradas = []
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
            except ValueError:
                print("Error: el formato de fecha debe ser DD-MM-YYYY.")
                return []
        for id_venta, venta in self.__ventas.items():
            venta_fecha = venta['fecha']
            if isinstance(venta_fecha, datetime):
                venta_fecha = venta_fecha.date()
            
            if venta_fecha == fecha:
                ventas_encontradas.append((id_venta, venta))
        return ventas_encontradas

