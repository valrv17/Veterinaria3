import logging
import csv
import json

# Configuración del logging
logging.basicConfig(
    filename='clinica_veterinaria.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Inicio del sistema de gestión veterinaria")

# CLASES
class Dueno:
    def _init_(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def _str_(self):
        return f"{self.nombre} | Tel: {self.telefono} | Dir: {self.direccion}"

class Mascota:
    def _init_(self, nombre, especie, raza, edad, dueno):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno
        self.consultas = []

    def agregar_consulta(self, consulta):
        self.consultas.append(consulta)

    def mostrar_historial(self):
        if not self.consultas:
            return f"No hay consultas para {self.nombre}."
        historial = f"Historial de {self.nombre}:\n"
        for c in self.consultas:
            historial += str(c) + "\n"
        return historial

    def _str_(self):
        return f"{self.nombre} | {self.especie} | {self.raza} | {self.edad} años | Dueño: {self.dueno.nombre}"

class Consulta:
    def _init_(self, fecha, motivo, diagnostico, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota

    def _str_(self):
        return f"[{self.fecha}] Motivo: {self.motivo} | Diagnóstico: {self.diagnostico}"

# Datos globales
duenos = []
mascotas = []

# Funciones de serialización
def export_to_csv(csv_file='mascotas_dueños.csv'):
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nombre_mascota','especie','raza','edad','nombre_dueno','telefono','direccion'])
            for m in mascotas:
                writer.writerow([
                    m.nombre, m.especie, m.raza, m.edad,
                    m.dueno.nombre, m.dueno.telefono, m.dueno.direccion
                ])
        logging.info(f"Datos de mascotas y dueños exportados a {csv_file}")
        print(f"Datos exportados a {csv_file}")
    except Exception as e:
        logging.error(f"Error al exportar CSV: {e}")
        print(f"Error al exportar CSV: {e}")


def import_from_csv(csv_file='mascotas_dueños.csv'):
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            duenos.clear()
            mascotas.clear()
            for row in reader:
                dueno = Dueno(row['nombre_dueno'], row['telefono'], row['direccion'])
                duenos.append(dueno)
                mascota = Mascota(
                    row['nombre_mascota'], row['especie'], row['raza'], int(row['edad']), dueno
                )
                mascotas.append(mascota)
        logging.info(f"Datos importados de {csv_file}")
        print(f"Datos importados de {csv_file}")
    except FileNotFoundError:
        logging.warning(f"Archivo CSV no encontrado: {csv_file}")
        print(f"No se encontró el archivo {csv_file}")
    except Exception as e:
        logging.error(f"Error al importar CSV: {e}")
        print(f"Error al importar CSV: {e}")


def export_to_json(json_file='consultas.json'):
    try:
        data = []
        for m in mascotas:
            for c in m.consultas:
                data.append({
                    'nombre_mascota': m.nombre,
                    'fecha': c.fecha,
                    'motivo': c.motivo,
                    'diagnostico': c.diagnostico
                })
        with open(json_file, mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Consultas exportadas a {json_file}")
        print(f"Consultas exportadas a {json_file}")
    except Exception as e:
        logging.error(f"Error al exportar JSON: {e}")
        print(f"Error al exportar JSON: {e}")


def import_from_json(json_file='consultas.json'):
    try:
        with open(json_file, mode='r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            mascota = next((m for m in mascotas if m.nombre == item['nombre_mascota']), None)
            if mascota:
                consulta = Consulta(item['fecha'], item['motivo'], item['diagnostico'], mascota)
                mascota.agregar_consulta(consulta)
        logging.info(f"Consultas importadas de {json_file}")
        print(f"Consultas importadas de {json_file}")
    except FileNotFoundError:
        logging.warning(f"Archivo JSON no encontrado: {json_file}")
        print(f"No se encontró el archivo {json_file}")
    except Exception as e:
        logging.error(f"Error al importar JSON: {e}")
        print(f"Error al importar JSON: {e}")

# Funciones del menú de gestión de mascotas y consultas
def registrar_mascota():
    print("\n--- Registrar Nueva Mascota ---")
    try:
        nombre = input("Nombre de la mascota: ")
        especie = input("Especie: ")
        raza = input("Raza: ")
        edad = int(input("Edad: "))
        if edad < 0:
            raise ValueError("La edad no puede ser negativa.")

        print("Ingrese datos del dueño:")
        nombre_d = input("Nombre del dueño: ")
        tel = input("Teléfono: ")
        dir = input("Dirección: ")

        dueno = Dueno(nombre_d, tel, dir)
        duenos.append(dueno)
        mascota = Mascota(nombre, especie, raza, edad, dueno)
        mascotas.append(mascota)

        print("Mascota registrada con éxito.")
        logging.info(f"Mascota registrada: {mascota.nombre}")
    except ValueError as e:
        print(f"Error en el ingreso de datos: {e}")
        logging.error(f"Error al registrar mascota: {e}")


def registrar_consulta():
    print("\n--- Registrar Consulta ---")
    if not mascotas:
        print("No hay mascotas registradas.")
        logging.warning("Intento de registrar consulta sin mascotas registradas.")
        return

    for i, m in enumerate(mascotas):
        print(f"{i + 1}. {m.nombre} - Dueño: {m.dueno.nombre}")
    try:
        indice = int(input("Seleccione la mascota (número): ")) - 1
        if indice < 0 or indice >= len(mascotas):
            raise IndexError("Índice fuera de rango.")
        mascota = mascotas[indice]

        fecha = input("Fecha (dd/mm/aaaa): ")
        motivo = input("Motivo de la consulta: ")
        diagnostico = input("Diagnóstico: ")

        consulta = Consulta(fecha, motivo, diagnostico, mascota)
        mascota.agregar_consulta(consulta)

        print("Consulta registrada con éxito.")
        logging.info(f"Consulta registrada para {mascota.nombre} el {fecha}")
    except (IndexError, ValueError) as e:
        print(f"Error al registrar la consulta: {e}")
        logging.error(f"Error al registrar consulta: {e}")


def listar_mascotas():
    print("\n--- Mascotas Registradas ---")
    if not mascotas:
        print("No hay mascotas registradas.")
        logging.warning("Intento de listar mascotas sin ninguna registrada.")
    else:
        for m in mascotas:
            print(m)
        logging.info("Listado de mascotas mostrado al usuario.")


def ver_historial():
    print("\n--- Historial de Consultas ---")
    if not mascotas:
        print("No hay mascotas registradas.")
        logging.warning("Intento de ver historial sin mascotas registradas.")
        return

    for i, m in enumerate(mascotas):
        print(f"{i + 1}. {m.nombre} - Dueño: {m.dueno.nombre}")
    try:
        indice = int(input("Seleccione la mascota (número): ")) - 1
        if indice < 0 or indice >= len(mascotas):
            raise IndexError("Índice inválido.")
        mascota = mascotas[indice]
        print(mascota.mostrar_historial())
        logging.info(f"Historial mostrado para la mascota {mascota.nombre}")
    except (IndexError, ValueError) as e:
        print(f"Error al acceder al historial: {e}")
        logging.error(f"Error al mostrar historial: {e}")

# MENÚ PRINCIPAL
def menu():
    try:
        while True:
            print("\n=== Clínica Veterinaria 'Amigos Peludos' ===")
            print("1. Registrar Mascota")
            print("2. Registrar Consulta")
            print("3. Listar Mascotas")
            print("4. Ver Historial de Consultas")
            print("5. Exportar Datos a CSV/JSON")
            print("6. Importar Datos desde CSV/JSON")
            print("7. Salir")

            opc = input("Seleccione una opción: ")

            if opc == "1":
                registrar_mascota()
            elif opc == "2":
                registrar_consulta()
            elif opc == "3":
                listar_mascotas()
            elif opc == "4":
                ver_historial()
            elif opc == "5":
                export_to_csv()
                export_to_json()
            elif opc == "6":
                import_from_csv()
                import_from_json()
            elif opc == "7":
                print("Saliendo del sistema. ¡Hasta pronto!")
                logging.info("Cierre del sistema de gestión veterinaria")
                break
            else:
                print("Opción inválida.")
                logging.warning(f"Opción inválida: {opc}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        logging.critical(f"Error inesperado en menú: {e}", exc_info=True)

if __name__== "__main__":
    menu()





