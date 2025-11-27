import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from src.usuario import Usuario
from src.artista import Artista
from src.admin import Admin

from src.track import Track
from src.tracklist import Tracklist

current_user = None

def login_inicial():
    global current_user

    tiene = messagebox.askyesno("Bienvenido", "¿Tienes una cuenta?")
    if tiene is None:
        salir()
        return

    if not tiene:
        u = registrar_usuario_publico()
        if u:
            current_user = u
            lbl_user.config(text=f"Conectado: {u.nombre} ({u.tipo})")
            ajustar_menu_por_rol()
            return
        else:
            messagebox.showinfo("Info", "Registro cancelado.")

    # Intentos de login
    for _ in range(3):
        login = simpledialog.askstring("Iniciar sesión", "Usuario:")
        if login is None:
            salir()
            return
        pwd = simpledialog.askstring("Iniciar sesión", "Contraseña:", show='*')
        if pwd is None:
            salir()
            return

        usuario = Usuario.autenticar(login.strip(), pwd)
        if usuario:
            current_user = usuario
            lbl_user.config(text=f"Conectado: {usuario.nombre} ({usuario.tipo})")
            ajustar_menu_por_rol()
            return
        else:
            retry = messagebox.askretrycancel("Error", "Credenciales incorrectas.")
            if not retry:
                want_reg = messagebox.askyesno("Registro", "¿Deseas registrarte?")
                if want_reg:
                    u = registrar_usuario_publico()
                    if u:
                        current_user = u
                        lbl_user.config(text=f"Conectado: {u.nombre} ({u.tipo})")
                        ajustar_menu_por_rol()
                        return
    messagebox.showerror("Error", "Demasiados intentos fallidos.")
    salir()

def registrar_usuario_publico():
    nombre = simpledialog.askstring("Registro", "Nombre:")
    if not nombre:
        return None

    tipo = simpledialog.askstring("Registro", "Tipo (usuario/artista/admin):", initialvalue="usuario")
    if tipo is None:
        return None

    if tipo not in ("usuario", "artista", "admin"):
        messagebox.showwarning("Tipo inválido", "Tipo inválido. Se usará 'usuario'.")
        tipo = "usuario"

    pwd = simpledialog.askstring("Contraseña", "Contraseña:", show="*")

    if tipo == "usuario":
        u = Usuario.crear(nombre, pwd)
    elif tipo == "artista":
        bio = simpledialog.askstring("Bio", "Biografía:", initialvalue="")
        u = Artista.crear(nombre, pwd, bio=bio)
    else:
        u = Admin.crear(nombre, pwd)

    messagebox.showinfo("OK", f"Usuario creado: {u.nombre} ({u.tipo})")
    return u

def requiere_artista_o_admin(func):
    def wrapper(*args, **kwargs):
        if current_user.tipo not in ("artista", "admin"):
            messagebox.showerror("Permisos", "Solo artistas o admin pueden hacer esto.")
            return
        return func(*args, **kwargs)
    return wrapper

# MENU

def listar_tracks():
    try:
        tracks = Track.listar_todos()
        lst_output.delete(0, tk.END)
        if not tracks:
            lst_output.insert(tk.END, "No hay canciones registradas.")
            return
        lst_output.insert(tk.END, "Canciones:")
        for t in tracks:
            lst_output.insert(tk.END, f"[{t.id}] {t.titulo} Artista: {t.artista_id} {t.duracion}s")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar tracks: \n{e}")

def listar_playlists():
    try:
        playlists = Tracklist.listar_todos_playlists()
        lst_output.delete(0, tk.END)
        if not playlists:
            lst_output.insert(tk.END, "No hay playlists registradas.")
            return
        for p in playlists:
            lst_output.insert(tk.END, f"[{p.id}] {p.titulo} Usuario: {p.usuario_id} {p.lanzamiento}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar playlists: \n{e}")

def listar_albums():
    try:
        albums = Tracklist.listar_todos_albums()
        lst_output.delete(0, tk.END)
        if not albums:
            lst_output.insert(tk.END, "No hay albums registradas.")
            return
        for a in albums:
            lst_output.insert(tk.END, f"[{a.id}] {a.titulo} Artista: {a.usuario_id} {a.lanzamiento}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar albums: \n{e}")

def listar_artistas():
    try:
        artistas = Artista.listar_todos()
        lst_output.delete(0, tk.END)
        if not artistas:
            lst_output.insert(tk.END, "No hay artistas registrados.")
            return
        lst_output.insert(tk.END, "Artistas:")
        for a in artistas:
            lst_output.insert(tk.END, f"[{a.id}] {a.nombre} Followers: {a.followers}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar artistas: \n{e}")

# MENU DESPLEGABLE

def crear_playlist():
    # Disponible para todos
    # TODO: implementar
    messagebox.showinfo("Crear playlist", "TODO: implementar crear_playlist()")


@requiere_artista_o_admin
def crear_track():
    # TODO: implementar
    messagebox.showinfo("Crear track", "TODO: implementar crear_track()")


@requiere_artista_o_admin
def crear_album():
    # TODO: implementar
    messagebox.showinfo("Crear álbum", "TODO: implementar crear_album()")


@requiere_artista_o_admin
def eliminar_track():
    # TODO: implementar
    messagebox.showinfo("Eliminar track", "TODO: implementar eliminar_track()")


@requiere_artista_o_admin
def eliminar_tracklist():
    # TODO: implementar
    messagebox.showinfo("Eliminar tracklist", "TODO: implementar eliminar_tracklist()")

# AJUSTES SEGUN EL ROL

def ajustar_menu_por_rol():
    tipo = current_user.tipo
    menu_acciones.entryconfig("Crear track", state="normal" if tipo in ("artista", "admin") else "disabled")
    menu_acciones.entryconfig("Crear álbum", state="normal" if tipo in ("artista", "admin") else "disabled")
    menu_acciones.entryconfig("Eliminar track", state="normal" if tipo in ("artista", "admin") else "disabled")
    menu_acciones.entryconfig("Eliminar tracklist", state="normal" if tipo in ("artista", "admin") else "disabled")

    # Crear playlist siempre está habilitado
    menu_acciones.entryconfig("Crear playlist", state="normal")

# CERRAR APP

def salir():
    root.destroy()
    sys.exit()

# INTERFAZ

root = tk.Tk()
root.title("Sistema de Música")

# Marco principal
frame_main = ttk.Frame(root)
frame_main.pack(fill="both", expand=True, padx=10, pady=10)

# Columna izquierda (botones)
frame_left = ttk.Frame(frame_main)
frame_left.pack(side="left", fill="y", padx=5)

ttk.Button(frame_left, text="Listar tracks", command=listar_tracks).pack(fill="x", pady=3)
ttk.Button(frame_left, text="Listar playlists", command=listar_playlists).pack(fill="x", pady=3)
ttk.Button(frame_left, text="Listar álbumes", command=listar_albums).pack(fill="x", pady=3)
ttk.Button(frame_left, text="Listar artistas", command=listar_artistas).pack(fill="x", pady=3)

# Panel derecho (listbox)
frame_right = ttk.Frame(frame_main)
frame_right.pack(side="right", fill="both", expand=True)

lbl_user = ttk.Label(frame_right, text="No conectado")
lbl_user.pack(anchor="ne")

lst_output = tk.Listbox(frame_right, width=60, height=25)
lst_output.pack(fill="both", expand=True)

# Menú superior
menu_bar = tk.Menu(root)
menu_acciones = tk.Menu(menu_bar, tearoff=0)

menu_acciones.add_command(label="Crear playlist", command=crear_playlist)
menu_acciones.add_command(label="Crear track", command=crear_track)
menu_acciones.add_command(label="Crear álbum", command=crear_album)
menu_acciones.add_separator()
menu_acciones.add_command(label="Eliminar track", command=eliminar_track)
menu_acciones.add_command(label="Eliminar tracklist", command=eliminar_tracklist)

menu_bar.add_cascade(label="Acciones", menu=menu_acciones)
root.config(menu=menu_bar)

# Inicio de login
root.after(100, login_inicial)

root.mainloop()
