import tkinter as tk
from tkinter import messagebox

class Trabajador:
    def __init__(self):
        self.nombre = ""
        self.fecha_nacimiento = ""
        self.tipo_contratacion = ""
        self.sexo = ""
        self.ultimo_grado_estudio = ""
        self.especialidad = ""
        self.posgrado = ""
        self.cedula_profesional = ""
        self.domicilio = ""
        self.telefono = ""
        self.correo_electronico = ""
        self.fecha_ingreso = ""

    def registrar_datos(self):
        self.nombre = nombre_entry.get()
        self.fecha_nacimiento = fecha_nacimiento_entry.get()
        self.tipo_contratacion = tipo_contratacion_var.get()
        self.sexo = sexo_var.get()
        self.ultimo_grado_estudio = ultimo_grado_estudio_var.get()
        self.especialidad = especialidad_entry.get()
        self.posgrado = posgrado_entry.get()
        self.cedula_profesional = cedula_profesional_entry.get()
        self.domicilio = domicilio_entry.get()
        self.telefono = telefono_entry.get()
        self.correo_electronico = correo_electronico_entry.get()
        self.fecha_ingreso = fecha_ingreso_entry.get()
        messagebox.showinfo("Registro", "Datos registrados con éxito")

    def mostrar_datos(self):
        datos = f"Nombre: {self.nombre}\n"
        datos += f"Fecha de nacimiento: {self.fecha_nacimiento}\n"
        datos += f"Tipo de contratación: {self.tipo_contratacion}\n"
        datos += f"Sexo: {self.sexo}\n"
        datos += f"Último grado de estudio: {self.ultimo_grado_estudio}\n"
        datos += f"Especialidad: {self.especialidad}\n"
        datos += f"Posgrado: {self.posgrado}\n"
        datos += f"Cédula profesional: {self.cedula_profesional}\n"
        datos += f"Domicilio: {self.domicilio}\n"
        datos += f"Teléfono: {self.telefono}\n"
        datos += f"Correo electrónico: {self.correo_electronico}\n"
        datos += f"Fecha de ingreso: {self.fecha_ingreso}"
        messagebox.showinfo("Datos del Trabajador", datos)

# Interfaz gráfica
root = tk.Tk()
root.title("Control de Asistencias")

trabajador = Trabajador()

# Entradas
nombre_label = tk.Label(root, text="Nombre:")
nombre_label.grid(row=0, column=0, sticky="e")
nombre_entry = tk.Entry(root)
nombre_entry.grid(row=0, column=1)

fecha_nacimiento_label = tk.Label(root, text="Fecha de nacimiento:")
fecha_nacimiento_label.grid(row=1, column=0, sticky="e")
fecha_nacimiento_entry = tk.Entry(root)
fecha_nacimiento_entry.grid(row=1, column=1)

tipo_contratacion_label = tk.Label(root, text="Tipo de contratación:")
tipo_contratacion_label.grid(row=2, column=0, sticky="e")
tipo_contratacion_var = tk.StringVar(root)
tipo_contratacion_var.set("Enfermero")
tipo_contratacion_option = tk.OptionMenu(root, tipo_contratacion_var, "Enfermero", "Doctor", "Otros")
tipo_contratacion_option.grid(row=2, column=1)

sexo_label = tk.Label(root, text="Sexo:")
sexo_label.grid(row=3, column=0, sticky="e")
sexo_var = tk.StringVar(root)
sexo_var.set("Femenino")
sexo_option = tk.OptionMenu(root, sexo_var, "Femenino", "Masculino")
sexo_option.grid(row=3, column=1)

ultimo_grado_estudio_label = tk.Label(root, text="Último grado de estudio:")
ultimo_grado_estudio_label.grid(row=4, column=0, sticky="e")
ultimo_grado_estudio_var = tk.StringVar(root)
ultimo_grado_estudio_var.set("Doctorado")
ultimo_grado_estudio_option = tk.OptionMenu(root, ultimo_grado_estudio_var, "Doctorado", "Maestría", "Licenciatura", "Auxiliar", "Técnico General")
ultimo_grado_estudio_option.grid(row=4, column=1)

especialidad_label = tk.Label(root, text="Especialidad:")
especialidad_label.grid(row=5, column=0, sticky="e")
especialidad_entry = tk.Entry(root)
especialidad_entry.grid(row=5, column=1)

posgrado_label = tk.Label(root, text="Posgrado:")
posgrado_label.grid(row=6, column=0, sticky="e")
posgrado_entry = tk.Entry(root)
posgrado_entry.grid(row=6, column=1)

cedula_profesional_label = tk.Label(root, text="Cédula profesional:")
cedula_profesional_label.grid(row=7, column=0, sticky="e")
cedula_profesional_entry = tk.Entry(root)
cedula_profesional_entry.grid(row=7, column=1)

domicilio_label = tk.Label(root, text="Domicilio:")
domicilio_label.grid(row=8, column=0, sticky="e")
domicilio_entry = tk.Entry(root)
domicilio_entry.grid(row=8, column=1)

telefono_label = tk.Label(root, text="Teléfono:")
telefono_label.grid(row=9, column=0, sticky="e")
telefono_entry = tk.Entry(root)
telefono_entry.grid(row=9, column=1)

correo_electronico_label = tk.Label(root, text="Correo electrónico:")
correo_electronico_label.grid(row=10, column=0, sticky="e")
correo_electronico_entry = tk.Entry(root)
correo_electronico_entry.grid(row=10, column=1)

fecha_ingreso_label = tk.Label(root, text="Fecha de ingreso:")
fecha_ingreso_label.grid(row=11, column=0, sticky="e")
fecha_ingreso_entry = tk.Entry(root)
fecha_ingreso_entry.grid(row=11, column=1)

# Botones
registrar_button = tk.Button(root, text="Registrar Datos", command=trabajador.registrar_datos)
registrar_button.grid(row=12, column=0, pady=10)

mostrar_button = tk.Button(root, text="Mostrar Datos", command=trabajador.mostrar_datos)
mostrar_button.grid(row=12, column=1, pady=10)

root.mainloop()