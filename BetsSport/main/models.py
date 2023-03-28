from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sport(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='sport')

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='sport')
    
    def __str__(self):
        return f'{self.name} - {self.sport.name} - {self.sport.country.name}'


class Match(models.Model):
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_home')
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_away')
    date = models.DateField()
    result_home = models.PositiveIntegerField(null=True, blank=True)
    result_away = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.team_home.name} vs. {self.team_away.name} ({self.date})'


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    result_home = models.PositiveIntegerField()
    result_away = models.PositiveIntegerField()
    score_of_bet = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} apuesta {self.result_home} - {self.result_away} en {self.match}'

    def get_score(self):
        if self.match.result_home is None or self.match.result_away is None:
            return 0
        if self.result_home == self.match.result_home and self.result_away == self.match.result_away:
            return 3
        elif (self.result_home > self.result_away and self.match.result_home > self.match.result_away) or \
           (self.result_home < self.result_away and self.match.result_home < self.match.result_away) or \
           (self.result_home == self.result_away and self.match.result_home == self.match.result_away):
            return 1
        return 0

    def save(self, *args, **kwargs):
        self.score_of_bet = self.get_score()
        super(Bet, self).save(*args, **kwargs)