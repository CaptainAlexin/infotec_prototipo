import sqlite3
import tkinter as tk
from tkinter import ttk

# Conexión a la base de datos
conn = sqlite3.connect("infotec_posgrados.db")
cursor = conn.cursor()

# Intentamos traer todos los registros
try:
    cursor.execute("SELECT * FROM estudiantes")
    registros = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    print(f"✅ Se encontraron {len(registros)} registros.")
except Exception as e:
    print("❌ Error al consultar la base de datos:", e)
    registros = []
    columnas = []

conn.close()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Visor de Estudiantes INFOTEC")
ventana.geometry("1200x600")

if registros:
    # Crear tabla (Treeview)
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

    # Definir encabezados
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")

    # Insertar registros
    for fila in registros:
        tabla.insert("", "end", values=fila)

    # Scrollbars
    scroll_y = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(ventana, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Layout
    tabla.pack(expand=True, fill="both")
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
else:
    # Mensaje si no hay registros
    mensaje = tk.Label(ventana, text="No se encontraron registros en la base de datos.", font=("Arial", 14))
    mensaje.pack(pady=20)

# Ejecutar ventana
ventana.mainloop()
