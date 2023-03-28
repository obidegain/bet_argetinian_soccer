from django.contrib import admin
from .models import Sport, Country, Team, Match, Bet

admin.site.register(Sport)
admin.site.register(Country)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Bet)
