# IMPORTAR
# flask
# flask_cors
# flask_sqlalchemy
# flask_marshmallow

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Crear la app
app = Flask(__name__)

# Utilizar Cors, permite el acceso al frontend
CORS(app)

# CONFIGURACIÓN A LA BASE DE DATOS DESDE app
# (SE LE INFORMA A LA APP DONDE UBICAR LA BASE DE DATOS)
                                                    # //user:password@url/nombre de la base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

# Crear el objeto db
# Notifica a la app que trabajará con SQLAlchemy
db = SQLAlchemy(app)

# Objeto ma permite acceder a los métodos para transformar datos
ma = Marshmallow(app)

# DEFINICIÓN DE LA TABLA A PARTIR DE UNA CLASE (Producto)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre =db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self,nombre, precio,stock,imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen


# CÓDIGO DE CREACIÓN DE LA TABLA
with app.app_context():
    db.create_all()

# CREAR UNA CLASE  ProductoSchema, 
# DONDE SE DEFINEN LOS CAMPOS DE LA TABLA
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')

# CREAR DOS OBJETOS PARA TRANSFORMAR
producto_schema = ProductoSchema() # Permitir convertir un sólo dato. Ej: 1 objeto
productos_schema = ProductoSchema(many=True) # Permitir convertir un listado de datos. Ej: lista de objetos
    
# CREAR LAS RUTAS PARA: productos
# '/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS 
# DISPONIBLES EN LA BASE DE DATOS: GET

@app.route("/productos", methods=['GET'])
def get_productos():
    # Consulta toda la info de la tabla productos
    all_productos = Producto.query.all()
    return productos_schema.jsonify(all_productos)


# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    
    # Entrada de datos:
#     {
#       "imagen": "https://picsum.photos/200/300?grayscale",
#       "nombre": "MICROONDAS",
#       "precio": 50000,
#       "stock": 10
#    }

    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']

    new_producto=Producto(nombre,precio,stock,imagen)
    db.session.add(new_producto)
    db.session.commit()

    # Retornar los datos guardados en formato JSON 
    # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return producto_schema.jsonify(new_producto)


# '/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   


@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()
    
    # Devuelve un json con el registro eliminado
    # Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return producto_schema.jsonify(producto)   


# '/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT
@app.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
 
    #  Recibir los datos a modificar
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']

    # Del objeto resultante de la consulta modificar los valores  
    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    producto.imagen=imagen
#  Guardar los cambios
    db.session.commit()
# Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return producto_schema.jsonify(producto)



# BLOQUE PRINCIPAL 
if __name__=='__main__':
    app.run(debug=True)