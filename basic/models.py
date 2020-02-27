from django.db import models

# Create your models here.
class Planet(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование", unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Планету"
        verbose_name_plural = "Планеты"