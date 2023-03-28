from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Bet

@receiver(post_save, sender=Match)
def actualizar_puntajes_apuestas(sender, instance, **kwargs):
    bets = Bet.objects.filter(partido=instance)
    for bet in bets:
        bet.save()