from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

class ClienteForm(FlaskForm):
    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio'), Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')]
    )
    email = EmailField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio'), Email(message='Ingresa un correo válido')]
    )
    telefono = TelField(
        'Teléfono',
        validators=[DataRequired(message='El teléfono es obligatorio'), Length(min=7, max=15, message='Ingresa un número válido')]
    )
    ciudad = SelectField(
        'Ciudad',
        choices=[
            ('', 'Selecciona...'),
            ('Quito', 'Quito'),
            ('Guayaquil', 'Guayaquil'),
            ('Cuenca', 'Cuenca'),
            ('Ambato', 'Ambato'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Selecciona una ciudad')]
    )
    submit = SubmitField('Agregar Cliente')