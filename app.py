import os
from sqlite3 import Error
from flask import Flask, render_template, request, flash, session
from flask.helpers import url_for
from werkzeug.utils import redirect
import bcrypt

#Mis Archivos Importar
from formulario import formLogin, formUsuarios
from conexion import get_db, close_db

app = Flask(__name__)
app.secret_key = 'dafofndf9sadf'

#Semilla Para Encriptar usando gensalt()
semilla = bcrypt.gensalt()

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    form = formLogin()
    return render_template("login.html", form=form)

@app.route('/inicioSesion', methods=['GET','POST'])
def inicioSesion():
    form = formLogin()
    if (request.method == "POST"):
          email = request.form['email']
          password = request.form['password']

          password_encode = password.encode("utf-8")

          if form.validate_on_submit():

            db = get_db()
            cur = db.cursor()

            sQuery = "SELECT idUsuario,nombres,apellidos,direccion,telefono,email,contrasenia,idTipoUsuario FROM usuario WHERE email = ?"
            
            cur.execute(sQuery,[email])

            user = cur.fetchone()

            cur.close()

            if user is None: 
                error = 'Usuario o contraseña inválidos'
                flash( error )
            else:
                print("password", user[6])
                password_encriptado_encode = user[6]

                if bcrypt.checkpw(password_encode,password_encriptado_encode):
                    if user[7] == 1:
                        session["usuario"] = email 
                        session["nivel"] = "Super Administrador"
                        return redirect("/superadmin")
                    elif user[7] == 2:
                        session["usuario"] = email 
                        session["nivel"] = "administrador"
                        return redirect("/admin")
                    elif user[7] == 3:
                        session["usuario"] = email 
                        session["nivel"] = "Empleado"
                        return redirect("/colaborador")
            
            return render_template("login.html", form=form)

          else:
               return render_template("login.html", form=form)
     
    return render_template("login.html", form=form)

# Rutas ------     CONTROL ACCESO

@app.route('/superadmin', methods=["GET",'POST'])
def superadmin():
    return render_template("superadmin/main.html")

@app.route('/admin', methods=['GET','POST'])
def admin():
    return render_template("administrador/main.html")

@app.route('/colaborador', methods=['GET','POST'])
def colaborador():
    return render_template("empleado/main.html")

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect("/")

#Rutas -------- Control Formularios
@app.route('/registrarusuarios', methods=['GET', 'POST'])
def registrarusuarios():
    form = formUsuarios(request.form)
    if (request.method == 'GET'):
        # if 'usuario' in session:
            cursor = get_db().cursor()
            cursor.execute('SELECT idTipoUsuario,nombre FROM tipoUsuario ORDER BY idTipoUsuario')
            tipoUser = cursor.fetchall()
            cursor.close()
            return render_template("superadmin/registrouser.html", form=form, tipoUser=tipoUser)
    # else:
    #     return render_template("superadmin/registrouser.html")
    else:
        # POST y capturamos los datos del formulario:
        nombres = request.form['nombres'].strip().lower()
        apellidos = request.form['apellidos'].strip().lower()
        direccion = request.form['direccion'].strip().lower()
        telefono = request.form['telefono'].strip().lower()
        correo = request.form['correo'].strip().lower()

        contrasenia = request.form['contrasenia'].strip()
        #Encriptar contraseña usando semilla 
        password_encode = contrasenia.encode("utf-8")
        password_encriptada = bcrypt.hashpw(password_encode,semilla)

        tipoUser = request.form['tipoUser']

        try:
            sQuery = "INSERT INTO usuario (nombres,apellidos,direccion,telefono,email,contrasenia,idTipoUsuario) VALUES (?, ?, ?, ?, ?, ?, ?)"
        
            con = get_db()
            cur = con.cursor()
            cur.execute(sQuery,(nombres,apellidos,direccion,telefono,correo,password_encriptada,tipoUser))
            con.commit()
            con.close()
            error = ""
            if cur is None:
                error = "Error en el registro"
                flash(error,'error')
            else:
                error ="Exito"
                flash(error, 'success')
                return redirect("/registrarusuarios")
                
            # return error
        
        except Error:
            print( Error)

@app.route('/consultausuarios')
def consultausuarios():
    db = get_db()
    cur = db.cursor()

    sQuery = "SELECT * FROM usuario"

    cur.execute(sQuery)

    data = cur.fetchall()

    cur.close()
    # if (request.method == 'GET'):
    #     if 'usuario' in session:
    #         cursor = get_db().cursor()
    #         cursor.execute('SELECT idTipoUsuario,nombre,descripcion FROM tipoUsuario')
    #         tipoUser = cursor.fetchall()
    #         cursor.close()
    return render_template("superadmin/consultausuarios.html", usuarios = data)
    #     else:
    #         return redirect("/")
    # else:


@app.route('/eliminarusuario/<string:id>')
def eliminarusuario(id):
    try:
        db = get_db()
        cur = db.cursor()
        sQuery = "DELETE FROM usuario WHERE idUsuario = {0}".format(id)
        cur.execute(sQuery)
        flash("Eliminado Satisfactoriamente") # falta incluir mensaje
        db.commit()
        cur.close()
        db = close_db()
    except Error:
            print( Error)
            flash("Se ha detectado un error al intentar eliminar el registro")
    finally:
        return redirect(url_for('consultausuarios'))



@app.route('/editarusuario/<id>', methods=['GET','POST'])
def editarusuario(id):
    db = get_db() 
    cur = db.cursor() 

    sQuery = "SELECT * FROM usuario WHERE idUsuario = ?" 
    cur.execute(sQuery,[id])

    userEdit = cur.fetchone()
    cur.close()
    return render_template("superadmin/editarusuario.html" , usuario = userEdit)


@app.route('/updateusuario/<id>', methods = ['POST']) 
def updateusuario(id):

    if request.method == 'POST':
        #Captura de datos
        nombres = request.form['nombres'].strip().lower()
        apellidos = request.form['apellidos'].strip().lower()
        direccion = request.form['direccion'].strip().lower()
        telefono = request.form['telefono'].strip().lower()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        #Encriptar contraseña usando semilla 
        password_encode = password.encode("utf-8")
        password_encriptada = bcrypt.hashpw(password_encode,semilla)

        db = get_db() #Abre conexion
        cur = db.cursor() #Variable que tiene la conexion y cre un objeto de tipo cursor

        sQuery = """UPDATE usuario
                        SET nombres = ?,
                            apellidos = ?,
                            direccion = ?,
                            telefono = ?,
                            email = ?,
                            contrasenia = ?
                    WHERE idUsuario = ?""" 

        # sentencia SQL
        cur.execute(sQuery,(nombres,apellidos,direccion,telefono,email,password_encriptada,id)) #Preparamos la sentencia para ejecucion
        db.commit()
        cur.close() # cerramos el cursor
        db = close_db()
        return redirect(url_for("consultausuarios"))

    else:
        return redirect(url_for("superadmin"))

# Verificamos que exista una sesion
@app.before_request
def antes_de_cada_ruta():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and ruta !="/inicioSesion" and ruta != "/" and ruta != "/logout" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar
        
if  __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)