import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from src.db_connection import get_conn
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

def obtener_username_por_id(user_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()

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
            artista = obtener_username_por_id(t.artista_id)
            lst_output.insert(
                tk.END,
                f"[{t.id}] {t.titulo} - {artista} - ({t.duracion}s)"
            )
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
            usuario = obtener_username_por_id(p.usuario_id)
            lst_output.insert(
                tk.END,
                f"[{p.id}] {p.titulo} - {usuario} - {p.lanzamiento}"
            )
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar playlists: \n{e}")

def listar_albums():
    try:
        albums = Tracklist.listar_todos_albums()
        lst_output.delete(0, tk.END)
        if not albums:
            lst_output.insert(tk.END, "No hay albums registrados.")
            return
        for a in albums:
            artista = obtener_username_por_id(a.usuario_id)
            lst_output.insert(
                tk.END,
                f"[{a.id}] {a.titulo} - {artista} - {a.lanzamiento}"
            )
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
            lst_output.insert(tk.END, f"[{a.id}] {a.nombre} - Followers: {a.followers}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar artistas: \n{e}")

def listar_tracks_tracklist():
    titulo = simpledialog.askstring("Tracks de Tracklist", "Título del álbum/playlist:")
    if not titulo:
        return
    try:
        tracklist = Tracklist.buscar_por_title(titulo)
        if not tracklist:
            messagebox.showerror("Error", "No se encontró la tracklist.")
            return
        tracks = Tracklist.listar_tracks(tracklist.id)
        lst_output.delete(0, tk.END)
        if not tracks:
            lst_output.insert(tk.END, f"La tracklist '{titulo}' no tiene tracks.")
            return
        lst_output.insert(tk.END, f"Tracks de '{titulo}':")
        lst_output.insert(tk.END, "---------------------------------------")
        for t in tracks:
            linea = (
                f"{t['position']}. "
                f"{t['title']} "
                f"({t['duration']}s) - "
                f"{t['artist']}  "
                f"[ID: {t['track_id']}]"
            )
            lst_output.insert(tk.END, linea)
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar tracks de la tracklist:\n{e}")

# MENU DESPLEGABLE

def crear_playlist():
    titulo = simpledialog.askstring("Crear playlist", "Título de la playlist:")
    if not titulo:
        return
    try:
        tracklist_id = current_user.crear_tracklist(titulo)
        if tracklist_id is None:
            messagebox.showerror("Error", "No se puedo crear el tracklist (ver consola).")
            return
        messagebox.showinfo("OK", f"Playlist creado:\nID: {tracklist_id}\nTítulo: {titulo}")
        listar_playlists()
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear playlist: \n{e}")

@requiere_artista_o_admin
def crear_track():
    titulo = simpledialog.askstring("Crear track", "Título del track:")
    if not titulo:
        return
    dur_str = simpledialog.askstring("Crear track", "Duración en segundos:")
    if not dur_str:
        return
    try:
        duracion = int(dur_str)
        if duracion <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "La duración debe ser un número entero mayor a 0.")
        return

    try:
        track_id = current_user.crear_track(titulo, duracion)
        if track_id is None:
            messagebox.showerror("Error", "No se pudo crear el track (ver consola).")
            return
        messagebox.showinfo("OK", f"Track creado:\nID: {track_id}\nTítulo: {titulo}")
        listar_tracks()
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear track:\n{e}")

@requiere_artista_o_admin
def crear_album():
    titulo = simpledialog.askstring("Crear album", "Título del album:")
    if not titulo:
        return
    try:
        album_id = current_user.crear_album(titulo)
        if album_id is None:
            messagebox.showerror("Error", "No se pudo crear el album (ver consola).")
            return
        messagebox.showinfo("OK", f"Album creado:\nID: {album_id}\nTítulo: {titulo}")
        listar_albums()
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear album:\n{e}")

@requiere_artista_o_admin
def eliminar_track():
    titulo = simpledialog.askstring("Eliminar track", "Título del track a eliminar:")
    if not titulo:
        return
    track = Track.buscar_por_titulo(titulo)
    if track is None:
        messagebox.showwarning("No encontrado", "Track no encontrado.")
        return
    if messagebox.askyesno("Confirmar", f"Eliminar el track '{track.titulo} {track.artista_id}'?"):
        if current_user.eliminar_track(track.id):
            messagebox.showinfo("OK", f"Track eliminado")
    listar_tracks()

def eliminar_tracklist():
    titulo = simpledialog.askstring("Eliminar tracklist", "Título del tracklist a eliminar:")
    if not titulo:
        return
    tracklist = Tracklist.buscar_por_title(titulo)
    if tracklist is None:
        messagebox.showwarning("No encontrado", "Tracklist no encontrado.")
        return
    if messagebox.askyesno("Confirmar", f"Eliminar tracklist '{tracklist.titulo} {tracklist.usuario_id}'?"):
        if current_user.eliminar_tracklist(tracklist.id):
            messagebox.showinfo("OK", f"Tracklist eliminado")
    if tracklist.tipo == 'album':
        listar_albums()
    else:
        listar_playlists()

def agregar_track_tracklist():
    titulo_tracklist = simpledialog.askstring("Agregar track", "Título del álbum/playlist a modificar:")
    if not titulo_tracklist:
        return
    titulo_track = simpledialog.askstring("Agregar track", "Título del track a agregar:")
    if not titulo_track:
        return
    try:
        tracklist = Tracklist.buscar_por_title(titulo_tracklist)
        if tracklist is None:
            messagebox.showerror("Error", "No se encontró la tracklist.")
            return
        track = Track.buscar_por_titulo(titulo_track)
        if track is None:
            messagebox.showerror("Error", "No se encontró el track.")
            return

        if tracklist.tipo == "album":
            if current_user.tipo not in ("artista", "admin"):
                messagebox.showerror("Permisos", "Solo artistas o admin pueden modificar álbumes.")
                return
            if current_user.tipo == "artista" and track.artista_id != current_user.id:
                messagebox.showerror("Permisos", "Solo el artista dueño puede agregar canciones a su álbum.")
                return

        if tracklist.agregar_track(track.id):
            messagebox.showinfo("OK", f"Track agregado correctamente.")
            lst_output.delete(0, tk.END)
            lst_output.insert(0, f"Tracklist '{titulo_tracklist}' actualizada:")
            tracks = Tracklist.listar_tracks(tracklist.id)
            for t in tracks:
                lst_output.insert(tk.END, f"{t['position']}. {t['title']} - {t['artist']} ({t['duration']}s) [ID:{t['track_id']}]")
        else:
            messagebox.showerror("Error", "No se pudo agregar el track.")
    except Exception as e:
        messagebox.showerror("Error",
            f"Error al agregar track a la tracklist:\n{e}")

def eliminar_track_tracklist():
    titulo_tracklist = simpledialog.askstring("Eliminar track", "Título del álbum/playlist a modificar:")
    if not titulo_tracklist:
        return
    titulo_track = simpledialog.askstring("Eliminar track", "Título del track a eliminar:")
    if not titulo_track:
        return
    try:
        tracklist = Tracklist.buscar_por_title(titulo_tracklist)
        if tracklist is None:
            messagebox.showerror("Error", "No se encontró la tracklist.")
            return
        track = Track.buscar_por_titulo(titulo_track)
        if track is None:
            messagebox.showerror("Error", "No se encontró el track.")
            return

        if tracklist.tipo == "album":
            if current_user.tipo not in ("artista", "admin"):
                messagebox.showerror("Permisos", "Solo artistas o admin pueden modificar álbumes.")
                return
            if current_user.tipo == "artista" and track.artista_id != current_user.id:
                messagebox.showerror("Permisos", "Solo el artista dueño puede eliminar canciones de su álbum.")
                return

        if tracklist.eliminar_track(track.id):
            messagebox.showinfo("OK", f"Track eliminado correctamente.")
            lst_output.delete(0, tk.END)
            lst_output.insert(0, f"Tracklist '{titulo_tracklist}' actualizada:")
            tracks = Tracklist.listar_tracks(tracklist.id)
            for t in tracks:
                lst_output.insert(
                    tk.END,
                    f"{t['position']}. {t['title']} - {t['artist']} ({t['duration']}s) [ID:{t['track_id']}]"
                )
        else:
            messagebox.showerror("Error", "No se pudo eliminar el track (no existe en la tracklist).")
    except Exception as e:
        messagebox.showerror("Error",
            f"Error al eliminar track de la tracklist:\n{e}")

# AJUSTES SEGUN EL ROL

def ajustar_menu_por_rol():
    tipo = current_user.tipo
    menu_acciones.entryconfig("Crear track", state="normal" if tipo in ("artista", "admin") else "disabled")
    menu_acciones.entryconfig("Crear álbum", state="normal" if tipo in ("artista", "admin") else "disabled")
    menu_acciones.entryconfig("Eliminar track", state="normal" if tipo in ("artista", "admin") else "disabled")

    # Crear playlist siempre está habilitado
    menu_acciones.entryconfig("Crear playlist", state="normal")
    menu_acciones.entryconfig("Eliminar tracklist", state="normal")

# CERRAR APP

def salir():
    root.destroy()
    sys.exit()

# INTERFAZ

root = tk.Tk()
root.title("NOISE")
root.geometry("900x550")
root.update_idletasks()
root.config(bg="#2A2A2A")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 11), padding=6, background="#444", foreground="white")
style.map("TButton", background=[("active", "#666")])
style.configure("TLabel", background="#2A2A2A", foreground="white", font=("Segoe UI", 11))
style.configure("Left.TFrame", background="#1F1F1F")
style.configure("Right.TFrame", background="#2A2A2A")

frame_main = ttk.Frame(root, style="Right.TFrame")
frame_main.pack(fill="both", expand=True, padx=10, pady=10)
frame_main.configure(borderwidth=0)

frame_left = ttk.Frame(frame_main, style="Left.TFrame")
frame_left.pack(side="left", fill="y", padx=10, pady=10)
frame_left.configure(borderwidth=0, relief="flat")

ttk.Label(frame_left, text="NOISE", font=("Segoe UI", 14, "bold"), background="#1F1F1F").pack(pady=10)

button_width = 20
ttk.Button(frame_left, text="Listar tracks", width=button_width, command=listar_tracks).pack(pady=5)
ttk.Button(frame_left, text="Listar playlists", width=button_width, command=listar_playlists).pack(pady=5)
ttk.Button(frame_left, text="Listar álbumes", width=button_width, command=listar_albums).pack(pady=5)
ttk.Button(frame_left, text="Listar artistas", width=button_width, command=listar_artistas).pack(pady=5)
ttk.Button(frame_left, text="Listar tracks de tracklists", width=button_width, command=listar_tracks_tracklist).pack(pady=5)

frame_right = ttk.Frame(frame_main, style="Right.TFrame")
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
frame_right.configure(borderwidth=0, relief="flat")

lbl_user = ttk.Label(frame_right, text="No conectado", font=("Segoe UI", 10, "italic"))
lbl_user.pack(anchor="ne", pady=5)

lst_output = tk.Listbox(frame_right, width=60, height=22, bg="#1C1C1C", fg="white", selectbackground="#444", bd=0, highlightthickness=1, highlightbackground="#555")
lst_output.pack(fill="both", expand=True, pady=10)

menu_bar = tk.Menu(root, tearoff=0)
menu_acciones = tk.Menu(menu_bar, tearoff=0)
menu_acciones.add_command(label="Crear playlist", command=crear_playlist)
menu_acciones.add_command(label="Crear track", command=crear_track)
menu_acciones.add_command(label="Crear álbum", command=crear_album)
menu_acciones.add_separator()
menu_acciones.add_command(label="Agregar track a tracklist", command=agregar_track_tracklist)
menu_acciones.add_command(label="Eliminar track de tracklist", command=eliminar_track_tracklist)
menu_acciones.add_separator()
menu_acciones.add_command(label="Eliminar track", command=eliminar_track)
menu_acciones.add_command(label="Eliminar tracklist", command=eliminar_tracklist)

menu_bar.add_cascade(label="Acciones", menu=menu_acciones)
root.config(menu=menu_bar)

root.after(100, login_inicial)

root.mainloop()