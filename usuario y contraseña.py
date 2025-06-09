import tkinter as tk
from tkinter import messagebox


usuarios = {} #guarda los usuarios y contrasñas


def registrar(): #funcion para registrarte ya seas nuevo
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if usuario in usuarios:
        messagebox.showerror("Error", "El usuario ya existe.")
    elif usuario == "" or contrasena == "":
        messagebox.showerror("Error", "Rellena todos los campos.")
    else:
        usuarios[usuario] = contrasena
        messagebox.showinfo("Registro exitoso", f"Usuario '{usuario}' registrado.")
        entry_usuario.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)


def iniciar_sesion(): #funcion para poder ingresar con tu contraseña y usuario
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if usuario in usuarios and usuarios[usuario] == contrasena:
        messagebox.showinfo("Acceso concedido", f"Bienvenido, {usuario}.")
        entry_usuario.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


ventana = tk.Tk()
ventana.title("Plataforma de usuarios")
ventana.geometry("300x200")


tk.Label(ventana, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(ventana)
entry_usuario.pack()

tk.Label(ventana, text="Contraseña:").pack(pady=5)
entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.pack()


tk.Button(ventana, text="Registrar", command=registrar).pack(pady=5)
tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion).pack(pady=5)


ventana.mainloop()
