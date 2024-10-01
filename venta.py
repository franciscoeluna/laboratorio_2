
# Mejoras aplicadas.
# Cambio de ID generado por fecha y hs por un ID tipo entero generado autimaticamente auto incrementable.
# Cambio los atributos de las clases a privados proporcionando métodos getters y setters.
# Script para la base de datos.

# CREATE DATABASE IF NOT EXISTS venta;
# USE venta;

# CREATE TABLE Venta (
#     Fecha DATETIME,
#     Cliente VARCHAR(50) NOT NULL,
#     Productos VARCHAR(50) NOT NULL,
#     ID INT NOT NULL AUTO_INCREMENT,
#     PRIMARY KEY (ID)
# );

# CREATE TABLE VentaOnline (
#     direccion_envio VARCHAR(50) NOT NULL,
#     ID INT NOT NULL,
#     PRIMARY KEY (ID),
#     FOREIGN KEY (ID) REFERENCES Venta(ID)
# );

from datetime import datetime

class Venta:
    def __init__(self, fecha, cliente, productos, id):
        self.__fecha = fecha
        self.__cliente = cliente
        self.__productos = productos
        self.__id = id

    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def productos(self):
        return self.__productos
    
    @property
    def id(self):
        return self.__id

    def to_dict(self):
        return {
            'fecha': self.__fecha,
            'cliente': self.__cliente,
            'productos': self.__productos,
            'if': self.__id,
            'tipo': self.__class__.__name__
        }

class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, id, direccion_envio):
        super().__init__(fecha, cliente, productos, id)
        self.__direccion_envio = direccion_envio

    def to_dict(self):
        data = super().to_dict()
        data['direccion_envio'] = self.__direccion_envio
        return data

class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, id, tienda):
        super().__init__(fecha, cliente, productos, id)
        self.__tienda = tienda

    def to_dict(self):
        data = super().to_dict()
        data['tienda'] = self.__tienda
        return data

