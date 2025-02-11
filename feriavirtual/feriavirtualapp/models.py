from email.policy import default
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import fields
from django.db.models.fields import related
from django.utils import timezone
PRODUCTOS =(
    ("1", "Cerezas "),
    ("2", "Uvas"),
    ("3", "Arándanos "),
    ("4", "Nueces"),
    ("5", "Manzana"),
    ("6", "Ciruela"),
    ("7", "Peras"),
    ("9", "Durazno"),
    ("11", "Frutilla"),
    ("12", "Granada"),
    ("13", "Limón"),
    ("14", "Mandarina"),
    ("15", "Naranja"),
    ("16", "Sandia "),
    ("17", "Melón"),
    ("18", "Mora"),
    ("19", "Pera"),
    ("20", "Manzana"),
    )
#ATENDIENDO TAMAÑO Y CALIBRE LA FRUTA SE PUEDE CALIFICAR EN:
CALIBRE =(
    ("1", "Segunda"),
    ("2", "Primera"),
    ("3", "Extra "),
)
TAMAÑO =(
    ("1", "Ligero "),
    ("2", "Liviano"),
    ("3", "Semi Liviano"),
    ("4", "Mediano"),
    ("5", "Semi esado"),
    ("6", "Pesado"),
    ("7", "Extra Pesado"),
    ("8", "Mega Pesado"),
    ("9", "Ultra Pesado"),
    ("10", "Extra Pesado"),
    ("11", "Giga Pesado"),
    ("12", "Super Pesado"),
    )
EstadoSolicitudCompra =(
    ("1", "Aprobado"),
    ("2", "Rechazado"),
    ("3", "Pendiente"),
    ("4", "Subasta de transporte"),
    ("5", "Transporte Listo"),
    ("6","Entregado en bodega"),
    ("7","Viaje interrumpido (productor)"),
    ("8", "Revision de calidad"),
    ("9", "Rechazado en revision"),
    ("10", "Revisado"),
    ("11", "En camino"),
    ("12", "Viaje interrumpido (transportista)"),
    ("13", "Destino"),
    ("14", "Aceptado por el destinatario"),
    ("15", "Rechazado por el destinatario"),
    ("16", "Saldo"),
    ("17", "Completado")


    
    )
class User(AbstractUser):
    ROLES =(
    ("1", "Productor"),
    ("2", "Cliente externo"),
    ("3", "Cliente interno"),
    ("4", "Transportista"),
    ("5", "Consultor"),
    ("6", "Administrador"),
    ("7", "Revisor de calidad"),
    )
    dni = models.CharField(max_length=30,null=True)
    rol = models.CharField(max_length=50, choices = ROLES, null=True)
    imagen = models.ImageField(upload_to="Perfil",default='Perfil/default.png')
    direccion=models.CharField(max_length=50, null=True)
    codigopostal=models.IntegerField(default=0, null=True)
    def __str__(self):
        return f'{self.username}'
    



class Producto(models.Model):
    
    autor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='producto')
    producto = models.CharField(max_length=50, choices = PRODUCTOS, null=True)
    variedad = models.CharField(max_length=50, null=True)
    calibre = models.CharField(max_length=50,choices = CALIBRE, null=True)
    cantidad = models.IntegerField(default=0)
    fecha_subida = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="Productos", null=True)
    precio = models.IntegerField(default=0)
    Saldo= models.BooleanField(default=False)
    def __str__(self):
        return f'{self.autor.username}: {self.producto}: { self.variedad} :  { self.calibre} : { self.cantidad}: { self.fecha_subida}: { self.imagen}: { self.precio}'


class Contrato(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_termino = models.DateField(default=timezone.now)
    vigencia = models.BooleanField(default=False)

class Transporte(models.Model):
    transportista = models.ForeignKey(User, on_delete=models.CASCADE)
    tamaño = models.CharField(max_length=50, choices = TAMAÑO, null=True)
    refrigeracion = models.BooleanField(default=False)
    tarifa = models.IntegerField(default=0)
    disponible= models.BooleanField(default=True)
    def __str__(self):
        return f'{self.transportista.username}: tamaño: {self.tamaño}: Refrigeracion: {self.refrigeracion}: Tarifa: {self.tarifa}'

    

class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.CharField(max_length=50, choices = PRODUCTOS, null=True)
    productor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="productor" ,null=True)
    variedad = models.CharField(max_length=50, null=True)
    calibre = models.CharField(max_length=50, choices = CALIBRE, null=True,default=1)
    cantidad_actual = models.IntegerField(default=0)
    cantidad_necesaria = models.IntegerField(default=0)
    contenido = models.CharField(max_length=50, null=True)
    refrigeracion = models.BooleanField(default=False)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ClienteSoli')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="Posts", null=True)
    EstadoSolicitud = models.CharField(max_length=50, null=True, choices=EstadoSolicitudCompra, default='3')
    transportista = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="transportista")
    transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE, null=True,related_name="transporte")
    comentariosTransportista = models.TextField(default="")
    class Meta:
        ordering = ['-fecha_creacion']
    def publish(self):
        self.fecha_publicacion = timezone.now()
        self.save()

class Posthistorico(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    idpost= models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    producto = models.CharField(max_length=50, choices = PRODUCTOS, null=True)
    productor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="productorh" ,null=True)
    variedad = models.CharField(max_length=50, null=True)
    calibre = models.CharField(max_length=50, choices = CALIBRE, null=True,default=1)
    cantidad_actual = models.IntegerField(default=0,null=True)
    cantidad_necesaria = models.IntegerField(default=0,null=True)
    contenido = models.CharField(max_length=50, null=True)
    refrigeracion = models.BooleanField(default=False,null=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ClienteSolih',null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now,null=True)
    fecha_modificacion = models.DateTimeField(null=True)
    imagen = models.ImageField(upload_to="Posts", null=True)
    EstadoSolicitud = models.CharField(max_length=50, null=True, choices=EstadoSolicitudCompra, default='3')
    transportista = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="transportistah")
    transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE, null=True,related_name="transporteh")
    comentariosTransportista = models.TextField(default="",null=True)   
