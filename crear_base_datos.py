import sqlite3

# Conectar o crear base de datos
conn = sqlite3.connect("infotec_posgrados.db")
cursor = conn.cursor()

# Crear la tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT,
    generacion TEXT,
    fecha_inicio TEXT,
    nombre_estudiante TEXT,
    genero TEXT,
    estatus TEXT,
    becado TEXT,
    supervisor TEXT,
    institucion TEXT,
    nombre_actividad TEXT,
    inicio_actividad TEXT,
    fin_actividad TEXT,
    modalidad_titulacion INTEGER,
    titulo_trabajo TEXT,
    asesor TEXT,
    vobo_asesor TEXT,
    nombre_revisor TEXT,
    vobo_revisor TEXT,
    fecha_titulacion TEXT,
    estatus_biblioteca INTEGER,
    fecha_vobo_biblioteca TEXT,
    observaciones TEXT
)
""")

conn.commit()
conn.close()

print("✅ Base de datos creada con éxito: infotec_posgrados.db")
