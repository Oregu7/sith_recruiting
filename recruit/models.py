from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.crypto import get_random_string
from basic.helpers import simple_paginator


class Recruit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    planet = models.ForeignKey('basic.Planet', on_delete=models.CASCADE, verbose_name="Планета")
    age = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(10), MaxValueValidator(999)], verbose_name="Возраст")
    email = models.EmailField(verbose_name="Почта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рекрут"
        verbose_name_plural = "Рекруты"

class ShadowHandTest(models.Model):
    order_code = models.CharField(max_length=30, unique=True, verbose_name="Код ордена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.order_code

    @classmethod
    def get_random(cls):
        return cls.objects.order_by('?').first()

    class Meta:
        verbose_name = "Тестовое испытание для руки тени"
        verbose_name_plural = "Тестовые испытания для руки тени"

class ShadowHandQuestion(models.Model):
    description = models.TextField(verbose_name="Вопрос")
    test = models.ForeignKey(ShadowHandTest, on_delete=models.CASCADE)

    def __str__(self):
        return f"Вопрос #{self.id}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы" 

class ShadowHandSession(models.Model):
    test = models.ForeignKey(ShadowHandTest, on_delete=models.CASCADE)
    recruit = models.OneToOneField(Recruit, on_delete=models.CASCADE)
    token = models.CharField(max_length=42, unique=True)
    done = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, test: ShadowHandTest, recruit: Recruit):
        token = get_random_string(42)
        session = cls(test=test, recruit=recruit, token=token)
        session.save()
        return session

    @classmethod
    def pagination_actual(cls, page: int = 1, limit: int = 10):
        object_list = cls.objects.filter(done=True, success=False).order_by('recruit__name').distinct()
        session_list = simple_paginator(object_list, page=page, limit=limit)
        return session_list

class ShadowHandAnswer(models.Model):
    session = models.ForeignKey(ShadowHandSession, on_delete=models.CASCADE)
    question = models.ForeignKey(ShadowHandQuestion, on_delete=models.CASCADE)
    answer = models.BooleanField()