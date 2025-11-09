from django.db import models

# ---------------- CREDENCIALES ----------------
class Credenciales(models.Model):
    idcredenciales = models.AutoField(primary_key=True, db_column='idcredenciales')
    user = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'credenciales'

    def __str__(self):
        return self.user


# ---------------- TIPO EMPLEADO ----------------
class TipoEmpleado(models.Model):
    idtipoEmpleado = models.AutoField(primary_key=True, db_column='idtipoEmpleado')
    rol = models.CharField(max_length=45)

    class Meta:
        db_table = 'tipoEmpleado'

    def __str__(self):
        return self.rol


# ---------------- EMPLEADO ----------------
class Empleado(models.Model):
    idempleado = models.AutoField(primary_key=True, db_column='idempleado')
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.EmailField(blank=True)

    # Antes eran IntegerField; ahora son FK reales
    credenciales = models.OneToOneField(
        Credenciales,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='credenciales_idcredenciales',
        related_name='empleado',
    )
    tipoEmpleado = models.ForeignKey(
        TipoEmpleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='tipoEmpleado_idtipoEmpleado',
        related_name='empleados',
    )

    class Meta:
        db_table = 'empleado'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'.strip()


# ---------------- ALERTAS ----------------
class Alertas(models.Model):
    idalertas = models.AutoField(primary_key=True, db_column='idalertas')
    fecha = models.DateField()
    estado = models.CharField(max_length=45)

    class Meta:
        db_table = 'alertas'

    def __str__(self):
        return f'Alerta #{self.idalertas} - {self.estado}'


# ---------------- PRODUCTO ----------------
class Producto(models.Model):
    idproducto = models.AutoField(primary_key=True, db_column='idproducto')
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=400)
    precio = models.IntegerField()
    stock_actual = models.IntegerField()
    cantidad_minima = models.IntegerField()

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre


# ---------------- VENTA ----------------
class Venta(models.Model):
    idventa = models.AutoField(primary_key=True, db_column='idventa')
    fecha = models.DateField()
    total = models.IntegerField()

    # Antes: empleado_idempleado = IntegerField(...)
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='empleado_idempleado',
        related_name='ventas',
    )

    class Meta:
        db_table = 'venta'

    def __str__(self):
        return f'Venta #{self.idventa} - {self.fecha}'


# ---------------- MOVIMIENTO ----------------
class Movimiento(models.Model):
    idmovimiento = models.AutoField(primary_key=True, db_column='idmovimiento')
    descripcion = models.CharField(max_length=400)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=45)

    # Antes: producto_idproducto = IntegerField(...)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='producto_idproducto',
        related_name='movimientos',
    )

    class Meta:
        db_table = 'movimiento'

    def __str__(self):
        if self.producto:
            return f'Movimiento #{self.idmovimiento} - {self.tipo} ({self.producto.nombre})'
        return f'Movimiento #{self.idmovimiento} - {self.tipo}'


# ---------------- HISTORIAL ----------------
class Historial(models.Model):
    idhistorial = models.AutoField(primary_key=True, db_column='idhistorial')
    fecha = models.DateTimeField()

    # Antes eran IntegerField
    alerta = models.ForeignKey(
        Alertas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='alertas_idalertas',
        related_name='historiales',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='producto_idproducto',
        related_name='historiales',
    )

    class Meta:
        db_table = 'historial'

    def __str__(self):
        return f'Historial #{self.idhistorial}'


# ---------------- DETALLE VENTA ----------------
class DetalleVenta(models.Model):
    iddetalleVenta = models.AutoField(primary_key=True, db_column='iddetalleVenta')
    cantidad_producto = models.IntegerField()
    precio_unitario = models.IntegerField()
    subtotal = models.IntegerField()

    # Antes: IntegerField
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='producto_idproducto',
        related_name='detalles',
    )
    venta = models.ForeignKey(
        Venta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='venta_idventa',
        related_name='detalles'
    )

    class Meta:
        db_table = 'detalleventa'

    def __str__(self):
        return f'DetalleVenta #{self.iddetalleVenta}'
