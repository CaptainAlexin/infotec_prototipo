import tkinter as tk
from tkinter import ttk, messagebox
import db  # Importamos tu archivo de base de datos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de estudiantes INFOTEC")
        self.root.geometry("1400x700")

        self.campos = db.obtener_estudiantes()[0][1:]  # Omitimos el ID
        self.datos = db.obtener_estudiantes()[1]

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_datos()

    def crear_formulario(self):
        self.entradas = {}
        frame_form = tk.Frame(self.root)
        frame_form.pack(pady=10)

        for idx, campo in enumerate(self.campos):
            label = tk.Label(frame_form, text=campo, width=20, anchor="w")
            label.grid(row=idx//4, column=(idx%4)*2, padx=5, pady=3)

            entrada = tk.Entry(frame_form, width=25)
            entrada.grid(row=idx//4, column=(idx%4)*2 + 1, padx=5, pady=3)
            self.entradas[campo] = entrada

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_estudiante).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_estudiante).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_estudiante).pack(side="left", padx=5)

    def crear_tabla(self):
        columnas, _ = db.obtener_estudiantes()
        self.tree = ttk.Treeview(self.root, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_fila)

        self.tree.pack(expand=True, fill="both")

    def cargar_datos(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        columnas, registros = db.obtener_estudiantes()
        for row in registros:
            self.tree.insert("", "end", values=row)

    def limpiar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def seleccionar_fila(self, event):
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")
        self.id_seleccionado = valores[0]
        for i, campo in enumerate(self.campos):
            self.entradas[campo].delete(0, tk.END)
            self.entradas[campo].insert(0, valores[i+1])

    def agregar_estudiante(self):
        data = [self.entradas[campo].get() for campo in self.campos]
        if any(d == "" for d in data):
            messagebox.showwarning("Validación", "Todos los campos deben estar completos.")
            return
        db.insertar_estudiante(tuple(data))
        self.limpiar_formulario()
        self.cargar_datos()

    def actualizar_estudiante(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showinfo("Actualizar", "Selecciona un estudiante para actualizar.")
            return
        data = [self.entradas[campo].get() for campo in self.campos]
        db.actualizar_estudiante(self.id_seleccionado, tuple(data))
        self.limpiar_formulario()
        self.cargar_datos()

    def eliminar_estudiante(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showinfo("Eliminar", "Selecciona un estudiante para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?")
        if confirm:
            db.eliminar_estudiante(self.id_seleccionado)
            self.limpiar_formulario()
            self.cargar_datos()

# Punto de entrada (si ejecutas directamente este archivo)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

