from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Bet

@receiver(post_save, sender=Match)
def upload_score_bets(sender, instance, **kwargs):
    bets = Bet.objects.filter(match=instance)
    for bet in bets:
        bet.save()