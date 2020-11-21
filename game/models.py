from djongo import models


# Create your models here.
class GamePlay(models.Model):
    room_id = models.IntegerField(primary_key=True)
    players = models.JSONField()
    objects = models.DjongoManager()

    def __str__(self):
        return str(self.players)

