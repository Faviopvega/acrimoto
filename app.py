import os
from sqlite3 import Error
from flask import Flask, render_template, request, flash, session
from flask.helpers import url_for
from werkzeug.utils import redirect
import bcrypt

#Mis Archivos Importar
from formulario import formLogin, formUsuarios
from conexion import get_db

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
                        session["nivel"] = "administrador"
                        return redirect("/superadmin")
                    elif user[7] == 2:
                        session["usuario"] = email 
                        session["nivel"] = "docente"
                        return redirect("/admin")
                    elif user[7] == 3:
                        session["usuario"] = email 
                        session["nivel"] = "estudiante"
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
        
if  __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)