# Generated by Django 2.2.15 on 2020-09-11 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_technicalservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashierShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated at')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='Время завершения работы')),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('cashier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кассир')),
            ],
            options={
                'get_latest_by': '-created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourierShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated at')),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_type', models.CharField(choices=[('vehicle', 'транспорт'), ('walk', 'пеший')], default='vehicle', max_length=255, verbose_name='Тип доставки')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Курьер')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Vehicle', verbose_name='Транспортное средство')),
                ('vehicle_accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_accepted_by', related_query_name='vehicle_accepted_by', to=settings.AUTH_USER_MODEL, verbose_name='Принял')),
                ('vehicle_given_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_given_by', related_query_name='vehicle_given_by', to=settings.AUTH_USER_MODEL, verbose_name='Выдал')),
            ],
            options={
                'get_latest_by': '-created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpensesType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('custom_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated at')),
                ('next_service_time', models.DateTimeField(blank=True, null=True)),
                ('mileage', models.IntegerField(blank=True, null=True, verbose_name='Пробег')),
                ('amount', models.IntegerField(default=0, verbose_name='Сумма за услугу')),
                ('service', models.ForeignKey(on_delete=django.db.models.fields.Empty, to='api.TechnicalService')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.fields.Empty, to='api.Vehicle')),
            ],
            options={
                'get_latest_by': '-created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DailyRansom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated at')),
                ('amount', models.IntegerField(verbose_name='Сумма выкупа')),
                ('cashier_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashier_cash', to='api.CashierShift', verbose_name='Рабочий день кассира')),
                ('courier_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier_day', to='api.CourierShift', verbose_name='Рабочий день курьера')),
            ],
            options={
                'get_latest_by': '-created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourierShiftExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated at')),
                ('bill_photo', models.ImageField(blank=True, null=True, upload_to='bills', verbose_name='Фото чека')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Сумма к оплате')),
                ('courier_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='couriers_expenses', related_query_name='courier_expenses', to='api.CourierShift', verbose_name='Смена курьера')),
                ('expenses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ExpensesType', verbose_name='Оплата за')),
            ],
            options={
                'get_latest_by': '-created_at',
                'abstract': False,
            },
        ),
    ]
