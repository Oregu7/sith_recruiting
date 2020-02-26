from django.db import models


class Sith(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    planet = models.ForeignKey('basic.Planet', on_delete=models.CASCADE, verbose_name="Планета")

    def __str__(self):
        return super().name

    class Meta:
        verbose_name = "Ситха"
        verbose_name_plural = "Ситхи"


class ShadowHand(models.Model):
    recruit = models.ForeignKey('recruit.Recruit', on_delete=models.CASCADE)
    sith_master = models.ForeignKey(Sith, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)