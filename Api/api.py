from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'database-1.ctae2g6iq6cd.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin123_123'
app.config['MYSQL_DB'] = 'FRESHTRACK'

mysql = MySQL(app)

@app.route('/get_users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id ,Nombre, correo, telefono, contraseña FROM USUARIOS")
    usuarios = cursor.fetchall()
    cursor.close()

    # Convertir los datos obtenidos a un formato JSON
    usuarios_list = []
    for usuario in usuarios:
     usuarios_list.append({
        "id": usuario[0],  # Asegúrate de incluir el ID
        "Nombre": usuario[1],
        "correo": usuario[2],
        "telefono": usuario[3],
        "contraseña": usuario[4]
    })

    return jsonify(usuarios_list)

# Ruta para insertar datos
@app.route('/insert_users', methods=['POST'])
def insert_users():
    details = request.json
    nombre = details['Nombre']
    correo = details['correo']
    telefono = details['telefono']
    contrasena = details['contraseña']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO USUARIOS (Nombre, correo, telefono, contraseña) VALUES (%s, %s, %s, %s)", (nombre, correo, telefono, contrasena))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Datos insertados correctamente"})

@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    details = request.json
    nombre = details.get('Nombre')
    correo = details.get('correo')
    telefono = details.get('telefono')
    contrasena = details.get('contraseña')

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE USUARIOS SET Nombre = %s, correo = %s, telefono = %s, contraseña = %s WHERE id = %s", (nombre, correo, telefono, contrasena, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Usuario actualizado correctamente"})

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM USUARIOS WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"mensaje": "Error al eliminar el usuario", "error": str(e)}), 500
    
#PRODUCTO 
@app.route('/get_productos', methods=['GET'])
def get_productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ID, Folio, Nombre, Tipo, cantidad, fecha_entrada, fecha_salida, precio FROM PRODUCTOS")
    productos = cursor.fetchall()
    cursor.close()

    # Convertir los datos obtenidos a un formato JSON
    productos_list = []
    for item in productos:
        productos_list.append({
            "ID": item[0],
            "Folio": item[1],
            "Nombre": item[2],
            "Tipo": item[3],
            "cantidad": item[4],
            "fecha_entrada": item[5].isoformat() if item[5] else None,
            "fecha_salida": item[6].isoformat() if item[6] else None,
            "precio": item[7]
        })

    return jsonify(productos_list)

@app.route('/insert_producto', methods=['POST'])
def insert_producto():
    details = request.json
    folio = details['Folio']
    nombre = details['Nombre']
    tipo = details['Tipo']
    cantidad = details['cantidad']
    fecha_entrada = details['fecha_entrada']
    fecha_salida = details['fecha_salida']
    precio = details['precio']
    
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO PRODUCTOS (Folio, Nombre, Tipo, cantidad, fecha_entrada, fecha_salida, precio) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (folio, nombre, tipo, cantidad, fecha_entrada, fecha_salida, precio)
    )
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": "Datos insertados correctamente"})

@app.route('/update_producto/<int:id>', methods=['PUT'])
def update_producto(id):
    details = request.json
    folio = details.get('Folio')
    nombre = details.get('Nombre')
    tipo = details.get('Tipo')
    cantidad = details.get('cantidad')
    fecha_entrada = details.get('fecha_entrada')
    fecha_salida = details.get('fecha_salida')
    precio = details.get('precio')

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE PRODUCTOS SET Folio = %s, Nombre = %s, Tipo = %s, cantidad = %s, fecha_entrada = %s, fecha_salida = %s, precio = %s WHERE ID = %s",
        (folio, nombre, tipo, cantidad, fecha_entrada, fecha_salida, precio, id)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Producto actualizado correctamente"})

@app.route('/delete_producto/<int:id>', methods=['DELETE'])
def delete_producto(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM PRODUCTOS WHERE ID = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Producto eliminado correctamente"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
