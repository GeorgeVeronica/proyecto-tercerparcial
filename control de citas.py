import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime #con esto podre trabajar con tiempos y fechas
import json #se uso para que los datos puedan ser almacenados
import os #servira para eleminar, modificar o renombrar algo dentro del codigo

class Persona:
    def __init__(self, nombre, edad=None):
        self.nombre = nombre
        self.edad = edad

class PersonalHospital(Persona):
    def __init__(self, nombre, area, fecha_nacimiento="", tipo_contratacion="", sexo="",
                 ultimo_grado_estudio="", especialidad="", posgrado="",
                 cedula_profesional="", domicilio="", telefono="",
                 correo_electronico="", fecha_ingreso="", puesto=""):
        super().__init__(nombre)
        self.area = area
        self.ocupado = False
        self.fecha_nacimiento = fecha_nacimiento
        self.tipo_contratacion = tipo_contratacion
        self.sexo = sexo
        self.ultimo_grado_estudio = ultimo_grado_estudio
        self.especialidad = especialidad
        self.posgrado = posgrado
        self.cedula_profesional = cedula_profesional
        self.domicilio = domicilio
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.fecha_ingreso = fecha_ingreso
        self.puesto = puesto

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "area": self.area,
            "ocupado": self.ocupado,
            "fecha_nacimiento": self.fecha_nacimiento,
            "tipo_contratacion": self.tipo_contratacion,
            "sexo": self.sexo,
            "ultimo_grado_estudio": self.ultimo_grado_estudio,
            "especialidad": self.especialidad,
            "posgrado": self.posgrado,
            "cedula_profesional": self.cedula_profesional,
            "domicilio": self.domicilio,
            "telefono": self.telefono,
            "correo_electronico": self.correo_electronico,
            "fecha_ingreso": self.fecha_ingreso,
            "puesto": self.puesto
        }

class Paciente(Persona):
    def __init__(self, nombre, edad, area, camilla=None, doctor_asignado=None, enfermero_asignado=None, enfermedad=None, seguro_social=None):
        super().__init__(nombre, edad)
        self.area = area
        self.camilla = camilla
        self.doctor_asignado = doctor_asignado
        self.enfermero_asignado = enfermero_asignado
        self.enfermedad = enfermedad
        self.seguro_social = seguro_social

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "area": self.area,
            "camilla": self.camilla,
            "doctor_asignado_nombre": self.doctor_asignado.nombre if self.doctor_asignado else None,
            "enfermero_asignado_nombre": self.enfermero_asignado.nombre if self.enfermero_asignado else None,
            "enfermedad": self.enfermedad,
            "seguro_social": self.seguro_social
        }

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Hospitalaria")
        self.attributes("-fullscreen", True)

        self.colors = {  #esto funciona desde un diccionario de nombre self.colors lo que hace que los colores se puedan gestionar 
            "primary": "#2C3E50",
            "secondary": "#34495E",
            "accent": "#3498DB",
            "background": "#ECF0F1",
            "text_light": "white",
            "text_dark": "#2C3E50",
            "button_hover": "#2980B9",
            "error": "#E74C3C",
            "success": "#2ECC71"
        }

        self.personal = []

        self.camillas = {
            "Medicina General": [{"ocupada": False, "id": i + 1} for i in range(8)],
            "Urgencias": [{"ocupada": False, "id": i + 1} for i in range(5)],
            "Hospitalización": [{"ocupada": False, "id": i + 1} for i in range(10)],
            "UCI": [{"ocupada": False, "id": i + 1} for i in range(3)]
        }
        
        self.areas_personal_disponibles = ["Medicina General", "Urgencias", "Hospitalización"]
        self.areas_paciente_disponibles = ["Medicina General", "Urgencias", "Hospitalización"] 

        self.pacientes = []
        self._load_data() 

        self.main_frame = tk.Frame(self, bg=self.colors["background"]) #la self.main_frame es la base sobre el cual es codigo se llevara acabo
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.frames_container = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.frames_container.grid(row=0, column=1, sticky="nsew")
        self.frames_container.grid_rowconfigure(0, weight=1)
        self.frames_container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for name in ["Inicio", "Registro de Paciente", "Administrar Personal", "Ver Camillas y Asignaciones"]:
            frame = tk.Frame(self.frames_container, bg=self.colors["background"])
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.create_inicio_frame(self.frames["Inicio"])
        self.create_registro_paciente_frame(self.frames["Registro de Paciente"])
        self.create_administrar_personal_frame(self.frames["Administrar Personal"])
        self.create_ver_camillas_frame(self.frames["Ver Camillas y Asignaciones"])

        self.actualizar_tablas_display() 

        self.show_frame("Inicio")

    def _load_data(self):
        if os.path.exists("personal_data.json"): #esto se usa para saber si hay datos guardados anteriormente
            try:
                with open("personal_data.json", "r") as f:
                    personal_dicts = json.load(f)
                    for p_dict in personal_dicts:
                        init_params = [
                            "nombre", "area", "fecha_nacimiento", "tipo_contratacion", "sexo",
                            "ultimo_grado_estudio", "especialidad", "posgrado",
                            "cedula_profesional", "domicilio", "telefono",
                            "correo_electronico", "fecha_ingreso", "puesto"
                        ]
                        
                        constructor_args = {key: p_dict.get(key, "") for key in init_params}
                        
                        person = PersonalHospital(**constructor_args)
                        person.ocupado = p_dict.get("ocupado", False)
                        self.personal.append(person)
            except json.JSONDecodeError:
                messagebox.showerror("Error de carga", "Archivo de personal corrupto o vacío.")
            except Exception as e:
                messagebox.showerror("Error de carga", f"Error al cargar personal: {e}")

        if os.path.exists("patient_data.json"):
            try:
                with open("patient_data.json", "r") as f:
                    patient_dicts = json.load(f)
                    for p_dict in patient_dicts:
                        doctor_obj = next((p for p in self.personal if p.nombre == p_dict["doctor_asignado_nombre"]), None)
                        enfermero_obj = next((p for p in self.personal if p.nombre == p_dict["enfermero_asignado_nombre"]), None)
                        
                        if doctor_obj:
                            doctor_obj.ocupado = True
                        if enfermero_obj:
                            enfermero_obj.ocupado = True

                        if p_dict["area"] in self.camillas and p_dict["camilla"]:
                            for c_data in self.camillas[p_dict["area"]]:
                                if c_data["id"] == p_dict["camilla"]:
                                    c_data["ocupada"] = True
                                    break

                        patient = Paciente(
                            nombre=p_dict["nombre"],
                            edad=p_dict["edad"],
                            area=p_dict["area"],
                            camilla=p_dict["camilla"],
                            doctor_asignado=doctor_obj,
                            enfermero_asignado=enfermero_obj,
                            enfermedad=p_dict["enfermedad"],
                            seguro_social=p_dict["seguro_social"]
                        )
                        self.pacientes.append(patient)
            except json.JSONDecodeError:
                messagebox.showerror("Error de carga", "Archivo de pacientes corrupto o vacío.")
            except Exception as e:
                messagebox.showerror("Error de carga", f"Error al cargar pacientes: {e}")

    def _save_data(self):
        try:
            with open("personal_data.json", "w") as f:
                json.dump([p.to_dict() for p in self.personal], f, indent=4)
        except Exception as e:
            messagebox.showerror("Error de guardado", f"Error al guardar personal: {e}")

        try:
            with open("patient_data.json", "w") as f:
                json.dump([p.to_dict() for p in self.pacientes], f, indent=4)
        except Exception as e:
            messagebox.showerror("Error de guardado", f"Error al guardar pacientes: {e}")

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, width=200, bg=self.colors["primary"])
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="MENÚ", bg=self.colors["secondary"], fg=self.colors["text_light"],
                 font=("Arial", 16, "bold"), pady=10).pack(fill="x", pady=(0, 20))

        buttons = ["Inicio", "Registro de Paciente", "Administrar Personal", "Ver Camillas y Asignaciones"]
        for name in buttons:
            btn = tk.Button(self.sidebar, text=name, bg=self.colors["primary"], fg=self.colors["text_light"],
                            relief="flat", font=("Arial", 11, "bold"),
                            command=lambda n=name: self.show_frame(n))
            btn.pack(fill="x", pady=5, padx=10, ipady=8)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["button_hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["primary"]))

        btn_exit = tk.Button(self.sidebar, text="Salir", bg=self.colors["error"], fg=self.colors["text_light"],
                            relief="flat", font=("Arial", 11, "bold"), command=self.on_closing)
        btn_exit.pack(fill="x", pady=5, padx=10, ipady=8)
        btn_exit.bind("<Enter>", lambda e, b=btn_exit: b.config(bg="#C0392B"))
        btn_exit.bind("<Leave>", lambda e, b=btn_exit: b.config(bg=self.colors["error"]))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir de la aplicación?"):
            self._save_data() 
            self.destroy()

    def create_inicio_frame(self, frame):
        tk.Label(frame, text="Bienvenido al Sistema de Gestión Hospitalaria",
                 bg=self.colors["background"], font=("Arial", 24, "bold"), fg=self.colors["primary"]).pack(pady=50)
        tk.Label(frame, text="Utilice el menú lateral para navegar por las opciones.",
                 bg=self.colors["background"], font=("Arial", 16), fg=self.colors["text_dark"]).pack(pady=20)
        tk.Label(frame, text="Este sistema le permite registrar personal y pacientes, asignar camillas y gestionar el estado del hospital.",
                 bg=self.colors["background"], font=("Arial", 12), fg=self.colors["text_dark"], wraplength=500).pack(pady=10)

    def create_registro_paciente_frame(self, frame):
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Registro de Paciente", bg=self.colors["background"], font=("Arial", 18, "bold"), fg=self.colors["primary"]).grid(row=0, column=0, columnspan=2, pady=(20, 15))

        self._create_label_entry(frame, "Nombre:", "pac_nombre", 1)
        self._create_label_entry(frame, "Edad:", "pac_edad", 2)
        self._create_label_entry(frame, "Enfermedad:", "pac_enfermedad", 3)
        self._create_label_entry(frame, "No. Seguro Social:", "pac_seguro_social", 4)

        tk.Label(frame, text="Área Requerida:", bg=self.colors["background"], font=("Arial", 12), fg=self.colors["text_dark"]).grid(row=5, column=0, padx=20, sticky="w")
        self.combo_registro_area = ttk.Combobox(frame, values=self.areas_paciente_disponibles, state="readonly", font=("Arial", 12))
        self.combo_registro_area.grid(row=5, column=1, padx=20, pady=5, sticky="ew")
        if self.areas_paciente_disponibles:
            self.combo_registro_area.set(self.areas_paciente_disponibles[0])

        self.combo_registro_area.bind("<<ComboboxSelected>>", self.update_personal_comboboxes_for_patient_registration)

        tk.Label(frame, text="Doctor Asignado:", bg=self.colors["background"], font=("Arial", 12), fg=self.colors["text_dark"]).grid(row=6, column=0, padx=20, sticky="w")
        self.combo_doctor_registro = ttk.Combobox(frame, values=[], state="readonly", font=("Arial", 12))
        self.combo_doctor_registro.grid(row=6, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(frame, text="Enfermero Asignado:", bg=self.colors["background"], font=("Arial", 12), fg=self.colors["text_dark"]).grid(row=7, column=0, padx=20, sticky="w")
        self.combo_enfermero_registro = ttk.Combobox(frame, values=[], state="readonly", font=("Arial", 12))
        self.combo_enfermero_registro.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        btn_registrar = tk.Button(frame, text="Registrar Paciente", bg=self.colors["accent"], fg=self.colors["text_light"],
                                    font=("Arial", 12, "bold"), command=self.registrar_paciente_logic,
                                    relief="raised", bd=2, highlightbackground=self.colors["accent"], highlightthickness=1)
        btn_registrar.grid(row=8, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)
        btn_registrar.bind("<Enter>", lambda e, b=btn_registrar: b.config(bg=self.colors["button_hover"]))
        btn_registrar.bind("<Leave>", lambda e, b=btn_registrar: b.config(bg=self.colors["accent"]))

        self.update_personal_comboboxes_for_patient_registration()

    def _create_label_entry(self, parent_frame, text, var_name, row):
        tk.Label(parent_frame, text=text, bg=self.colors["background"], font=("Arial", 12), fg=self.colors["text_dark"]).grid(row=row, column=0, padx=20, sticky="w")
        entry = tk.Entry(parent_frame, font=("Arial", 12), bd=2, relief="groove")
        entry.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
        setattr(self, f"entry_{var_name}", entry)

    def update_personal_comboboxes_for_patient_registration(self, event=None):
        selected_area = self.combo_registro_area.get()

        available_doctors = [p.nombre for p in self.personal if p.area == selected_area and p.puesto == "Doctor" and not p.ocupado]
        self.combo_doctor_registro["values"] = available_doctors
        self.combo_doctor_registro.set(available_doctors[0] if available_doctors else "")

        available_enfermeros = [p.nombre for p in self.personal if p.area == selected_area and p.puesto == "Enfermero" and not p.ocupado]
        self.combo_enfermero_registro["values"] = available_enfermeros
        self.combo_enfermero_registro.set(available_enfermeros[0] if available_enfermeros else "")

    def registrar_paciente_logic(self):
        nombre = self.entry_pac_nombre.get().strip()
        edad_str = self.entry_pac_edad.get().strip()
        enfermedad = self.entry_pac_enfermedad.get().strip()
        seguro_social = self.entry_pac_seguro_social.get().strip()
        area = self.combo_registro_area.get().strip()
        selected_doctor_name = self.combo_doctor_registro.get().strip()
        selected_enfermero_name = self.combo_enfermero_registro.get().strip()

        if not all([nombre, edad_str, enfermedad, seguro_social, area, selected_doctor_name, selected_enfermero_name]):
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos, incluyendo la asignación de Doctor y Enfermero.")
            return

        try:
            edad = int(edad_str)
            if edad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error de entrada", "La edad debe ser un número entero positivo.")
            return

        if area not in self.camillas:
            messagebox.showerror("Error de asignación", f"El área '{area}' no tiene camillas asignadas para pacientes.")
            return

        camilla_info = next((c_data for c_data in self.camillas[area] if not c_data["ocupada"]), None)
        if camilla_info is None:
            messagebox.showerror("Error de asignación", f"No hay camillas disponibles en el área de '{area}'.")
            return

        doctor_asignado_obj = next((p for p in self.personal if p.nombre == selected_doctor_name and p.area == area and p.puesto == "Doctor" and not p.ocupado), None)
        enfermero_asignado_obj = next((p for p in self.personal if p.nombre == selected_enfermero_name and p.area == area and p.puesto == "Enfermero" and not p.ocupado), None)

        if not doctor_asignado_obj:
            messagebox.showerror("Error de asignación", f"El Doctor '{selected_doctor_name}' no está disponible, no pertenece a '{area}' o ya está ocupado.")
            return
        if not enfermero_asignado_obj:
            messagebox.showerror("Error de asignación", f"El Enfermero '{selected_enfermero_name}' no está disponible, no pertenece a '{area}' o ya está ocupado.")
            return

        doctor_asignado_obj.ocupado = True
        enfermero_asignado_obj.ocupado = True
        camilla_info["ocupada"] = True

        paciente = Paciente(nombre, edad, area, camilla_info["id"], doctor_asignado_obj, enfermero_asignado_obj, enfermedad, seguro_social)
        self.pacientes.append(paciente)

        messagebox.showinfo("Registro Exitoso", f"Paciente {nombre} registrado en camilla {camilla_info['id']} de {area}.\nDoctor: {doctor_asignado_obj.nombre}\nEnfermero: {enfermero_asignado_obj.nombre}")
        self.limpiar_campos_registro_paciente()
        self.actualizar_tablas_display()
        self.update_personal_comboboxes_for_patient_registration()

    def limpiar_campos_registro_paciente(self):
        self.entry_pac_nombre.delete(0, tk.END)
        self.entry_pac_edad.delete(0, tk.END)
        self.entry_pac_enfermedad.delete(0, tk.END)
        self.entry_pac_seguro_social.delete(0, tk.END)
        if self.areas_paciente_disponibles:
            self.combo_registro_area.set(self.areas_paciente_disponibles[0])
        self.combo_doctor_registro.set("")
        self.combo_enfermero_registro.set("")

    def create_administrar_personal_frame(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Administrar Personal", bg=self.colors["background"], font=("Arial", 18, "bold"), fg=self.colors["primary"]).pack(pady=(20, 10))

        btn_registrar_personal = tk.Button(frame, text="Registrar Nuevo Personal", command=self.registrar_personal_popup,
                   bg=self.colors["accent"], fg=self.colors["text_light"], font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_registrar_personal.pack(pady=10)
        btn_registrar_personal.bind("<Enter>", lambda e, b=btn_registrar_personal: b.config(bg=self.colors["button_hover"]))
        btn_registrar_personal.bind("<Leave>", lambda e, b=btn_registrar_personal: b.config(bg=self.colors["accent"]))


        self.personal_table = ttk.Treeview(frame, columns=(
            "Nombre", "Puesto", "Área", "Especialidad", "F. Nac.", "Contratación", "Sexo",
            "Grado Estudio", "Posgrado", "Cédula", "Domicilio", "Teléfono", "Correo", "F. Ingreso", "¿Ocupado?"
        ), show="headings")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background=self.colors["background"],
                        foreground=self.colors["text_dark"],
                        rowheight=25,
                        fieldbackground=self.colors["background"])
        style.map('Treeview', background=[('selected', self.colors["accent"])])
        style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        background=self.colors["secondary"],
                        foreground=self.colors["text_light"])
        style.map("Treeview.Heading", background=[('active', self.colors["primary"])])


        for col in self.personal_table["columns"]:
            self.personal_table.heading(col, text=col.replace("_", " "))
            self.personal_table.column(col, width=100, anchor=tk.W if col not in ["F. Nac.", "F. Ingreso", "¿Ocupado?"] else tk.CENTER)

        self.personal_table.pack(pady=15, padx=20, fill="both", expand=True)

        personal_scrollbar_y = ttk.Scrollbar(self.personal_table, orient="vertical", command=self.personal_table.yview)
        personal_scrollbar_x = ttk.Scrollbar(self.personal_table, orient="horizontal", command=self.personal_table.xview)
        self.personal_table.configure(yscrollcommand=personal_scrollbar_y.set, xscrollcommand=personal_scrollbar_x.set)
        personal_scrollbar_y.pack(side="right", fill="y")
        personal_scrollbar_x.pack(side="bottom", fill="x")

        action_button_frame = tk.Frame(frame, bg=self.colors["background"])
        action_button_frame.pack(pady=10)

        btn_edit = tk.Button(action_button_frame, text="Editar Personal Seleccionado", command=self.editar_personal,
                   bg=self.colors["secondary"], fg=self.colors["text_light"], font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_edit.grid(row=0, column=0, padx=5)
        btn_edit.bind("<Enter>", lambda e, b=btn_edit: b.config(bg=self.colors["primary"]))
        btn_edit.bind("<Leave>", lambda e, b=btn_edit: b.config(bg=self.colors["secondary"]))

        btn_delete = tk.Button(action_button_frame, text="Eliminar Personal Seleccionado", command=self.eliminar_personal,
                   bg=self.colors["error"], fg=self.colors["text_light"], font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_delete.grid(row=0, column=1, padx=5)
        btn_delete.bind("<Enter>", lambda e, b=btn_delete: b.config(bg="#C0392B"))
        btn_delete.bind("<Leave>", lambda e, b=btn_delete: b.config(bg=self.colors["error"]))

    def actualizar_tabla_personal(self):
        for item in self.personal_table.get_children():
            self.personal_table.delete(item)

        for p in self.personal:
            data = [
                p.nombre, p.puesto, p.area, p.especialidad, p.fecha_nacimiento,
                p.tipo_contratacion, p.sexo, p.ultimo_grado_estudio, p.posgrado,
                p.cedula_profesional, p.domicilio, p.telefono, p.correo_electronico,
                p.fecha_ingreso, "Sí" if p.ocupado else "No"
            ]
            self.personal_table.insert("", tk.END, values=data)

    def _create_personal_popup_fields(self, popup, personal_obj=None):
        fields = {}
        row_idx = 0

        sexo_options = ["Femenino", "Masculino"]
        grado_estudio_options = ["Doctorado", "Maestría", "Licenciatura", "Técnico Superior Universitario", "Técnico General"]
        puesto_options = ["Doctor", "Enfermero", "Otro"]


        labels_entries_vars = [
            ("Nombre:", "nombre", "entry"),
            ("Fecha de nacimiento (YYYY-MM-DD):", "fecha_nacimiento", "entry"),
            ("Tipo de Contratación:", "tipo_contratacion", "combo", ["Permanente", "Temporal", "Servicio Social", "Voluntario"]),
            ("Sexo:", "sexo", "combo", sexo_options),
            ("Último Grado de Estudio:", "ultimo_grado_estudio", "combo", grado_estudio_options),
            ("Especialidad:", "especialidad", "entry"),
            ("Posgrado:", "posgrado", "entry"),
            ("Cédula Profesional:", "cedula_profesional", "entry"),
            ("Domicilio:", "domicilio", "entry"),
            ("Teléfono:", "telefono", "entry"),
            ("Correo Electrónico:", "correo_electronico", "entry"),
            ("Fecha de Ingreso (YYYY-MM-DD):", "fecha_ingreso", "entry"),
            ("Área:", "area", "combo", self.areas_personal_disponibles),
            ("Puesto:", "puesto", "combo", puesto_options)
        ]

        for text, key, widget_type, *options in labels_entries_vars:
            tk.Label(popup, text=text, bg=self.colors["background"], fg=self.colors["text_dark"]).grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            if widget_type == "entry":
                entry = tk.Entry(popup, font=("Arial", 10))
                entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                if personal_obj and hasattr(personal_obj, key):
                    entry.insert(0, getattr(personal_obj, key))
                fields[key] = entry
                if personal_obj and key == "nombre":
                    entry.config(state='readonly')
            elif widget_type == "combo":
                var = tk.StringVar(popup)
                combo = ttk.Combobox(popup, values=options[0], state="readonly", textvariable=var, font=("Arial", 10))
                combo.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                if personal_obj and hasattr(personal_obj, key) and getattr(personal_obj, key) in options[0]:
                    var.set(getattr(personal_obj, key))
                else:
                    var.set(options[0][0] if options[0] else "")
                fields[key] = var
                fields[f'combo_{key}'] = combo
            row_idx += 1

        fields['current_row_index'] = row_idx
        return fields

    def _validate_personal_data(self, data, is_new_entry=True, current_personal_obj=None, parent_popup=None):
        required_fields = ["nombre", "fecha_nacimiento", "tipo_contratacion", "sexo", "ultimo_grado_estudio",
                           "domicilio", "telefono", "correo_electronico", "fecha_ingreso", "area", "puesto"]

        if not all(data.get(field) for field in required_fields):
            messagebox.showerror("Error de validación", "Todos los campos obligatorios deben ser completados.", parent=parent_popup)
            return False

        try:
            datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d")
            datetime.strptime(data['fecha_ingreso'], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error de validación", "El formato de fecha debe ser (AAAA-MM-DD).", parent=parent_popup)
            return False

        if is_new_entry or (current_personal_obj and data['cedula_profesional'] != current_personal_obj.cedula_profesional):
            if data['cedula_profesional'] and any(p.cedula_profesional == data['cedula_profesional'] for p in self.personal if p.cedula_profesional and p != current_personal_obj):
                messagebox.showerror("Error de validación", "Ya existe personal con esa cédula profesional.", parent=parent_popup)
                return False

        if is_new_entry:
            if any(p.nombre == data['nombre'] for p in self.personal):
                messagebox.showerror("Error de validación", "Ya existe personal con ese nombre.", parent=parent_popup)
                return False
        
        if current_personal_obj and current_personal_obj.ocupado and data['area'] != current_personal_obj.area:
            messagebox.showerror("Error de edición", f"No se puede cambiar el área del personal '{current_personal_obj.nombre}' mientras esté ocupado. Primero libérelo de cualquier paciente.", parent=parent_popup)
            return False

        return True

    def registrar_personal_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Registrar Nuevo Personal")
        popup.transient(self)
        popup.grab_set()
        popup.config(bg=self.colors["background"])
        popup.grid_columnconfigure(1, weight=1)

        fields = self._create_personal_popup_fields(popup)
        row_idx = fields['current_row_index']

        def guardar():
            data = {k: v.get() if isinstance(v, tk.StringVar) else v.get().strip() for k, v in fields.items() if k not in ['current_row_index'] and not k.startswith('combo_')}
            
            if not self._validate_personal_data(data, is_new_entry=True, parent_popup=popup):
                return

            new_personal = PersonalHospital(**data)
            self.personal.append(new_personal)
            messagebox.showinfo("Éxito", f"Personal '{new_personal.nombre}' registrado.", parent=popup)
            self.actualizar_tablas_display()
            self.update_personal_comboboxes_for_patient_registration()
            popup.destroy()

        btn_save_personal = tk.Button(popup, text="Guardar Personal", command=guardar, bg=self.colors["accent"], fg=self.colors["text_light"], font=("Arial", 10, "bold"))
        btn_save_personal.grid(row=row_idx, column=0, columnspan=2, pady=10)
        btn_save_personal.bind("<Enter>", lambda e, b=btn_save_personal: b.config(bg=self.colors["button_hover"]))
        btn_save_personal.bind("<Leave>", lambda e, b=btn_save_personal: b.config(bg=self.colors["accent"]))

    def editar_personal(self):
        try:
            item_id = self.personal_table.selection()[0]
            values = self.personal_table.item(item_id, 'values')
            nombre_actual = values[0]

            personal_obj = next((p for p in self.personal if p.nombre == nombre_actual), None)
            if not personal_obj:
                messagebox.showwarning("Error", "No se encontró el personal para editar.")
                return

            popup = tk.Toplevel(self)
            popup.title(f"Editar Personal: {personal_obj.nombre}")
            popup.transient(self)
            popup.grab_set()
            popup.config(bg=self.colors["background"])
            popup.grid_columnconfigure(1, weight=1)

            fields = self._create_personal_popup_fields(popup, personal_obj)
            row_idx = fields['current_row_index']

            def guardar_edicion():
                data = {k: v.get() if isinstance(v, tk.StringVar) else v.get().strip() for k, v in fields.items() if k not in ['current_row_index'] and not k.startswith('combo_')}
                
                if not self._validate_personal_data(data, is_new_entry=False, current_personal_obj=personal_obj, parent_popup=popup):
                    return

                personal_obj.fecha_nacimiento = data['fecha_nacimiento']
                personal_obj.tipo_contratacion = data['tipo_contratacion']
                personal_obj.sexo = data['sexo']
                personal_obj.ultimo_grado_estudio = data['ultimo_grado_estudio']
                personal_obj.especialidad = data['especialidad']
                personal_obj.posgrado = data['posgrado']
                personal_obj.cedula_profesional = data['cedula_profesional']
                personal_obj.domicilio = data['domicilio']
                personal_obj.telefono = data['telefono']
                personal_obj.correo_electronico = data['correo_electronico']
                personal_obj.fecha_ingreso = data['fecha_ingreso']
                personal_obj.area = data['area']
                personal_obj.puesto = data['puesto']

                messagebox.showinfo("Éxito", f"Personal {personal_obj.nombre} actualizado correctamente.", parent=popup)
                self.actualizar_tablas_display()
                self.update_personal_comboboxes_for_patient_registration()
                popup.destroy()

            btn_save_changes = tk.Button(popup, text="Guardar Cambios", command=guardar_edicion,
                       bg=self.colors["accent"], fg=self.colors["text_light"], font=("Arial", 10, "bold"))
            btn_save_changes.grid(row=row_idx, column=0, columnspan=2, pady=10)
            btn_save_changes.bind("<Enter>", lambda e, b=btn_save_changes: b.config(bg=self.colors["button_hover"]))
            btn_save_changes.bind("<Leave>", lambda e, b=btn_save_changes: b.config(bg=self.colors["accent"]))

        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un personal de la tabla para editar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al editar: {e}")

    def eliminar_personal(self):
        try:
            item_id = self.personal_table.selection()[0]
            values = self.personal_table.item(item_id, 'values')
            nombre_a_eliminar = values[0]

            personal_obj_to_remove = next((p for p in self.personal if p.nombre == nombre_a_eliminar), None)

            if personal_obj_to_remove and personal_obj_to_remove.ocupado:
                messagebox.showerror("Error", f"No se puede eliminar a {nombre_a_eliminar} mientras esté asignado a un paciente. Primero libérelo.")
                return

            self.personal[:] = [p for p in self.personal if p.nombre != nombre_a_eliminar]

            messagebox.showinfo("Éxito", f"Personal {nombre_a_eliminar} eliminado correctamente.")
            self.actualizar_tablas_display()
            self.update_personal_comboboxes_for_patient_registration()

        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un personal de la tabla para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def create_ver_camillas_frame(self, frame):
        tk.Label(frame, text="Estado de Camillas y Asignaciones", bg=self.colors["background"], font=("Arial", 18, "bold"), fg=self.colors["primary"]).pack(pady=(20, 10))

        self.camillas_table = ttk.Treeview(frame, columns=("Paciente", "Edad", "Enfermedad", "Seguro Social", "Área", "Camilla", "Doctor Asignado", "Enfermero Asignado"), show="headings")
        self.camillas_table.heading("Paciente", text="Paciente")
        self.camillas_table.heading("Edad", text="Edad")
        self.camillas_table.heading("Enfermedad", text="Enfermedad")
        self.camillas_table.heading("Seguro Social", text="No. SS")
        self.camillas_table.heading("Área", text="Área")
        self.camillas_table.heading("Camilla", text="Camilla")
        self.camillas_table.heading("Doctor Asignado", text="Doctor Asignado")
        self.camillas_table.heading("Enfermero Asignado", text="Enfermero Asignado")

        self.camillas_table.column("Paciente", width=120, anchor=tk.W)
        self.camillas_table.column("Edad", width=50, anchor=tk.CENTER)
        self.camillas_table.column("Enfermedad", width=100, anchor=tk.W)
        self.camillas_table.column("Seguro Social", width=100, anchor=tk.W)
        self.camillas_table.column("Área", width=80, anchor=tk.CENTER)
        self.camillas_table.column("Camilla", width=70, anchor=tk.CENTER)
        self.camillas_table.column("Doctor Asignado", width=120, anchor=tk.W)
        self.camillas_table.column("Enfermero Asignado", width=120, anchor=tk.W)

        self.camillas_table.pack(pady=15, padx=20, fill="both", expand=True)

        camillas_scrollbar = ttk.Scrollbar(self.camillas_table, orient="vertical", command=self.camillas_table.yview)
        self.camillas_table.configure(yscrollcommand=camillas_scrollbar.set)
        camillas_scrollbar.pack(side="right", fill="y")

        liberar_frame = tk.Frame(frame, bg=self.colors["background"])
        liberar_frame.pack(pady=10)

        tk.Label(liberar_frame, text="Paciente para Dar de Alta (Liberar Camilla):", bg=self.colors["background"], font=("Arial", 12), fg=self.colors["text_dark"]).pack(side="left", padx=10)
        self.combo_liberar_camilla = ttk.Combobox(liberar_frame, state="readonly", font=("Arial", 12), width=40)
        self.combo_liberar_camilla.pack(side="left", padx=10)

        btn_liberar = tk.Button(liberar_frame, text="Dar de Alta Paciente", command=self.liberar_camilla_logic,
                                 bg=self.colors["error"], fg=self.colors["text_light"], font=("Arial", 10, "bold"))
        btn_liberar.pack(side="left", padx=10)
        btn_liberar.bind("<Enter>", lambda e, b=btn_liberar: b.config(bg="#C0392B"))
        btn_liberar.bind("<Leave>", lambda e, b=btn_liberar: b.config(bg=self.colors["error"]))

    def actualizar_tabla_camillas(self):
        for item in self.camillas_table.get_children():
            self.camillas_table.delete(item)

        liberar_options = []
        for paciente in self.pacientes:
            doctor_nombre = paciente.doctor_asignado.nombre if paciente.doctor_asignado else "N/A"
            enfermero_nombre = paciente.enfermero_asignado.nombre if paciente.enfermero_asignado else "N/A"
            camilla_id = paciente.camilla if paciente.camilla else "N/A"

            self.camillas_table.insert("", tk.END, values=(
                paciente.nombre, paciente.edad, paciente.enfermedad, paciente.seguro_social,
                paciente.area, camilla_id, doctor_nombre, enfermero_nombre
            ))
            if paciente.camilla != "N/A":
                liberar_options.append(f"{paciente.nombre} (Camilla: {camilla_id}, Área: {paciente.area})")

        self.combo_liberar_camilla["values"] = liberar_options
        self.combo_liberar_camilla.set("No hay pacientes ocupando camillas" if not liberar_options else "")

    def liberar_camilla_logic(self):
        selected_text = self.combo_liberar_camilla.get()
        if not selected_text or selected_text == "No hay pacientes ocupando camillas":
            messagebox.showwarning("Advertencia", "Seleccione un paciente de la lista para darlo de alta.")
            return

        try:
            paciente_nombre_str, rest = selected_text.split(" (Camilla: ", 1)
            camilla_id_part, area_part = rest.split(", Área: ", 1)
            camilla_id = int(camilla_id_part.strip())
            area = area_part.replace(")", "").strip()

        except ValueError:
            messagebox.showerror("Error", "Formato de selección incorrecto. Formato esperado: 'Nombre (Camilla: X, Área: Y)'")
            return

        paciente_a_liberar = next((p for p in self.pacientes if p.nombre == paciente_nombre_str and p.camilla == camilla_id and p.area == area), None)

        if not paciente_a_liberar:
            messagebox.showerror("Error", "No se encontró el paciente o la asignación de camilla. Puede que ya haya sido dado de alta.")
            return

        found_camilla = False
        for camilla_data in self.camillas.get(paciente_a_liberar.area, []):
            if camilla_data["id"] == paciente_a_liberar.camilla and camilla_data["ocupada"]:
                camilla_data["ocupada"] = False
                found_camilla = True
                break

        if not found_camilla:
            messagebox.showerror("Error Interno", "La camilla no se encontró marcada como ocupada. Verifique el estado.")
            return

        def is_personal_still_needed(personnel_obj_to_check, current_patient_being_freed):
            for pat in self.pacientes:
                if pat != current_patient_being_freed:
                    if pat.doctor_asignado == personnel_obj_to_check or \
                       pat.enfermero_asignado == personnel_obj_to_check:
                        return True
            return False

        if paciente_a_liberar.doctor_asignado and not is_personal_still_needed(paciente_a_liberar.doctor_asignado, paciente_a_liberar):
            paciente_a_liberar.doctor_asignado.ocupado = False

        if paciente_a_liberar.enfermero_asignado and not is_personal_still_needed(paciente_a_liberar.enfermero_asignado, paciente_a_liberar):
            paciente_a_liberar.enfermero_asignado.ocupado = False

        self.pacientes.remove(paciente_a_liberar)

        messagebox.showinfo("Éxito", f"Paciente {paciente_a_liberar.nombre} dado de alta y camilla {camilla_id} liberada. El personal asociado ha sido liberado si no está asignado a otros pacientes.")
        self.actualizar_tablas_display()
        self.update_personal_comboboxes_for_patient_registration()

    def actualizar_tablas_display(self):
        self.update_idletasks()
        self.actualizar_tabla_personal()
        self.actualizar_tabla_camillas()


if __name__ == "__main__":
    app = App()
    app.mainloop()
