from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import MySQLdb
import os
from werkzeug.utils import secure_filename

# Conexión a la base de datos con timeout y autocommit
conn = MySQLdb.connect(
    host="bzhahp9gear4wppnvuw8-mysql.services.clever-cloud.com",
    user="uenogooku1xj27kq",
    passwd="kJMRU7ehR4CWs81gsEBK",
    db="bzhahp9gear4wppnvuw8",
    connect_timeout=60,  # Aumenta el tiempo de espera de la conexión a 60 segundos
    autocommit=True      # Activar autocommit
)
cursor = conn.cursor()

# Inicialización de Flask
app = Flask(__name__)

# Configuración de carpeta de subida para fotos
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que la carpeta de subidas exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Enlaces de navegación
enlaces = [
    {"url": "/", "texto": "Home"},
    {"url": "/create", "texto": "Create"},
    {"url": "/read", "texto": "Read"},
    {"url": "/update", "texto": "Update"},
    {"url": "/delete", "texto": "Delete"}
]

def nombre_Columnas():
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Employes' ORDER BY ORDINAL_POSITION")
    columns_DB = [column[0] for column in cursor.fetchall()]
    return columns_DB

# Rutas de la aplicación
@app.route('/')
def init():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace["url"] != "/"]
    return render_template('index.html', enlaces=enlaces_filtrados)

@app.route('/create')
def create():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace["url"] != "/create"]
    return render_template('create.html', enlaces=enlaces_filtrados)

# Función para ejecutar consultas con manejo de reconexión
def execute_query(query, params):
    try:
        conn.ping(True)
        cursor.execute(query, params)
        conn.commit()
    except MySQLdb.OperationalError as e:
        if e.args[0] == 2006:
            print("Reconnecting to the database due to lost connection...")
            conn.ping(True)
            cursor.execute(query, params)
            conn.commit()
        else:
            raise e

# Ruta para procesar el formulario de creación de empleados
@app.route('/procesar', methods=['POST'])
def data_create():
    name = request.form['name']
    last_name = request.form['last-name']
    document = request.form['document']
    address = request.form['address']
    cell = request.form['cell-phone']
    
    # Guardar imagen en el sistema de archivos
    photo = request.files['photo']
    photo_filename = secure_filename(photo.filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
    photo.save(photo_path)  # Guardar la imagen
    
    # Guardar solo la ruta de la imagen en la base de datos
    query = """INSERT INTO Employes (Nombre, Apellido, Documento, Direccion, Telefono, Foto)
               VALUES (%s, %s, %s, %s, %s, %s);"""
    params = (name, last_name, document, address, cell, photo_filename)
    
    execute_query(query, params)  # Ejecutar la consulta con manejo de reconexión
    return redirect(url_for('create'))

# Servir imágenes subidas
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete')
def delete():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace["url"] != "/delete"]
    columns_DB = nombre_Columnas()
    cursor.execute("SELECT * FROM Employes")
    tabla = cursor.fetchall()
    return render_template('delete.html', enlaces=enlaces_filtrados, columns_DB=columns_DB, tabla=tabla)

@app.route('/selection_delete', methods=['POST'])
def selection_delete():
    id_delete = request.form['id_delete']
    cursor.execute("SELECT MAX(Id) FROM Employes")
    max_id = cursor.fetchall()[0][0]
    cursor.execute(f"DELETE FROM Employes WHERE Id = {id_delete}")
    cursor.execute(f"ALTER TABLE Employes AUTO_INCREMENT = {max_id - 1}")
    if int(id_delete) < max_id:
        cursor.execute(f"UPDATE Employes SET Id = Id - 1 WHERE Id > {id_delete}")
    return delete()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5001)
