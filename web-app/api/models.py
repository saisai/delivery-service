from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Case, When, BooleanField, QuerySet, Value
from django.utils.translation import ugettext as _
import api.permission_constants as permission_constants
from django.contrib.postgres.fields import JSONField
from safedelete.models import SafeDeleteModel, SOFT_DELETE

ORDER_STATUS_NEW = 'new'
ORDER_STATUS_ACCEPTED = 'accepted'
ORDER_STATUS_CANCELED = 'canceled'
ORDER_STATUS_DONE = 'done'
ORDER_STATUS_IN_PROGRESS = 'in_progress'

MOTO_TYPE = 'moto'
CAR_TYPE = 'car'
VEHICLE_TYPE = 'vehicle'
WALK_TYPE = 'walk'

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS_NEW, 'Новый'),
    (ORDER_STATUS_ACCEPTED, 'Принят'),
    (ORDER_STATUS_CANCELED, 'Отменен'),
    (ORDER_STATUS_DONE, 'Завершен'),
    (ORDER_STATUS_IN_PROGRESS, 'Выполняется'),
)

VEHICLE_TYPE_CHOICES = (
    (MOTO_TYPE, 'мото'),
    (CAR_TYPE, 'авто'),
)

COURIER_DELIVERY_TYPE_CHOICES = (
    (VEHICLE_TYPE, 'транспорт'),
    (WALK_TYPE, 'пеший'),
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email,
                     password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone_number,
                    email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password,
                                 **extra_fields)

    def create_superuser(self, username, email, password,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password,
                                 **extra_fields)


class User(AbstractUser):
    phone_number = models.CharField(max_length=9, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    passport = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Пасспортные данные'))

    objects = UserManager()
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        permissions = (
            *permission_constants.ProfilePermissions.CHOICES,
        )


class TitleDescriptionModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True)

    def get_name(self):
        pass

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        get_latest_by = '-created_at'


class City(TitleDescriptionModel):
    name = models.CharField(verbose_name=_('Город'), max_length=255)

    def __str__(self):
        return f"Город {self.name}"


class District(TitleDescriptionModel):

    def __str__(self):
        return f"Район {self.name}"


class Street(TitleDescriptionModel):

    def __str__(self):
        return f"ул. {self.name}"


class Address(TitleDescriptionModel):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='addresses',
        related_query_name='address',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='addresses',
        related_query_name='address'
    )
    street = models.ForeignKey(
        Street,
        verbose_name=_('Улица'),
        max_length=255,
        on_delete=models.Empty,
        related_name='addresses',
        related_query_name='address',
    )
    house = models.CharField(verbose_name=_('Дом'), max_length=255)
    flat = models.IntegerField(verbose_name=_('квартира'), blank=True, null=True)
    floor = models.IntegerField(verbose_name=_('Этаж'), blank=True, null=True)
    enter_key = JSONField(
        verbose_name=_('Enter keys'),
        default=dict,
        null=True,
        blank=True,
    )

    def get_address_with_flat(self):
        return f'дом {self.house} квартира {self.flat}'

    def get_address_without_flat(self):
        return f'дом {self.house}'

    def get_full_house_address(self):
        if self.flat:
            return self.get_address_with_flat()
        return self.get_address_without_flat()

    def get_full_city_address(self):
        return f'Город {self.city.name}, район {self.district.name}, {self.street}'

    def get_full_address(self):
        return f'{self.get_full_city_address()}, {self.get_full_house_address()}'

    def get_enter_keys(self):
        return self.enter_key

    def __str__(self):
        return f'{self.street}'


# Vehicle


class Vehicle(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    type = models.CharField(choices=VEHICLE_TYPE_CHOICES, max_length=50)
    vin_code = models.CharField(unique=True, max_length=100)
    gov_number = models.CharField(unique=True, max_length=20)
    number = models.IntegerField(blank=True, null=True, verbose_name='vehicle number')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ТС номер {self.number} тип {self.type}"


class TechnicalService(TitleDescriptionModel):
    address = models.ForeignKey(
        Address,
        verbose_name=_('Адрес СТО'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='tech_services',
        related_query_name='tech_service',
    )

    def __str__(self):
        return f'Сервис {self.name}'


class VehicleService(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    service = models.ForeignKey(
        TechnicalService,
        on_delete=models.Empty,
        related_name='vehicle_services',
        related_query_name='vehicle_service',
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.Empty,
        related_name='vehicle_service',
        related_query_name='vehicle_service',
    )
    next_service_time = models.DateTimeField(blank=True, null=True)
    mileage = models.IntegerField(verbose_name=_('Пробег'), blank=True, null=True)
    amount = models.IntegerField(verbose_name=_('Сумма за услугу'), default=0)

    def __str__(self):
        return f'{self.service.name} {self.vehicle.gov_number}'


# Courier Day Schedule


class CourierShiftManager(QuerySet):
    def with_is_active(self):
        """
        Annotates is_active flag to queryset according to bounds of
        start_date and end_date.
        """
        return self.annotate(
            is_active=Case(
                When(
                    end_time__isnull=True,
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )


class CourierShift(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    courier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Курьер'),
        on_delete=models.CASCADE,
        related_name='courier_shifts',
        related_query_name='courier_shift',
    )
    end_time = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
    )
    start_time = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
    )
    delivery_type = models.CharField(
        verbose_name=_('Тип доставки'),
        choices=COURIER_DELIVERY_TYPE_CHOICES,
        default=VEHICLE_TYPE,
        max_length=255,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        verbose_name=_('Транспортное средство'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='courier_shifts',
        related_query_name='courier_shift',
    )
    vehicle_given_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Выдал'),
        on_delete=models.CASCADE,
        related_name='vehicle_given_bys',
        related_query_name='vehicle_given_by',
        blank=True,
        null=True,
    )
    vehicle_accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Принял'),
        on_delete=models.CASCADE,
        related_name='vehicle_accepted_bys',
        related_query_name='vehicle_accepted_by',
        blank=True,
        null=True,
    )

    objects = CourierShiftManager.as_manager()

    def __str__(self):
        return f'Курьер - {self.pk}'


class ExpensesType(TitleDescriptionModel):
    def __str__(self):
        return self.name


class CourierShiftExpenses(TimeStampedModel):
    expenses = models.ForeignKey(
        ExpensesType,
        verbose_name=_('Оплата за'),
        on_delete=models.CASCADE
    )
    courier_shift = models.ForeignKey(
        CourierShift,
        verbose_name=_('Смена курьера'),
        related_name='courier_shift_expenses',
        related_query_name='courier_shift_expenses',
        on_delete=models.CASCADE,
    )
    bill_photo = models.ImageField(
        verbose_name=_('Фото чека'),
        upload_to='bills',
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        verbose_name=_('Сумма к оплате'),
        decimal_places=2,
        max_digits=8
    )

    def __str__(self):
        return f'{self.amount}'


# Cashier Day Schedule

class CashierShift(TimeStampedModel, SafeDeleteModel):
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Кассир'), on_delete=models.CASCADE)
    end_time = models.DateTimeField(auto_now_add=False, blank=True, null=True,
                                    verbose_name=_('Время завершения работы'))
    start_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'Кассир {self.cashier}'


class DailyRansom(TimeStampedModel, SafeDeleteModel):
    cashier_shift = models.ForeignKey(
        CashierShift,
        on_delete=models.CASCADE,
        verbose_name=_('Рабочий день кассира'),
        related_name='cashier_cash',
    )
    courier_shift = models.ForeignKey(
        CourierShift,
        on_delete=models.CASCADE,
        verbose_name=_('Рабочий день курьера'),
        related_name='courier_day',
    )
    amount = models.IntegerField(verbose_name=_('Сумма выкупа'), )

    def __str__(self):
        return f'Сумма выкупа - {self.amount}, кассир - {self.cashier_shift}'


class Fines(TitleDescriptionModel):
    description = models.TextField(
        verbose_name=_('Описание'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class UserFines(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    amount = models.IntegerField(
        verbose_name=_('Сумма штрафа'),
        default=0,
    )
    fines = models.ForeignKey(
        Fines,
        on_delete=models.PROTECT,
        verbose_name=_('Штрафы пользователя'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'Сумма штрафа {self.amount} пользователь {self.user}'


class OperatorShift(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='operator_shifts',
        related_query_name='operator_shift',
        on_delete=models.CASCADE,
        verbose_name=_('Оператор')
    )

    start_time = models.TimeField(
        auto_now_add=False,
        verbose_name=_('Начало смены'),
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        auto_now_add=False,
        verbose_name=_('Конец смены'),
        blank=True,
        null=True,
    )


class Order(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    courier_shift = models.ForeignKey(
        CourierShift,
        verbose_name=_('Смена курьера'),
        related_name='courier_orders',
        related_query_name='courier_order',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name=_('Статус заказа'),
        choices=ORDER_STATUS_CHOICES,
        max_length=100,
        default=ORDER_STATUS_NEW,
    )
    accepted_time = models.DateTimeField(
        verbose_name=_('Время подтверждения заказа'),
        auto_now_add=False,
        blank=True,
        null=True,
    )
    start_time = models.DateTimeField(
        verbose_name=_('Время начала выполнения заказа'),
        auto_now_add=False,
        blank=True,
        null=True,
    )
    end_time = models.DateTimeField(
        verbose_name=_('Время завершения заказа'),
        auto_now_add=False,
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Кем создан'),
        on_delete=models.CASCADE,
        related_name='orders_created_by',
        related_query_name='order_created_by',
    )
    reciever_name = models.CharField(
        max_length=255,
        verbose_name=_('Имя получателя'),
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Клиент'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='customers_orders',
        related_query_name='customer_order',
    )
    info = models.TextField(
        verbose_name=_('Дополнительные сведения'),
        blank=True,
        null=True,
    )
    ransom_sum = models.DecimalField(
        verbose_name=_('Сумма выкупа'),
        max_digits=6,
        decimal_places=2,
    )
    delivery_from = models.ForeignKey(
        Address,
        verbose_name=_('Забрать от'),
        on_delete=models.CASCADE,
        related_name='address_delivery_from',
        related_query_name='address_from',
        blank=True,
        null=True,
    )
    delivery_to = models.ForeignKey(
        Address,
        verbose_name=_('Куда доставить'),
        on_delete=models.CASCADE,
        related_name='address_delivery_to',
        related_query_name='address_to',
        blank=True,
        null=True,
    )
    wait_time = models.TimeField(
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name=_('Время ожидания')
    )
    delivery_cost = models.IntegerField(
        verbose_name=_('Стоимость даставки'),
        blank=True,
        null=True,
    )
    delivery_time = models.TimeField(
        verbose_name=_('Время выполнения заказа'),
        blank=True,
        null=True,
        auto_now_add=False,
    )
