from django.db import models

# Create your models here.

class Credenciales(models.Model):
    idcredenciales = models.AutoField(primary_key=True, db_column='idcredenciales')
    user = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'credenciales'   # coincide con tu diagrama

    def __str__(self):
        return self.user


class Movimiento(models.Model):
    idmovimiento = models.AutoField(primary_key=True, db_column='idmovimiento')
    descripcion = models.CharField(max_length=400)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=45)

    # SIN FK → solo guardamos el ID del producto
    producto_idproducto = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'movimiento'

    def __str__(self):
        return f'Movimiento #{self.idmovimiento} - {self.tipo}'


class Historial(models.Model):
    idhistorial = models.AutoField(primary_key=True, db_column='idhistorial')
    fecha = models.DateTimeField()

    # SIN FK → solo IDs
    alertas_idalertas = models.IntegerField(null=True, blank=True)
    producto_idproducto = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'historial'

    def __str__(self):
        return f'Historial #{self.idhistorial}'