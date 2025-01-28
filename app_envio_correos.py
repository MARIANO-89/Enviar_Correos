import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
from dotenv import load_dotenv
import re

# Cargar variables de entorno
load_dotenv()
CORREO_EMISOR = os.getenv("EMAIL_SENDER")
CONTRASEÑA_APLICACION = os.getenv("EMAIL_PASSWORD")

if not CORREO_EMISOR or not CONTRASEÑA_APLICACION:
    messagebox.showerror("Error", "Las credenciales de correo no están configuradas. Verifica tu archivo .env")
    exit()

# Configuración de estilo
COLOR_FONDO = "#ffffff"
COLOR_TEXTO = "#000000"
COLOR_BOTON = "#0078D7"
COLOR_TEXTO_BOTON = "#ffffff"
COLOR_BARRA_PROGRESO = "#0078D7"
COLOR_TITULO = "#0078D7"
BORDER_RADIUS = 10


def validar_email(email):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, email)


def enviar_correos():
    try:
        subject = entry_asunto.get()
        message_body = txt_mensaje.get("1.0", tk.END).strip()
        archivo_csv = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV Files", "*.csv")],
            initialdir=os.path.join(os.path.expanduser('~'), 'Desktop', 'Padel')
        )

        if not archivo_csv:
            return

        df = pd.read_csv(archivo_csv, sep=';')

        if 'Email' not in df.columns or 'Nombre' not in df.columns:
            messagebox.showerror("Error", "El CSV debe contener las columnas 'Email' y 'Nombre'")
            return

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CORREO_EMISOR, CONTRASEÑA_APLICACION)

        total = len(df)
        barra_progreso['maximum'] = total
        barra_progreso['value'] = 0
        enviados = 0
        errores = 0

        for index, row in df.iterrows():
            email = row['Email'].strip()
            nombre = row['Nombre'].strip()

            if not validar_email(email):
                errores += 1
                continue

            msg = MIMEMultipart()
            msg['From'] = CORREO_EMISOR
            msg['Subject'] = subject
            msg['To'] = email
            mensaje_personalizado = f"""
            <html>
            <body>
                <p>Hola {nombre},</p>
                <p>{message_body}</p>
                <p>¡Esperamos verte pronto!</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(mensaje_personalizado, 'html'))
            server.sendmail(CORREO_EMISOR, email, msg.as_string())
            enviados += 1
            barra_progreso['value'] = index + 1
            root.update_idletasks()

        server.quit()
        messagebox.showinfo("Resultado", f"Correos enviados: {enviados}\nErrores en emails: {errores}")
        barra_progreso['value'] = 0

    except Exception as e:
        messagebox.showerror("Error", f"Error al enviar correos:\n{str(e)}")


root = tk.Tk()
root.title("Correos Monteverde Padel")
root.geometry("800x500")
root.configure(bg=COLOR_FONDO )

fuente_titulo = Font(family="Segoe UI", size=14, weight="bold")
fuente_normal = Font(family="Segoe UI", size=10)

marco_principal = ttk.Frame(root, padding=20)
marco_principal.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.configure('White.TFrame', background=COLOR_FONDO)
marco_principal.configure(style='White.TFrame')

# Título
lbl_titulo = ttk.Label(
    marco_principal,
    text="Correos Monteverde Padel",
    font=fuente_titulo,
    foreground=COLOR_TITULO,
    background=COLOR_FONDO,
    justify= "center"
)
lbl_titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

# Campos de entrada
ttk.Label(
    marco_principal,
    text="Asunto del Correo:",
    font=fuente_normal,
    foreground=COLOR_TEXTO,
    background=COLOR_FONDO,
    border= BORDER_RADIUS,
    justify= "center"
).grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_asunto = ttk.Entry(marco_principal, width=50, font=fuente_normal)
entry_asunto.grid(row=1, column=1, padx=10, pady=5)

# Área de mensaje
lbl_mensaje = ttk.Label(
    marco_principal,
    text="Cuerpo del Mensaje:",
    font=fuente_normal,
    foreground=COLOR_TEXTO,
    background=COLOR_FONDO,
    border= BORDER_RADIUS,
    justify= "center"
)
lbl_mensaje.grid(row=2, column=0, padx=10, pady=5, sticky="nw")

txt_mensaje = tk.Text(
    marco_principal,
    width=60,
    height=12,
    font=fuente_normal,
    wrap=tk.WORD,
    padx=5,
    pady=5,
    highlightthickness=2,
    highlightbackground=COLOR_BOTON,
    highlightcolor=COLOR_BOTON,
    relief=tk.GROOVE,
    borderwidth=5
)
txt_mensaje.grid(row=2, column=1, padx=10, pady=5)

barra_progreso = ttk.Progressbar(
    marco_principal,
    orient=tk.HORIZONTAL,
    length=400,
    mode='determinate',
    style="blue.Horizontal.TProgressbar"
)
barra_progreso.grid(row=3, column=0, columnspan=2, pady=20)

style.configure("Blue.TButton", background=COLOR_BOTON, foreground=COLOR_TEXTO_BOTON)

btn_enviar = ttk.Button(
    marco_principal,
    text="Enviar Correos 🚀",
    command=enviar_correos,
    style="Dark.TButton"
)
btn_enviar.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
