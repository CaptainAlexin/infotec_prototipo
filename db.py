import sqlite3

DB_NAME = "infotec_posgrados.db"

def crear_conexion():
    return sqlite3.connect(DB_NAME)

def obtener_estudiantes():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    datos = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    return columnas, datos

def insertar_estudiante(data):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO estudiantes (
            matricula, generacion, fecha_inicio, nombre_estudiante, genero,
            estatus, becado, supervisor, institucion, nombre_actividad,
            inicio_actividad, fin_actividad, modalidad_titulacion, titulo_trabajo,
            asesor, vobo_asesor, nombre_revisor, vobo_revisor, fecha_titulacion,
            estatus_biblioteca, fecha_vobo_biblioteca, observaciones
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def actualizar_estudiante(id, data):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE estudiantes SET
            matricula=?, generacion=?, fecha_inicio=?, nombre_estudiante=?, genero=?,
            estatus=?, becado=?, supervisor=?, institucion=?, nombre_actividad=?,
            inicio_actividad=?, fin_actividad=?, modalidad_titulacion=?, titulo_trabajo=?,
            asesor=?, vobo_asesor=?, nombre_revisor=?, vobo_revisor=?, fecha_titulacion=?,
            estatus_biblioteca=?, fecha_vobo_biblioteca=?, observaciones=?
        WHERE id=?
    """, data + (id,))
    conn.commit()
    conn.close()

def eliminar_estudiante(id):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id=?", (id,))
    conn.commit()
    conn.close()
