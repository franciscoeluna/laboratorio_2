from datetime import datetime
from gestor_ventas import GestorVentas
from venta import VentaOnline, VentaLocal

def main():
    gestor = GestorVentas()
    
    while True:
        print("\n--- Gestión de Ventas ---")
        print("1. Crear venta online")
        print("2. Crear venta local")
        print("3. Ver venta por ID")
        print("4. Actualizar venta")
        print("5. Eliminar venta")
        print("6. Ver ventas por fecha")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            fecha = datetime.now().date().isoformat()
            cliente = input("Ingrese el nombre del cliente: ").capitalize()
            productos_input = input("Ingrese los productos vendidos (separados por coma): ").split(',')
            productos = [producto.strip() for producto in productos_input]
            direccion_envio = input("Ingrese la dirección de envío: ")
            nuevo_id = gestor.generar_id_venta()
            venta = VentaOnline(fecha, cliente, productos, nuevo_id, direccion_envio)
            gestor.crear_venta(venta)
        
        elif opcion == '2':
            fecha = datetime.now().date().isoformat()
            cliente = input("Ingrese el nombre del cliente: ").capitalize()
            productos = input("Ingrese los productos vendidos (separados por coma): ").split(',')
            tienda = input("Ingrese la tienda: ")
            nuevo_id = gestor.generar_id_venta()
            venta = VentaOnline(fecha, cliente, productos, nuevo_id, direccion_envio)
            gestor.crear_venta(venta)
        
        elif opcion == '3':
            id_venta = input("Ingrese el ID de la venta a leer: ")
            venta = gestor.leer_venta(id_venta)
            if venta:
                print(f"Venta ID {id_venta}:")
                print(venta)
            else:
                print("Venta no encontrada.")

        elif opcion == '4':
            id_venta = input("Ingrese el ID de la venta a actualizar: ")
            tipo = input("Ingrese el tipo de venta (online/local): ").lower()
            fecha = datetime.now().date().isoformat()
            cliente = input("Ingrese el nombre del cliente: ")
            productos = input("Ingrese los productos vendidos (separados por coma): ").split(',')

            if tipo == 'online':
                direccion_envio = input("Ingrese la dirección de envío: ")
                nueva_venta = VentaOnline(fecha, cliente, productos, id_venta, direccion_envio)
            elif tipo == 'local':
                tienda = input("Ingrese la tienda: ")
                nueva_venta = VentaLocal(fecha, cliente, productos, id_venta, tienda)
            else:
                print("Tipo de venta no válido, debe ingresar 'local' u 'online'.")
                continue
            
            gestor.actualizar_venta(id_venta, nueva_venta)

        elif opcion == '5':
            id_venta = input("Ingrese el ID de la venta a eliminar: ")
            gestor.eliminar_venta(id_venta)

        elif opcion == '6':
            fecha = input("Ingrese la fecha para buscar ventas (dd/mm/yyyy): ")
            ventas = gestor.buscar_ventas_por_fecha(fecha)
            if ventas is None:
                pass
            elif ventas:
                print(f"Ventas realizadas el {fecha}:")
                for i, (id_venta, venta) in enumerate(ventas):
                    print(f"{i + 1}. ID {id_venta}: {venta}")
            else:
                print("No se encontraron ventas en esa fecha.")
        
        elif opcion == '7':
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
