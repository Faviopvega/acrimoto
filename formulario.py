from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, Form, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length

class formLogin(FlaskForm):
    email = EmailField("Correo electronico", validators=[DataRequired(message='Campo Requerido *')])
    password = PasswordField("Password", validators=[DataRequired(message='Campo Requerido *'), Length(min=3, max=20, message="La contraseña requiere entre %(min)d y %(max)d caracteres")])
    enviar = SubmitField("Iniciar Sesión")

#CLASES
class formUsuarios(Form):
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    direccion = StringField('Direccion', validators=[DataRequired()])
    telefono = StringField('Numero Telefonico', validators=[DataRequired()])
    correo = EmailField("Correo electronico", validators=[DataRequired()])
    contrasenia = StringField('Contraseña', validators=[DataRequired()])
    tipoUsuario = SelectField("Tipo Usuario ", validators=[DataRequired()])
    registrar = SubmitField("Registrar Usuario")

