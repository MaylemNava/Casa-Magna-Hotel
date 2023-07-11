# Del módulo flask importar la clase Flask y los métodos jsonify,request 
from flask import Flask ,jsonify ,request 
# Del módulo flask_cors importar CORS, se usa en una api rest, permite conectar desde el frontend a una api. 
from flask_cors import CORS
# Los siguientes módulos ayudan al manejo de la base de datos. 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

app=Flask(__name__) # crear el objeto app de la clase Flask CORS(app) # Módulo

# configuro la base de datos, con el nombre el usuario y la clave 
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/proyecto' 
# URI de la BBDD. Driver de la BD user:clave@URLBBDD/nombreBBDD 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none

db= SQLAlchemy(app) #crea el objeto db de la clase SQLAlchemy 
ma=Marshmallow(app) 
#crea el objeto ma de de la clase Marshmallow


# Definir la tabla 
class Producto(db.Model): 
# clase Producto hereda de db.Model 
# # Define los campos de la tabla 
 id = db.Column(db.Integer, primary_key=True)
 nombre = db.Column(db.String(100))
 precio=db.Column(db.Integer)
 stock=db.Column(db.Integer)
 imagen=db.Column(db.String(400)) 
def __init__(self,nombre,precio,stock,imagen): 
    # crea el constructor de la clase self.nombre=nombre 
    # # No hace falta el id porque lo crea sola mysql por ser auto_incremento 
    self.precio=precio 
    self.stock=stock 
    self.imagen=imagen
    
with app.app_context(): 
    db.create_all()
    
class ProductoSchema(ma.Schema): 
    class Meta: 
        fields=('id','nombre','precio','stock','imagen')
        
#El objeto producto_schema es para traer un producto 
producto_schema=ProductoSchema() 
# El objeto productos_schema es para traer múltiples registros de producto 
productos_schema=ProductoSchema(many=True)

#CREAR LAS RUTAS PARA: productos
#'/productos' ENDPOINT PARA RECIBIR DATOS: POST
#'/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS DISPONIBLES EN LA BASE DE DATOS: GET
#'/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
#'/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
#'/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT # 

@app.route('/productos',methods=['GET']) 
def get_productos(): 
    # El metodo query.all() lo hereda de db.Model 
    # # Permite obtener todos los datos de la tabla Producto 
    all_productos=Producto.query.all() 
    # # Transforma un listado de objetos a JSON 
    return productos_schema.jsonify(all_productos)




if __name__=='__main__':
    app.run(debug=True)