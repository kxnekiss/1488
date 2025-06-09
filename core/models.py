from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    first_login = models.BooleanField(default=True, verbose_name='Первый вход')
    failed_attempts = models.PositiveIntegerField(default=0, verbose_name='Неудачные попытки авторизации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Client(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО клиента')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Car(models.Model):
    license_plate = models.CharField(max_length=20, unique=True, verbose_name='Гос. номер')
    brand = models.CharField(max_length=255, verbose_name='Марка')
    capacity_kg = models.PositiveIntegerField(default=1000, verbose_name='Грузоподъёмность (кг)')

    def __str__(self):
        return f"{self.license_plate} ({self.brand})"

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автопарк'


class Route(models.Model):
    origin = models.CharField(max_length=255, verbose_name='Пункт отправления')
    destination = models.CharField(max_length=255, verbose_name='Пункт назначения')

    def __str__(self):
        return f"{self.origin} → {self.destination}"

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    delivery_date = models.DateField(default=now, verbose_name='Дата доставки')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, verbose_name='Автомобиль')

    def __str__(self):
        return f"Заказ #{self.id} - {self.client}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    payment_date = models.DateField(default=now, verbose_name='Дата оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')

    def __str__(self):
        return f"Оплата #{self.id} - {self.amount}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    weight_kg = models.PositiveIntegerField(verbose_name='Вес груза (кг)')

    def __str__(self):
        return f"Доставка #{self.id} - {self.weight_kg} кг"

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'