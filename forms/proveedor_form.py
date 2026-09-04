from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ProveedorForm(FlaskForm):
    nombre = StringField(
        'Nombre del proveedor',
        validators=[DataRequired(message='El nombre es obligatorio'), Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')]
    )
    producto = StringField(
        'Producto que ofrece',
        validators=[DataRequired(message='El producto es obligatorio'), Length(min=3, max=100, message='El producto debe tener entre 3 y 100 caracteres')]
    )
    contacto = StringField(
        'Persona de contacto',
        validators=[DataRequired(message='El contacto es obligatorio'), Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')]
    )
    pais = SelectField(
        'País',
        choices=[
            ('', 'Selecciona...'),
            ('USA', 'USA'),
            ('Japon', 'Japon'),
            ('China', 'China'),
            ('Alemania', 'Alemania'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Selecciona un país')]
    )
    submit = SubmitField('Agregar Proveedor')