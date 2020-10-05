import datetime

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Subquery, OuterRef

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from utils import SQCount, ArraySubquery, StringArraySubquery
from .models import *
from django.utils.translation import ugettext as _


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'phone_number', 'email', 'is_active', 'is_staff')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'phone_number', 'email', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'is_active', 'is_staff')
    search_fields = ('username',)
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2'),
        }),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):

     list_display = (
         'name',
     )
     list_filter = (
         'name',
     )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'street',
         'house',
         'flat',
         'floor',
         'district',
         'city',
     )
     list_filter = (
         'street',
         'district',
         'city',
     )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'vin_code',
        'type',
        'gov_number',
        'is_active',
    )
    list_filter = (
        'type',
        'is_active',
    )
    search_fields = (
        'number',
        'vin_code',
        'type',
        'gov_number',
    )


@admin.register(TechnicalService)
class TechnicalServiceAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'name',
        'custom_name',
    )
    list_filter = (
        'name',
        'custom_name',
    )


@admin.register(VehicleService)
class VehicleServiceAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'vehicle',
        'next_service_time',
        'mileage',
    )
    list_filter = (
        'service',
        'vehicle',
        'next_service_time',
        'mileage',
    )


@admin.register(CourierShift)
class CourierShiftAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'courier',
        'start_time',
        'end_time',
        'created_at',
        'updated_at',
        'amount',
        'delivery_type',
        'expenses',
        'vehicle',
        'vehicle_given_by',
        'vehicle_accepted_by',
    )

    def expenses(self, obj):
        if obj.daily_courier_expenses:
            return sum(obj.daily_courier_expenses)
        return 0

    expenses.short_description = _('Траты за день')

    def is_active(self, obj):
        return obj.is_active

    is_active.short_description = _('Доступность')
    is_active.boolean = True

    def amount(self, obj):
        return obj.amount or None

    amount.short_description = _('сумма выкупа')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.with_is_active().annotate(
            amount=Subquery(
                DailyRansom.objects.filter(
                    courier_shift_id=OuterRef('id'),
                ).values('amount')[:1]
            ),
            daily_courier_expenses=StringArraySubquery(
                CourierShiftExpenses.objects.filter(
                    courier_shift_id=OuterRef('id')
                ).values('amount')
            )
        )
        return queryset


@admin.register(CashierShift)
class CashierShiftAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'updated_at',
        'cashier',
        'end_time',
    )


@admin.register(DailyRansom)
class DailyRansomAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'cashier_shift',
        'courier_shift',
        'amount',
    )

    def created(self, obj):
        return obj.created_at

    created.short_description = _('Дата создания')


@admin.register(ExpensesType)
class ExpensesTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'custom_name',
    )
    list_filter = (
        'name',
        'custom_name',
    )


@admin.register(CourierShiftExpenses)
class CourierShiftExpensesAdmin(admin.ModelAdmin):
    list_display = (
        'courier',
        'expenses',
        'amount',
        'created_at',
    )
    list_filter = (
        'expenses',
    )
    search_fields = (
        'expenses',
        'amount',
    )

    def courier(self, obj):
        return '\n'.join(courier.courier.username for courier in obj.courier_day.all())


@admin.register(OperatorShift)
class OperatorShiftAdmin(admin.ModelAdmin):
    fields = (
        'id',
        'operator',
        'start_time',
        'end_time',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'courier_shift',
        'status',
        'accepted_time',
        'start_time',
        'end_time',
        'delivery_time',
        'created_by',
        'reciever_name',
        'customer',
        'info',
        'ransom_sum',
        'delivery_from',
        'delivery_to',
        'wait_time',
        'delivery_cost',
    )


@admin.register(Fines)
class FinesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'custom_name',
        'description',
    )


@admin.register(UserFines)
class UserFinesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount',
        'fines',
    )
