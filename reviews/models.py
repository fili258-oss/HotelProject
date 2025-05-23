from django.db import models
from django.utils import timezone

class Reseña(models.Model):
    reseña_id = models.AutoField(primary_key=True)
    reserva = models.ForeignKey('reservations.Reserva', on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    fecha_reseña = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = 'reseñas'

    def __str__(self):
        return f"Reseña {self.reseña_id} - Reserva {self.reserva.reserva_id}"
    
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Reseña)
def actualizar_puntuacion_media_hotel(sender, instance, **kwargs):
    hotel = instance.reserva.habitacion.hotel
    puntuacion_media = Reseña.objects.filter(
        reserva__habitacion__hotel=hotel,
        visible=True
    ).aggregate(media=Avg('puntuacion'))['media'] or 0
    # Opcional: Guardar puntuacion_media en el modelo Hotel si se añade un campo
    # hotel.puntuacion_media = puntuacion_media
    # hotel.save()