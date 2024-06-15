from django.db import models
from django.contrib.auth.models import AbstractUser

class CentroMedico(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Especialista(models.Model):
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    # Agrega campos adicionales si es necesario
    TIPO_USUARIO_CHOICES = [
        ('paciente', 'Paciente'),
        ('admin', 'Administrador'),
        # Añade otros tipos de usuario según sea necesario
    ]
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return self.email

class Agenda(models.Model):
    fecha_disponible = models.DateField()
    hora_disponible = models.TimeField()
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    centro_medico = models.ForeignKey(CentroMedico, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha_disponible} {self.hora_disponible} - {self.especialista.nombre} - {self.centro_medico.nombre}"

class Cita(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cita con {self.usuario.email} en {self.agenda.fecha_disponible} {self.agenda.hora_disponible}"
