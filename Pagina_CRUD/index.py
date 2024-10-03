#Librerias
from flask import Flask, render_template, request
import MySQLdb #mysqlclient


#Coneccion
conn = MySQLdb.connect(
    host= "bzhahp9gear4wppnvuw8-mysql.services.clever-cloud.com",
    user="uenogooku1xj27kq",
    passwd="kJMRU7ehR4CWs81gsEBK",
    db="bzhahp9gear4wppnvuw8"
)
cursor = conn.cursor()

#Inicailizacion de Fask
app = Flask(__name__)

#Lista
enlaces=[
    {"url":"/", "texto":"Home"},
    {"url":"/create", "texto":"Create"},
    {"url":"/read", "texto":"Read"},
    {"url":"/update", "texto":"Update"},
    {"url":"/delete", "texto":"Delete"}
]

def nombre_Columnas():
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Employes' ORDER BY ORDINAL_POSITION")
    columns_DB = [column[0] for column in cursor.fetchall()]
    return columns_DB


@app.route('/')
def init():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace["url"] != "/"]
    return render_template('index.html', enlaces=enlaces_filtrados)


@app.route('/create')
def create():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace ["url"] != "/create"]
    return render_template('create.html', enlaces=enlaces_filtrados)

@app.route('/procesar', methods=['POST'])
def data_create():
    name = request.form['name']
    last_name = request.form['last-name']
    document = request.form['document']
    address = request.form['address']
    cell = request.form['cell-phone']
    photo = request.form['photo']
    cursor.execute("""INSERT INTO Employes (Nombre, Apellido, Documento, Direccion, Telefono, Foto)
    VALUES (%s, %s, %s, %s, %s, LOAD_FILE(%s));""", (name, last_name, document, address, cell, photo))
    conn.commit()
    return create()


@app.route('/read')
def read( condition_fulfied = "", tabla = ""):
    enlaces_filtrados = [enlace for enlace in enlaces if enlace ["url"] != "/read"]
    columns_DB = nombre_Columnas()
    if condition_fulfied == "":
        cursor.execute("SELECT * FROM Employes")
        tabla = cursor.fetchall()
    else:
        tabla = condition_fulfied
    return render_template('read.html', enlaces=enlaces_filtrados, columns_DB = columns_DB, tabla = tabla)

@app.route('/column_selection', methods=['POST'])
def column_select():
    column = request.form['selection']
    condition_record = request.form['condition_record']
    if condition_record != "":
        cursor.execute(f"SELECT * FROM Employes WHERE {column} = '{condition_record}'")
    else:
        cursor.execute("SELECT * FROM Employes")
    condition_fulfied = cursor.fetchall()
    print(condition_fulfied)
    return read(condition_fulfied = condition_fulfied)


@app.route('/update')
def update(column = "", id = "", a = True):
    enlaces_filtrados = [enlace for enlace in enlaces if enlace ["url"] != "/update"]
    columns_DB = nombre_Columnas()
    cursor.execute("SELECT * FROM Employes")
    tabla = cursor.fetchall()
    if column == "":
        return render_template('update.html', enlaces=enlaces_filtrados, columns_DB = columns_DB, tabla = tabla)
    else:
        return render_template('update.html', enlaces=enlaces_filtrados, columns_DB = columns_DB, tabla = tabla, column = column, id = id, a = a)

@app.route('/selection_modify', methods=['POST'])
def selection_modify():
    id = request.form['id_selection']
    column = request.form['selection']
    print(f"El id es {id} y la columna es {column}")
    return update(column = column, id = id)

@app.route('/remplace_value', methods=['POST'])
def remplace_value():
    new_value = request.form['new_value']
    id = request.form['id']
    column = request.form['column']
    cursor.execute(f"UPDATE Employes SET {column} = '{new_value}' WHERE Id = {id}")
    return update()


@app.route('/delete')
def delete():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace ["url"] != "/delete"]
    columns_DB = nombre_Columnas()
    cursor.execute("SELECT * FROM Employes")
    tabla = cursor.fetchall()
    return render_template('delete.html', enlaces=enlaces_filtrados, columns_DB = columns_DB, tabla = tabla)

@app.route('/selection_delete', methods=['POST'])
def selection_delete():
    id_delete = request.form['id_delete']
    cursor.execute("SELECT  MAX(Id) FROM Employes")
    max_id = cursor.fetchall()[0][0]
    cursor.execute(f"DELETE FROM Employes WHERE Id = {id_delete}")
    cursor.execute(f"ALTER TABLE Employes AUTO_INCREMENT = {max_id - 1}")
    if int(id_delete) < max_id:
        cursor.execute(f"UPDATE Employes SET Id = Id - 1 WHERE Id > {id_delete}")
    return delete()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

#cursor.close()
#conn.close()