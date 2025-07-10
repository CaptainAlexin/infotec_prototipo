import sqlite3
import random
from datetime import datetime, timedelta

# Conectar a la base de datos
conn = sqlite3.connect("infotec_posgrados.db")
cursor = conn.cursor()

# Listas de ejemplo
nombres = ["Ana López", "Luis Martínez", "María García", "Carlos Hernández", "Laura Torres", "José Ramírez"]
generos = ["Femenino", "Masculino", "Otro"]
estatus_list = ["Aprobado", "Titulado", "Baja definitiva"]
becado_list = ["Sí", "No"]
supervisores = ["Mtra. Pérez", "Dr. Ortega", "Ing. Luna"]
instituciones = ["INFOTEC AGS", "INFOTEC CDMX"]
actividades = ["Análisis de datos", "Desarrollo web", "Tesis aplicada", "Proyecto empresarial"]
modalidades = [1, 2, 3, 4]
vobos = ["Sí", "No"]
estatus_biblio = [1, 2, 3, 4]

# Generar fechas aleatorias
def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

# Rango de fechas posibles
fecha_inicio_base = datetime(2020, 1, 1)
fecha_fin_base = datetime(2025, 12, 31)

# Insertar 50 registros
for i in range(50):
    cursor.execute("""
        INSERT INTO estudiantes (
            matricula, generacion, fecha_inicio, nombre_estudiante, genero,
            estatus, becado, supervisor, institucion, nombre_actividad,
            inicio_actividad, fin_actividad, modalidad_titulacion, titulo_trabajo,
            asesor, vobo_asesor, nombre_revisor, vobo_revisor, fecha_titulacion,
            estatus_biblioteca, fecha_vobo_biblioteca, observaciones
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"MAT{1000 + i}",
        f"20{random.randint(20, 25)}",
        random_date(fecha_inicio_base, fecha_fin_base),
        random.choice(nombres),
        random.choice(generos),
        random.choice(estatus_list),
        random.choice(becado_list),
        random.choice(supervisores),
        random.choice(instituciones),
        random.choice(actividades),
        random_date(fecha_inicio_base, fecha_fin_base),
        random_date(fecha_inicio_base, fecha_fin_base),
        random.choice(modalidades),
        f"Tesis sobre {random.choice(actividades)}",
        random.choice(supervisores),
        random.choice(vobos),
        random.choice(supervisores),
        random.choice(vobos),
        random_date(fecha_inicio_base, fecha_fin_base),
        random.choice(estatus_biblio),
        random_date(fecha_inicio_base, fecha_fin_base),
        "Observaciones de ejemplo"
    ))

conn.commit()
conn.close()

print("✅ 50 registros de prueba insertados en la base de datos.")
