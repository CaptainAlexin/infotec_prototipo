import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import re
import db

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de estudiantes INFOTEC")
        self.root.geometry("1400x700")

        self.campos = db.obtener_estudiantes()[0][1:]  # Omitimos ID
        self.datos = db.obtener_estudiantes()[1]

        self.crear_buscador()
        self.crear_area_scrollable()
        self.crear_formulario()
        self.crear_tabla()
        self.cargar_datos()

    def crear_buscador(self):
        frame_busqueda = tk.Frame(self.root)
        frame_busqueda.pack(pady=5)

        tk.Label(frame_busqueda, text="Buscar:").pack(side="left", padx=5)
        self.entry_busqueda = tk.Entry(frame_busqueda, width=40)
        self.entry_busqueda.pack(side="left", padx=5)

        tk.Button(frame_busqueda, text="Buscar", command=self.buscar).pack(side="left", padx=5)
        tk.Button(frame_busqueda, text="Mostrar todos", command=self.cargar_datos).pack(side="left", padx=5)

    def crear_area_scrollable(self):
        container = tk.Frame(self.root)
        container.pack(fill="x")

        canvas = tk.Canvas(container, height=200)
        scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        self.form_frame = tk.Frame(canvas)

        self.form_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        self.canvas = canvas

    def crear_formulario(self):
        self.entradas = {}

        opciones_combobox = {
            "genero": ["Femenino", "Masculino", "Otro"],
            "estatus": ["Aprobado", "Titulado", "Baja definitiva"],
            "becado": ["Sí", "No"],
            "modalidad_titulacion": ["1", "2", "3", "4"],
            "vobo_asesor": ["Sí", "No"],
            "vobo_revisor": ["Sí", "No"],
            "estatus_biblioteca": ["1", "2", "3", "4"]
        }

        campos_fecha = ["fecha_inicio", "inicio_actividad", "fin_actividad", "fecha_titulacion", "fecha_vobo_biblioteca"]

        for idx, campo in enumerate(self.campos):
            label = tk.Label(self.form_frame, text=campo, width=20, anchor="w")
            label.grid(row=idx//4, column=(idx%4)*2, padx=5, pady=3)

            if campo in opciones_combobox:
                entrada = ttk.Combobox(self.form_frame, values=opciones_combobox[campo], state="readonly", width=22)
                entrada.current(0)
            elif campo in campos_fecha:
                entrada = DateEntry(self.form_frame, width=23, date_pattern='yyyy-mm-dd')
            else:
                entrada = tk.Entry(self.form_frame, width=25)

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
        for campo, entrada in self.entradas.items():
            if isinstance(entrada, ttk.Combobox):
                entrada.current(0)
            elif isinstance(entrada, DateEntry):
                entrada.set_date("2000-01-01")
            else:
                entrada.delete(0, tk.END)

    def seleccionar_fila(self, event):
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")
        self.id_seleccionado = valores[0]
        for i, campo in enumerate(self.campos):
            if isinstance(self.entradas[campo], ttk.Combobox):
                self.entradas[campo].set(valores[i+1])
            elif isinstance(self.entradas[campo], DateEntry):
                self.entradas[campo].set_date(valores[i+1])
            else:
                self.entradas[campo].delete(0, tk.END)
                self.entradas[campo].insert(0, valores[i+1])

    def validar_fecha(self, fecha):
        patron = r"^\d{4}-\d{2}-\d{2}$"
        return re.match(patron, fecha)

    def matricula_existente(self, matricula):
        _, registros = db.obtener_estudiantes()
        for r in registros:
            if r[1] == matricula:
                return True
        return False

    def agregar_estudiante(self):
        data = [self.entradas[campo].get() for campo in self.campos]

        if any(d == "" for d in data):
            messagebox.showwarning("Validación", "Todos los campos deben estar completos.")
            return

        fechas_a_validar = ["fecha_inicio", "inicio_actividad", "fin_actividad", "fecha_titulacion", "fecha_vobo_biblioteca"]
        for i, campo in enumerate(self.campos):
            if campo in fechas_a_validar and not self.validar_fecha(data[i]):
                messagebox.showerror("Error de formato", f"La fecha del campo '{campo}' no tiene el formato correcto (YYYY-MM-DD).")
                return

        matricula = self.entradas["matricula"].get()
        if self.matricula_existente(matricula):
            messagebox.showerror("Matrícula duplicada", f"La matrícula '{matricula}' ya existe.")
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

    def buscar(self):
        texto = self.entry_busqueda.get().lower()
        _, registros = db.obtener_estudiantes()

        resultados = []
        for fila in registros:
            if any(texto in str(celda).lower() for celda in fila[1:]):
                resultados.append(fila)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for fila in resultados:
            self.tree.insert("", "end", values=fila)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
