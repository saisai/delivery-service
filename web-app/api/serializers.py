import datetime

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils import TimeZoneProvider
from .models import *
from rest_framework import serializers

from .permission_constants import PERMISSIONS_MAP


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class AuthUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    is_staff = serializers.BooleanField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
        )


class UserSelfSerializer(UserSerializer):
    permissions = serializers.SerializerMethodField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)

    @staticmethod
    def get_permissions(obj):
        permissions = list()

        for permission_code, permission_name in PERMISSIONS_MAP.items():
            if obj.has_perm(permission_code):
                permissions.append(permission_name)

        return permissions

    class Meta:
        model = User
        fields = (*UserSerializer.Meta.fields, 'permissions')


class CourierShiftSerializer(serializers.Serializer):
    start_time = serializers.DateField(required=False, default=datetime.datetime.now().date())

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'start_time': instance.start_time,
            'courier_id': int(instance.courier_id),
            'courier_name': instance.courier.first_name,
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        time_zone_provider = TimeZoneProvider()

        today = time_zone_provider.get_date_according_to_timezone()

        start_time = attrs['start_time']

        user_id = self.context.get('pk')
        courier_day = CourierShift.objects.filter(
            courier_id=user_id,
            end_time__isnull=True,
        ).first()
        if courier_day:
            raise serializers.ValidationError("Courier have not finished the previous day")
        if not start_time:
            raise serializers.ValidationError(
                'start_time field is required'
            )
        if start_time != today.date():
            raise serializers.ValidationError(
                'start-time must be equal today date'
            )
        return attrs

    def create(self, validated_data):
        user_id = self.context.get('pk')
        courier_daily_task = CourierShift.objects.create(
            courier_id=user_id,
            start_time=validated_data.get('start_time'),
        )
        return courier_daily_task


class AssignVehicleSerializer(serializers.ModelSerializer):
    vehicle = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'vehicle': instance.vehicle.id,
            'vehicle_given_by': instance.vehicle_given_by.id,
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        vehicle = attrs.get('vehicle')
        if not vehicle:
            raise serializers.ValidationError('vehicle field is required')

        return attrs

    def update(self, instance, validated_data):
        instance.vehicle_id = validated_data.get('vehicle')
        instance.vehicle_given_by_id = self.context.get('request_user_id')
        instance.save()
        return instance

    def create(self, validated_data):
        instance = CourierShift.objects.get(id=self.context.get('pk'))
        return self.update(instance, validated_data)

    class Meta:
        model = CourierShift
        fields = (
            'id',
            'vehicle',
            'vehicle_given_by',
        )


class TakeVehicleSerializer(AssignVehicleSerializer):
    def create(self, validated_data):
        instance = CourierShift.objects.get(id=self.context.get('pk'))
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.vehicle_id = validated_data.get('vehicle')
        instance.vehicle_accepted_by_id = self.context.get('request_user_id')
        instance.save()
        return instance


class UpdateDailyCourierSerializer(serializers.Serializer):
    end_time = serializers.DateField(required=False, format="%Y-%m-%d %H:%M:%S")
    start_time = serializers.DateField(required=False, format="%Y-%m-%d %H:%M:%S")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today = datetime.datetime.now().date()
        self.pk = self.context.get('pk')

    def to_representation(self, instance):
        return {
            'id': self.instance.id,
            'start_time': self.instance.start_time,
            'end_time': self.instance.end_time if self.instance.end_time else None,
            'delivery_type': self.instance.delivery_type,
            'courier_id': self.instance.courier_id,
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        today = datetime.datetime.now().date()
        end_time = attrs.get('end_time')
        courier_day = CourierShift.objects.filter(id=self.pk, end_time__isnull=True).first()
        if not courier_day:
            raise serializers.ValidationError('The courier working day does not exist, nothing to update')
        if end_time and end_time != self.today:
            raise serializers.ValidationError('end_date field must be equal today date')
        return attrs

    def update(self, validated_data, pk):
        instance = CourierShift.objects.filter(courier_id=pk, end_time__isnull=True)
        instance_id = instance.first().id
        instance.update(**validated_data)
        updated_instance = CourierShift.objects.get(id=instance_id)
        return updated_instance

    def create(self, validated_data):
        pk = self.context.get('pk')
        return self.update(validated_data, pk)


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'phone_number',
        )


class CouriersShiftSerializer(serializers.ModelSerializer):
    courier = serializers.IntegerField(required=False)
    end_time = serializers.IntegerField(required=False)
    delivery_type = serializers.IntegerField(required=False)
    created_at = serializers.DateField(required=False)
    id = serializers.IntegerField(required=False)
    vehicle = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        return {
            'courier': StaffSerializer(instance.courier).data,
            'end_time': instance.end_time,
            'start_time': instance.start_time,
            'delivery_type': instance.delivery_type,
            'created_at': instance.created_at,
            'id': instance.id,
            'vehicle': instance.vehicle.id if instance.vehicle else None,
            'order_status': instance.order_status,
            'daily_ransom': instance.daily_ransom,
        }

    class Meta:
        model = CourierShift
        fields = (
            'courier',
            'end_time',
            'delivery_type',
            'created_at',
            'id',
            'vehicle',
            'order',
        )


class InputCourierSerializer(serializers.Serializer):
    date_0 = serializers.DateField(required=False, default=timezone.now)
    date_1 = serializers.DateField(required=False, default=timezone.now)
    end_time = serializers.CharField(required=False)


class ExpensesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    custom_name = serializers.CharField()

    class Meta:
        model = ExpensesType
        fields = (
            'id',
            'name',
            'custom_name',
        )


class CourierShiftExpensesSerializer(serializers.ModelSerializer):
    expenses = serializers.IntegerField(required=False)
    amount = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    courier_shift = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        return {
            'expenses': instance.expenses.name,
            'amount': instance.amount,
            'id': instance.id,
        }

    class Meta:
        model = CourierShiftExpenses
        fields = (
            'id',
            'expenses',
            'courier_shift',
            'amount',
        )

    def create(self, validated_data):
        instance = CourierShiftExpenses.objects.create(
            expenses_id=self.context.get('pk'),
            amount=validated_data.get('amount'),
            courier_shift_id=validated_data.get('courier_shift'),
        )

        return instance

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        attrs = super().validate(attrs)
        courier_shift_id = attrs.get('courier_shift')
        expenses_id = self.context.get('pk')
        if courier_shift_id is None:
            raise serializers.ValidationError('courier_shift field is required')
        if expenses_id is None:
            raise serializers.ValidationError('expenses field is required')
        if attrs.get('amount') is None:
            raise serializers.ValidationError('amount field is required')
        courier_day = CourierShift.objects.get(id=courier_shift_id)
        today = datetime.datetime.now().date()
        if courier_day.end_time is not None or courier_day.start_time.date() != today:
            raise serializers.ValidationError('Object is out of date')
        return attrs


class CashierSerializer(serializers.ModelSerializer):
    cashier = serializers.IntegerField(required=False)
    start_time = serializers.DateField(required=False)
    end_time = serializers.DateField(required=False)
    id = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'cashier': instance.cashier.username,
            'start_time': instance.start_time,
            'end_time': instance.end_time,
        }

    class Meta:
        model = CashierShift
        fields = (
            'id',
            'cashier',
            'start_time',
            'end_time',
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        cashier_user = self.context.get('pk')
        action = self.context.get('action')
        if action == 'create':
            existing_cashier_shift = CashierShift.objects.filter(
                cashier_id=cashier_user,
                end_time__isnull=True,
            )
            if existing_cashier_shift.first():
                raise serializers.ValidationError('this user does not and previous shift')

        return attrs

    def create(self, validated_data):
        today = datetime.datetime.now().date()
        instance, created = CashierShift.objects.get_or_create(
            start_time__date=today,
            cashier_id=self.context.get('pk')
        )
        return instance

    def update(self, instance, validated_data):
        instance.end_time = validated_data['end_time']
        instance.save()
        return instance


class DailyRansomSerializer(serializers.ModelSerializer):
    cashier_shift = serializers.IntegerField(required=False)
    courier_shift = serializers.IntegerField(required=False)
    amount = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        return {
            'cashier_shift': instance.cashier_shift.id,
            'courier_shift': instance.courier_shift.id,
            'amount': instance.amount,
            'created_at': instance.created_at,
        }

    def create(self, validated_data):
        instance, created = DailyRansom.objects.get_or_create(
            cashier_shift_id=validated_data['cashier_shift'],
            courier_shift_id=validated_data['courier_shift'],
            amount=validated_data['amount'],
        )
        return instance

    class Meta:
        model = DailyRansom
        fields = (
            'cashier_shift',
            'courier_shift',
            'amount',
        )
        read_only_fields = (
            'cashier_shift',
            'courier_shift',
            'amount',
        )


class CitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True)
    custom_name = serializers.CharField(required=False, default=None)

    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'custom_name',
        )

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance

    def create(self, validated_data):
        instance, created = City.objects.get_or_create(
            name=validated_data['name'],
            custom_name=validated_data.get('custom_name'),
        )
        return instance


class DistrictToRepresentation(serializers.Serializer):
    name = serializers.CharField()
    custom_name = serializers.CharField()
    id = serializers.IntegerField()


class DistrictSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    custom_name = serializers.CharField(required=False, default=None)

    def to_representation(self, instance):
        return DistrictToRepresentation(instance).data

    class Meta:
        model = District
        fields = (
            'id',
            'name',
            'custom_name',
        )

    def create(self, validated_data):
        city = validated_data['city']
        name = validated_data['name']
        custom_name = validated_data['custom_name']
        instance, created = District.objects.get_or_create(
            city_id=city,
            custom_name=custom_name,
            name=name,
        )
        return instance

    def update(self, instance, validated_data):
        instanse_to_update = District.objects.filter(id=instance.id)
        instanse_to_update.update(**validated_data)
        return instanse_to_update.first()


class StreetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    custom_name = serializers.CharField(required=False, default=None)

    class Meta:
        model = Street
        fields = (
            'id',
            'name',
            'custom_name',
        )

    def create(self, validated_data):
        name = validated_data['name']
        custom_name = validated_data['custom_name']
        instance, created = Street.objects.get_or_create(
            name=name,
            custom_name=custom_name,
        )
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.custom_name = validated_data['custom_name']
        instance.save()
        return instance


class AddressToRepresentation(serializers.Serializer):
    city = CitySerializer()
    district = DistrictSerializer()
    street = StreetSerializer()
    house = serializers.IntegerField()
    flat = serializers.IntegerField()
    floor = serializers.IntegerField()
    id = serializers.IntegerField()
    custom_name = serializers.CharField()


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.IntegerField(required=False)
    district = serializers.IntegerField(required=False)
    street = serializers.IntegerField(required=False)
    house = serializers.IntegerField(required=False, default=None)
    flat = serializers.IntegerField(required=False, default=None)
    floor = serializers.IntegerField(required=False, default=None)

    def to_representation(self, instance):
        return AddressToRepresentation(instance).data

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    class Meta:
        model = Address
        fields = (
            'id',
            'city',
            'district',
            'street',
            'house',
            'flat',
            'floor',
        )

    def create(self, validated_data):
        city = validated_data['city']
        district = validated_data['district']
        street = validated_data['street']
        house = validated_data['house']
        flat = validated_data['flat']
        floor = validated_data['floor']
        instance, created = Address.objects.get_or_create(
            city_id=city,
            district_id=district,
            street_id=street,
            house=house,
            flat=flat,
            floor=floor,
        )
        return instance

    def update(self, instance, validated_data):
        instance_to_update = Address.objects.filter(id=instance.id)
        instance_to_update.update(**validated_data)
        return instance_to_update.first()


class OperatorEndShiftSerializer(serializers.Serializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def update(self, instance, validated_data):
        instance.end_time = timezone.now()
        instance.save()
        return instance

    def create(self, validated_data):
        instance = OperatorShift.objects.filter(
            end_time__isnull=True, operator_id=self.context.get('pk')
        ).order_by('-created_at').first()
        return self.update(instance, validated_data)


class OperatorShiftSerializer(serializers.ModelSerializer):
    # user = serializers.IntegerField(required=True)
    # date = serializers.DateField(required=True)

    class Meta:
        model = OperatorShift
        fields = (
            'id',
            'start_time',
            'end_time',
            'operator',
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        date = attrs.get('date')
        operator_id = attrs.get('user')
        current_operator_shift = OperatorShift.objects.filter(
            operator_id=operator_id,
            end_time__isnull=True
        ).order_by(
            '-created_at'
        ).first()
        now = timezone.now()
        if current_operator_shift:
            started = current_operator_shift.created_at
            diff = now - started
            diff_days, diff_hour = diff.days, diff.seconds//3600
            if diff_days or diff_hour > 10:
                raise serializers.ValidationError('please end up your previous shift')

        return attrs


class OperatorSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)

    class Meta:
        model = OperatorShift
        fields = (
            'id',
            'start_time',
            'end_time',
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        action = self.context.get('action')
        if action == 'create':
            existing_operator_shift = OperatorShift.objects.filter(
                end_time__isnull=True,
                operator_id=self.context.get('pk'),
            ).first()
            if existing_operator_shift:
                raise serializers.ValidationError('The user does not finish previous shift')

        return attrs

    def create(self, validated_data):
        instance, cretaed = OperatorShift.objects.get_or_create(
            start_time=timezone.now(),
            operator_id=self.context.get('pk')
        )
        return instance


class OrderSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address_from = None
        self.address_to = None

    id = serializers.IntegerField(required=False)
    courier_shift = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    start_time = serializers.DateField(required=False)
    end_time = serializers.DateField(required=False, format="%Y-%m-%d %H:%M:%S")
    created_by = serializers.IntegerField(required=False)
    reciever_name = serializers.CharField(required=False)
    customer = serializers.IntegerField(required=False)
    info = serializers.CharField(required=False)
    ransom_sum = serializers.IntegerField(required=False)
    delivery_from = serializers.JSONField(required=False)
    delivery_to = serializers.JSONField(required=False)
    wait_time = serializers.IntegerField(required=False)
    delivery_cost = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "courier_shift": CourierShiftSerializer(instance.courier_shift).data,
            "status": instance.status,
            "start_time": instance.start_time,
            "end_time": instance.end_time,
            "created_by": UserSerializer(instance.created_by).data,
            "reciever_name": instance.reciever_name,
            "customer": UserSerializer(instance.customer).data,
            "info": instance.info,
            "ransom_sum": instance.ransom_sum,
            "delivery_from": AddressSerializer(instance.delivery_from).data,
            "delivery_to": AddressSerializer(instance.delivery_to).data,
            "delivery_cost": instance.delivery_cost,
        }

    class Meta:
        model = Order
        fields = (
            'id',
            'courier_shift',
            'status',
            'start_time',
            'end_time',
            'created_by',
            'reciever_name',
            'customer',
            'info',
            'ransom_sum',
            'delivery_from',
            'delivery_to',
            'delivery_cost',
            'wait_time',
        )

    def update(self, instance, validated_data):
        order_status_map = {
            'accepted': ORDER_STATUS_ACCEPTED,
            'canceled': ORDER_STATUS_CANCELED,
            'done': ORDER_STATUS_DONE,
            'in_progress': ORDER_STATUS_IN_PROGRESS,
        }
        end_date = validated_data.get('end_date')
        # today_date_time = datetime.datetime.now()
        today_date_time = timezone.now()
        status = validated_data.get('status')
        if status:
            if status == ORDER_STATUS_DONE:
                instance.end_time = today_date_time
                str_time = str(instance.end_time - instance.start_time)
                instance.delivery_time = str_time
            if status == ORDER_STATUS_IN_PROGRESS:
                instance.start_time = today_date_time
            instance.status = order_status_map[status]
        if end_date:
            instance.end_date = today_date_time
        instance.save()
        return instance

    def validate(self, attrs):
        attrs = super().validate(attrs)
        courier_shift = attrs.get('courier_shift')
        created_by = attrs.get('created_by')
        delivery_from = attrs.get('delivery_from')
        delivery_to = attrs.get('delivery_to')
        ransom_sum = attrs.get('ransom_sum')
        delivery_cost = attrs.get('delivery_cost')

        if delivery_from:
            self.address_from, created = Address.objects.get_or_create(
                city_id=1,
                street_id=delivery_from['street'],
                district_id=delivery_from['district'],
                house=delivery_from.get('house'),
                flat=delivery_from.get('flat')
            )
        if delivery_to:
            self.address_to, created = Address.objects.get_or_create(
                city_id=1,
                street_id=delivery_to['street'],
                district_id=delivery_to['district'],
                house=delivery_to.get('house'),
                flat=delivery_to.get('flat')
            )
        if not courier_shift:
            raise serializers.ValidationError('You have to select courier')

        return attrs

    def create(self, validated_data):
        instance, created = Order.objects.get_or_create(
            courier_shift_id=validated_data['courier_shift'],
            created_by_id=validated_data['created_by'],
            ransom_sum=validated_data.get('ransom_sum'),
            delivery_from=self.address_from,
            delivery_to=self.address_to,
            delivery_cost=validated_data.get('delivery_cost'),
            info=validated_data.get('info')
        )
        return instance


class OrderDeliveryToSerializer(OrderSerializer):
    def create(self, validated_data):
        instance = Order.objects.get(id=self.context.get('pk'))
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.delivery_to_id = validated_data['delivery_to']
        instance.save()
        return instance


class OrderDeliveryCostSerializer(OrderSerializer):
    def create(self, validated_data):
        instance = Order.objects.get(id=self.context.get('pk'))
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.delivery_cost = validated_data['delivery_cost']
        instance.save()
        return instance


class OrderCourierAcceptSerializer(OrderSerializer):
    def create(self, validated_data):
        instance = Order.objects.get(id=self.context.get('pk'))
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.accepted_time = datetime.datetime.now()
        instance.status = ORDER_STATUS_ACCEPTED
        instance.save()
        return instance


class OrderToInProgressSerializer(OrderSerializer):
    def create(self, validated_data):
        instance = Order.objects.get(id=self.context.get('pk'))
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.start_time = datetime.datetime.now()
        instance.status = ORDER_STATUS_IN_PROGRESS
        instance.save()
        return instance


class FinesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    custom_name = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Fines
        fields = (
            'name',
            'custom_name',
            'id',
            'description',
        )

    def create(self, validated_data):
        instance, created = Fines.objects.get_or_create(
            name=validated_data['name']
        )
        return instance

    def update(self, instance, validated_data):
        instance_to_update = Fines.objects.filter(id=instance.id).update(**validated_data)
        return instance_to_update.first()
