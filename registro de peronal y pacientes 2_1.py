import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


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

class Paciente(Persona):
    def __init__(self, nombre, edad, area, camilla=None, personal_asignado=None, enfermedad=None, seguro_social=None):
        super().__init__(nombre, edad)
        self.area = area
        self.camilla = camilla
        self.personal_asignado = personal_asignado if personal_asignado is not None else []
        self.enfermedad = enfermedad
        self.seguro_social = seguro_social

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Hospitalaria")
        self.attributes("-fullscreen", True)

        self.personal = []  #se creara una lista vacia sobre el personal

        self.camillas = {
            "Urgencias": [{"ocupada": False, "id": i + 1} for i in range(5)],
            "Hospitalización": [{"ocupada": False, "id": i + 1} for i in range(10)],
            "UCI": [{"ocupada": False, "id": i + 1} for i in range(3)]
        }
        self.areas_disponibles = list(self.camillas.keys())
        self.pacientes = []

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.frames_container = tk.Frame(self.main_frame, bg="white")
        self.frames_container.grid(row=0, column=1, sticky="nsew")
        self.frames_container.grid_rowconfigure(0, weight=1)
        self.frames_container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for name in ["Inicio", "Registro de Paciente", "Administrar Personal", "Ver Camillas y Asignaciones"]:
            frame = tk.Frame(self.frames_container, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.create_inicio_frame(self.frames["Inicio"])
        self.create_registro_paciente_frame(self.frames["Registro de Paciente"])
        self.create_administrar_personal_frame(self.frames["Administrar Personal"])
        self.create_ver_camillas_frame(self.frames["Ver Camillas y Asignaciones"])

        self.actualizar_tablas_display()
        
        self.show_frame("Inicio")

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#023035")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="MENÚ", bg="#0a5c64", fg="white",
                 font=("Arial", 16, "bold"), pady=10).pack(fill="x", pady=(0, 20))

        buttons = ["Inicio", "Registro de Paciente", "Administrar Personal", "Ver Camillas y Asignaciones"]
        for name in buttons:
            btn = tk.Button(self.sidebar, text=name, bg="#34495e", fg="white",
                            relief="flat", font=("Arial", 11, "bold"),
                            command=lambda n=name: self.show_frame(n))
            btn.pack(fill="x", pady=5, padx=10, ipady=8)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def create_inicio_frame(self, frame): #se creara la ventana principal donde nos dara el msj de bienvenida y nos dice que podemos hacer 
        tk.Label(frame, text="Bienvenido al Sistema de Gestión Hospitalaria",
                 bg="white", font=("Arial", 24, "bold"), fg="#0a2d31").pack(pady=50)
        tk.Label(frame, text="Utilice el menú lateral para navegar por las opciones.",
                 bg="white", font=("Arial", 16)).pack(pady=20)
        tk.Label(frame, text="Este sistema le permite registrar personal y pacientes, asignar camillas y gestionar el estado del hospital.",
                 bg="white", font=("Arial", 12), wraplength=500).pack(pady=10)

    def create_registro_paciente_frame(self, frame): #aqui se va a crear la def para registrar a los pacientes 
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Registro de Paciente", bg="white", font=("Arial", 18, "bold"), fg="#34495e").grid(row=0, column=0, columnspan=2, pady=(20, 15))

        self._create_label_entry(frame, "Nombre:", "pac_nombre", 1)
        self._create_label_entry(frame, "Edad:", "pac_edad", 2)
        self._create_label_entry(frame, "Enfermedad:", "pac_enfermedad", 3)
        self._create_label_entry(frame, "No. Seguro Social:", "pac_seguro_social", 4)

        tk.Label(frame, text="Área Requerida:", bg="white", font=("Arial", 12)).grid(row=5, column=0, padx=20, sticky="w")
        self.combo_registro_area = ttk.Combobox(frame, values=self.areas_disponibles, state="readonly", font=("Arial", 12))
        self.combo_registro_area.grid(row=5, column=1, padx=20, pady=5, sticky="ew")
        if self.areas_disponibles:
            self.combo_registro_area.set(self.areas_disponibles[0])
            
        self.combo_registro_area.bind("<<ComboboxSelected>>", self.update_personal_combobox)

        tk.Label(frame, text="Personal Asignado:", bg="white", font=("Arial", 12)).grid(row=6, column=0, padx=20, sticky="w")
        self.combo_personal_registro = ttk.Combobox(frame, values=[], state="readonly", font=("Arial", 12))
        self.combo_personal_registro.grid(row=6, column=1, padx=20, pady=5, sticky="ew")

        btn_registrar = tk.Button(frame, text="Registrar Paciente", bg="#158d9b", fg="white",
                                    font=("Arial", 12, "bold"), command=self.registrar_paciente_logic,
                                    relief="raised", bd=2, highlightbackground="#158d9b", highlightthickness=1)
        btn_registrar.grid(row=7, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

        self.update_personal_combobox()

    def _create_label_entry(self, parent_frame, text, var_name, row):
        tk.Label(parent_frame, text=text, bg="white", font=("Arial", 12)).grid(row=row, column=0, padx=20, sticky="w")
        entry = tk.Entry(parent_frame, font=("Arial", 12), bd=2, relief="groove")
        entry.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
        setattr(self, f"entry_{var_name}", entry)

    def update_personal_combobox(self, event=None):
        selected_area = self.combo_registro_area.get()
        available_personal = [p.nombre for p in self.personal if p.area == selected_area and not p.ocupado]
        self.combo_personal_registro["values"] = available_personal
        if available_personal:
            self.combo_personal_registro.set(available_personal[0])
        else:
            self.combo_personal_registro.set("")

    def registrar_paciente_logic(self):
        nombre = self.entry_pac_nombre.get().strip()
        edad_str = self.entry_pac_edad.get().strip()
        enfermedad = self.entry_pac_enfermedad.get().strip()
        seguro_social = self.entry_pac_seguro_social.get().strip()
        area = self.combo_registro_area.get().strip()
        selected_personal_name = self.combo_personal_registro.get().strip()

        if not all([nombre, edad_str, enfermedad, seguro_social, area, selected_personal_name]):
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        try:
            edad = int(edad_str)
            if edad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error de entrada", "La edad debe ser un número entero positivo.")
            return

        camilla_info = None
        for c_data in self.camillas.get(area, []):
            if not c_data["ocupada"]:
                camilla_info = c_data
                break

        if camilla_info is None:
            messagebox.showerror("Error de asignación", f"No hay camillas disponibles en el área de '{area}'.")
            return

        personal_asignado_obj = next((p for p in self.personal if p.nombre == selected_personal_name and p.area == area and not p.ocupado), None)
        if not personal_asignado_obj:
            messagebox.showerror("Error de asignación", f"El personal '{selected_personal_name}' no está disponible, no pertenece a '{area}' o ya está ocupado.")
            return

        camilla_info["ocupada"] = True
        personal_asignado_obj.ocupado = True

        paciente = Paciente(nombre, edad, area, camilla_info["id"], [personal_asignado_obj], enfermedad, seguro_social)
        self.pacientes.append(paciente)

        messagebox.showinfo("Registro Exitoso", f"Paciente {nombre} registrado en camilla {camilla_info['id']} de {area} con {personal_asignado_obj.puesto} {personal_asignado_obj.nombre}.")
        self.limpiar_campos_registro_paciente()
        self.actualizar_tablas_display()
        self.update_personal_combobox()

    def limpiar_campos_registro_paciente(self):
        self.entry_pac_nombre.delete(0, tk.END)
        self.entry_pac_edad.delete(0, tk.END)
        self.entry_pac_enfermedad.delete(0, tk.END)
        self.entry_pac_seguro_social.delete(0, tk.END)
        if self.areas_disponibles:
            self.combo_registro_area.set(self.areas_disponibles[0])
        self.combo_personal_registro.set("")

    def create_administrar_personal_frame(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Administrar Personal", bg="white", font=("Arial", 18, "bold"), fg="#34495e").pack(pady=(20, 10))

        tk.Button(frame, text="Registrar Nuevo Personal", command=self.registrar_personal_popup,
                   bg="#158d9b", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=10)

        self.personal_table = ttk.Treeview(frame, columns=(
            "Nombre", "Puesto", "Área", "Especialidad", "F. Nac.", "Contratación", "Sexo",
            "Grado Estudio", "Posgrado", "Cédula", "Domicilio", "Teléfono", "Correo", "F. Ingreso", "¿Ocupado?"
        ), show="headings")

        for col in self.personal_table["columns"]:
            self.personal_table.heading(col, text=col.replace("_", " "))
            self.personal_table.column(col, width=100, anchor=tk.W if col not in ["F. Nac.", "F. Ingreso", "¿Ocupado?"] else tk.CENTER)

        self.personal_table.pack(pady=15, padx=20, fill="both", expand=True)

        personal_scrollbar_y = ttk.Scrollbar(self.personal_table, orient="vertical", command=self.personal_table.yview)
        personal_scrollbar_x = ttk.Scrollbar(self.personal_table, orient="horizontal", command=self.personal_table.xview)
        self.personal_table.configure(yscrollcommand=personal_scrollbar_y.set, xscrollcommand=personal_scrollbar_x.set)
        personal_scrollbar_y.pack(side="right", fill="y")
        personal_scrollbar_x.pack(side="bottom", fill="x")

        action_button_frame = tk.Frame(frame, bg="white")
        action_button_frame.pack(pady=10)
        tk.Button(action_button_frame, text="Editar Personal Seleccionado", command=self.editar_personal,
                   bg="#34495e", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5)
        tk.Button(action_button_frame, text="Eliminar Personal Seleccionado", command=self.eliminar_personal,
                   bg="#b30000", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5)

    def actualizar_tabla_personal(self):
        if hasattr(self, 'personal_table') and self.personal_table.winfo_exists():
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

        labels_entries_vars = [
            ("Nombre:", "nombre", "entry"),
            ("Fecha de nacimiento (YYYY-MM-DD):", "fecha_nacimiento", "entry"),
            ("Tipo de Contratación:", "tipo_contratacion", "combo", ["Permanente", "Temporal", "Servicio Social", "Voluntario"]),
            ("Sexo:", "sexo", "combo", ["Femenino", "Masculino", "No binario", "Prefiero no decir"]),
            ("Último Grado de Estudio:", "ultimo_grado_estudio", "combo", ["Doctorado", "Maestría", "Licenciatura", "Técnico Superior Universitario", "Técnico General", "Bachillerato"]),
            ("Especialidad:", "especialidad", "entry"),
            ("Posgrado:", "posgrado", "entry"),
            ("Cédula Profesional:", "cedula_profesional", "entry"),
            ("Domicilio:", "domicilio", "entry"),
            ("Teléfono:", "telefono", "entry"),
            ("Correo Electrónico:", "correo_electronico", "entry"),
            ("Fecha de Ingreso (YYYY-MM-DD):", "fecha_ingreso", "entry"),
            ("Área:", "area", "combo", self.areas_disponibles),
            ("Puesto:", "puesto", "entry")
        ]

        for text, key, widget_type, *options in labels_entries_vars:
            tk.Label(popup, text=text).grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
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

    def registrar_personal_popup(self): #registraremos el diferente personal con la info pedida
        popup = tk.Toplevel(self)
        popup.title("Registrar Nuevo Personal")
        popup.transient(self)
        popup.grab_set()
        popup.grid_columnconfigure(1, weight=1)

        fields = self._create_personal_popup_fields(popup)
        row_idx = fields['current_row_index']

        def guardar():
            data = {k: v.get() if isinstance(v, tk.StringVar) else v.get().strip() for k, v in fields.items() if k not in ['current_row_index', 'combo_tipo_contratacion', 'combo_sexo', 'combo_ultimo_grado_estudio', 'combo_area']}
            
            required_fields = ["nombre", "fecha_nacimiento", "tipo_contratacion", "sexo", "ultimo_grado_estudio",
                               "domicilio", "telefono", "correo_electronico", "fecha_ingreso", "area", "puesto"]
            
            if not all(data.get(field) for field in required_fields):
                messagebox.showerror("Error", "Todos los campos obligatorios deben ser completados.", parent=popup)
                return

            try:
                datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d")
                datetime.strptime(data['fecha_ingreso'], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "El formato de fecha debe ser YYYY-MM-DD.", parent=popup)
                return

            if any(p.nombre == data['nombre'] for p in self.personal) or \
               (data['cedula_profesional'] and any(p.cedula_profesional == data['cedula_profesional'] for p in self.personal if p.cedula_profesional)):
                messagebox.showerror("Error", "Ya existe personal con ese nombre o cédula profesional.", parent=popup)
                return

            new_personal = PersonalHospital(**data)
            self.personal.append(new_personal)
            messagebox.showinfo("Éxito", f"Personal '{new_personal.nombre}' registrado.", parent=popup)
            self.actualizar_tabla_personal()
            self.update_personal_combobox()
            popup.destroy()

        tk.Button(popup, text="Guardar Personal", command=guardar, bg="#158d9b", fg="white", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, columnspan=2, pady=10)

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
            popup.grid_columnconfigure(1, weight=1)

            fields = self._create_personal_popup_fields(popup, personal_obj)
            row_idx = fields['current_row_index']

            def guardar_edicion():
                new_area = fields['area'].get().strip()
                if personal_obj.ocupado and personal_obj.area != new_area:
                    messagebox.showerror("Error de edición", f"No se puede cambiar el área del personal '{personal_obj.nombre}' mientras esté ocupado. Primero libérelo de cualquier paciente.")
                    return
                
                try:
                    datetime.strptime(fields['fecha_nacimiento'].get().strip(), "%Y-%m-%d") #esta funcion sirve para que la fecha tenga que coinsidir con el formato pedido
                    datetime.strptime(fields['fecha_ingreso'].get().strip(), "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "El formato de fecha debe ser YYYY-MM-DD.", parent=popup)
                    return

                personal_obj.fecha_nacimiento = fields['fecha_nacimiento'].get().strip()
                personal_obj.tipo_contratacion = fields['tipo_contratacion'].get().strip()
                personal_obj.sexo = fields['sexo'].get().strip()
                personal_obj.ultimo_grado_estudio = fields['ultimo_grado_estudio'].get().strip()
                personal_obj.especialidad = fields['especialidad'].get().strip()
                personal_obj.posgrado = fields['posgrado'].get().strip()
                personal_obj.cedula_profesional = fields['cedula_profesional'].get().strip()
                personal_obj.domicilio = fields['domicilio'].get().strip()
                personal_obj.telefono = fields['telefono'].get().strip()
                personal_obj.correo_electronico = fields['correo_electronico'].get().strip()
                personal_obj.fecha_ingreso = fields['fecha_ingreso'].get().strip()
                personal_obj.area = new_area
                personal_obj.puesto = fields['puesto'].get().strip()

                messagebox.showinfo("Éxito", f"Personal {personal_obj.nombre} actualizado correctamente.", parent=popup)
                self.actualizar_tabla_personal()
                self.update_personal_combobox()
                popup.destroy()

            tk.Button(popup, text="Guardar Cambios", command=guardar_edicion,
                       bg="#158d9b", fg="white", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, columnspan=2, pady=10)

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
            self.actualizar_tabla_personal()
            self.actualizar_tablas_display()
            self.update_personal_combobox()

        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un personal de la tabla para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def create_ver_camillas_frame(self, frame):
        tk.Label(frame, text="Estado de Camillas y Asignaciones", bg="white", font=("Arial", 18, "bold"), fg="#34495e").pack(pady=(20, 10))

        self.camillas_table = ttk.Treeview(frame, columns=("Paciente", "Edad", "Enfermedad", "Seguro Social", "Área", "Camilla", "Personal Asignado", "Puesto", "Especialidad"), show="headings")
        self.camillas_table.heading("Paciente", text="Paciente")
        self.camillas_table.heading("Edad", text="Edad")
        self.camillas_table.heading("Enfermedad", text="Enfermedad")
        self.camillas_table.heading("Seguro Social", text="No. SS")
        self.camillas_table.heading("Área", text="Área")
        self.camillas_table.heading("Camilla", text="Camilla")
        self.camillas_table.heading("Personal Asignado", text="Personal Asignado")
        self.camillas_table.heading("Puesto", text="Puesto")
        self.camillas_table.heading("Especialidad", text="Especialidad")

        self.camillas_table.column("Paciente", width=120, anchor=tk.W)
        self.camillas_table.column("Edad", width=50, anchor=tk.CENTER)
        self.camillas_table.column("Enfermedad", width=100, anchor=tk.W)
        self.camillas_table.column("Seguro Social", width=100, anchor=tk.W)
        self.camillas_table.column("Área", width=80, anchor=tk.CENTER)
        self.camillas_table.column("Camilla", width=70, anchor=tk.CENTER)
        self.camillas_table.column("Personal Asignado", width=120, anchor=tk.W)
        self.camillas_table.column("Puesto", width=100, anchor=tk.W)
        self.camillas_table.column("Especialidad", width=100, anchor=tk.W)

        self.camillas_table.pack(pady=15, padx=20, fill="both", expand=True)

        camillas_scrollbar = ttk.Scrollbar(self.camillas_table, orient="vertical", command=self.camillas_table.yview)
        self.camillas_table.configure(yscrollcommand=camillas_scrollbar.set)
        camillas_scrollbar.pack(side="right", fill="y")

        liberar_frame = tk.Frame(frame, bg="white")
        liberar_frame.pack(pady=10)

        tk.Label(liberar_frame, text="Liberar Camilla de Paciente:", bg="white", font=("Arial", 12)).pack(side="left", padx=10)
        self.combo_liberar_camilla = ttk.Combobox(liberar_frame, state="readonly", font=("Arial", 12), width=40)
        self.combo_liberar_camilla.pack(side="left", padx=10)

        btn_liberar = tk.Button(liberar_frame, text="Liberar Camilla", command=self.liberar_camilla_logic,
                                 bg="#4b0606", fg="white", font=("Arial", 10, "bold"))
        btn_liberar.pack(side="left", padx=10)

    def actualizar_tabla_camillas(self): # en esta def actualizamos las camillas si queremos liberar alguna o ver si estan ocupadas
        if hasattr(self, 'camillas_table') and self.camillas_table.winfo_exists():
            for item in self.camillas_table.get_children():
                self.camillas_table.delete(item)

            self.combo_liberar_camilla["values"] = []
            liberar_options = []

            for paciente in self.pacientes:
                personal_nombres = ", ".join([p.nombre for p in paciente.personal_asignado]) if paciente.personal_asignado else "N/A"
                personal_puestos = ", ".join([p.puesto for p in paciente.personal_asignado]) if paciente.personal_asignado else "N/A"
                personal_especialidades = ", ".join([p.especialidad for p in paciente.personal_asignado if p.especialidad]) if paciente.personal_asignado else "N/A"
                
                camilla_id = paciente.camilla if paciente.camilla else "N/A"

                self.camillas_table.insert("", tk.END, values=(
                    paciente.nombre, paciente.edad, paciente.enfermedad, paciente.seguro_social,
                    paciente.area, camilla_id, personal_nombres, personal_puestos, personal_especialidades
                ))
                if paciente.camilla != "N/A":
                    liberar_options.append(f"{paciente.nombre} (Camilla: {camilla_id}, Área: {paciente.area})")

            self.combo_liberar_camilla["values"] = liberar_options
            if liberar_options:
                self.combo_liberar_camilla.set("")
            else:
                self.combo_liberar_camilla.set("No hay camillas ocupadas")

    def liberar_camilla_logic(self):
        selected_text = self.combo_liberar_camilla.get()
        if not selected_text or selected_text == "No hay camillas ocupadas":
            messagebox.showwarning("Advertencia", "Seleccione un paciente de la lista para liberar su camilla.")
            return

        try:
            parts = selected_text.split(" (Camilla: ")
            if len(parts) < 2: raise ValueError("Formato de selección incorrecto.")
            paciente_nombre_str = parts[0].strip()
            camilla_info_str = parts[1].replace(")", "").strip()
            
            camilla_id_part = camilla_info_str.split(",")[0].replace("Camilla:", "").strip()
            camilla_id = int(camilla_id_part)
            area = camilla_info_str.split("Área: ")[1].strip()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la selección: {e}\nFormato esperado: 'Nombre (Camilla: X, Área: Y)'")
            return

        paciente_a_liberar = None
        for p in self.pacientes:
            if p.nombre == paciente_nombre_str and p.camilla == camilla_id and p.area == area:
                paciente_a_liberar = p
                break

        if not paciente_a_liberar:
            messagebox.showerror("Error", "No se encontró el paciente o la asignación de camilla. Puede que ya haya sido liberado.")
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

        for personal_obj in paciente_a_liberar.personal_asignado:
            is_personal_still_needed = False
            for pat in self.pacientes:
                if pat != paciente_a_liberar: 
                    if personal_obj in pat.personal_asignado:
                        is_personal_still_needed = True
                        break
            if not is_personal_still_needed:
                personal_obj.ocupado = False


        self.pacientes.remove(paciente_a_liberar)

        messagebox.showinfo("Éxito", f"Camilla {camilla_id} del paciente {paciente_a_liberar.nombre} liberada. El personal asociado ha sido liberado si no está asignado a otros pacientes.")
        self.actualizar_tablas_display()
        self.update_personal_combobox()

    def actualizar_tablas_display(self):
        self.update_idletasks() 
        self.actualizar_tabla_personal()
        self.actualizar_tabla_camillas()


if __name__ == "__main__":
    app = App()
    app.mainloop()
