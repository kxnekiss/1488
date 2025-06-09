from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_login = models.BooleanField(default=True)
    failed_attempts = models.PositiveIntegerField(default=0, verbose_name='Неудачные попытки авторизации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Room(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер комнаты')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'{self.number} - {self.capacity} чел. ({"занята" if self.is_available else "свободна"})'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    date_from = models.DateField(verbose_name='Дата от')
    date_to = models.DateField(verbose_name='Дата до')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def nights_count(self):
        return (self.date_to - self.date_from).days

