from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductoForm(FlaskForm):
    nombre = StringField(
        'Nombre del producto',
        validators=[DataRequired(message='El nombre es obligatorio'), Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')]
    )
    categoria = SelectField(
        'Categoría',
        choices=[
            ('', 'Selecciona...'),
            ('Procesador', 'Procesador'),
            ('Tarjeta Grafica', 'Tarjeta Grafica'),
            ('Memoria RAM', 'Memoria RAM'),
            ('Disco Duro', 'Disco Duro'),
            ('Fuente de Poder', 'Fuente de Poder'),
            ('Monitor', 'Monitor'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Selecciona una categoría')]
    )
    precio = FloatField(
        'Precio',
        validators=[DataRequired(message='El precio es obligatorio'), NumberRange(min=0.01, message='El precio debe ser mayor a 0')]
    )
    stock = IntegerField(
        'Stock',
        validators=[DataRequired(message='El stock es obligatorio'), NumberRange(min=0, message='El stock no puede ser negativo')]
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Optional(), Length(max=500, message='La descripción no puede exceder 500 caracteres')]
    )
    submit = SubmitField('Agregar Producto')