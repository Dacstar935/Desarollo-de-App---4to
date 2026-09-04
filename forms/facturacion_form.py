from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class FacturacionForm(FlaskForm):
    cliente = StringField(
        'Cliente',
        validators=[DataRequired(message='El cliente es obligatorio'), Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')]
    )
    producto = StringField(
        'Producto',
        validators=[DataRequired(message='El producto es obligatorio'), Length(min=3, max=100, message='El producto debe tener entre 3 y 100 caracteres')]
    )
    cantidad = IntegerField(
        'Cantidad',
        validators=[DataRequired(message='La cantidad es obligatoria'), NumberRange(min=1, message='La cantidad debe ser mayor a 0')]
    )
    total = FloatField(
        'Total',
        validators=[DataRequired(message='El total es obligatorio'), NumberRange(min=0.01, message='El total debe ser mayor a 0')]
    )
    estado = SelectField(
        'Estado',
        choices=[
            ('', 'Selecciona...'),
            ('Pagado', 'Pagado'),
            ('Pendiente', 'Pendiente'),
            ('Cancelado', 'Cancelado')
        ],
        validators=[DataRequired(message='Selecciona un estado')]
    )
    submit = SubmitField('Agregar Factura')