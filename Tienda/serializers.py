from rest_framework import serializers
from .models import (
    Credenciales, TipoEmpleado, Empleado, Alertas, 
    Producto, Venta, Movimiento, Historial, DetalleVenta
)

class CredencialesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credenciales
        fields = '__all__'

class TipoEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEmpleado
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    # Nested serializers for read-only details
    tipo_empleado_nombre = serializers.ReadOnlyField(source='tipoEmpleado.rol')
    
    class Meta:
        model = Empleado
        fields = '__all__'

class AlertasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alertas
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = Movimiento
        fields = '__all__'

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = '__all__'
