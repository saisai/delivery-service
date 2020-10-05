from django.contrib.auth.models import Permission
from django.db.models import Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets, decorators, mixins
from rest_framework.pagination import PageNumberPagination

from filterset import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from permissions import IsHeadOperator
from django.utils.functional import cached_property
import api.permissions as custom_permissions


class TokenAuthViewSet(viewsets.ViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AuthTokenSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            data={'detail': 'Enter username and password to obtain auth token'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user_serializer = AuthUserSerializer(instance=user)
        return_data = user_serializer.data

        token, created = Token.objects.get_or_create(user=user)
        return_data['token'] = token.key

        return Response(return_data)


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSelfSerializer
    permission_classes = [IsHeadOperator]
    filter_backends = (DjangoFilterBackend,)
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    @decorators.action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def me(self, request, *args, **kwargs):
        logged_user = self.request.user
        logged_user.permissions = Permission.objects.filter(
            user=logged_user,
        ).select_related('content_type')
        return Response(UserSelfSerializer(logged_user).data)


class CourierViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = CouriersShiftSerializer
    queryset = CourierShift.objects.all().prefetch_related('courier_orders')

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = CourierShiftFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            order_status=Subquery(
                Order.objects.filter(
                    courier_shift_id=OuterRef('id')
                ).values('status')[:1]
            ),
            daily_ransom=Subquery(
                DailyRansom.objects.filter(
                    courier_shift_id=OuterRef('id')
                ).values('amount')[:1]
            )
        )
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @cached_property
    def _params(self):
        serializer = InputCourierSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get_serializer_class(self):
        if self.action == 'start':
            return CourierShiftSerializer
        if self.action == 'update':
            return UpdateDailyCourierSerializer
        if self.action == 'assign_vehicle':
            return AssignVehicleSerializer
        if self.action == 'take_vehicle':
            return TakeVehicleSerializer
        return self.serializer_class

    @decorators.action(
        methods=('post',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsCourier),
        url_path='start'
    )
    def start(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if pk and request.user.id != int(pk):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializer_class(data=request.data, context={'pk': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @decorators.action(
        methods=('post',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsVehicleReceiver,),
        url_path='take-vehicle'
    )
    def take_vehicle(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk, 'request_user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @decorators.action(
        methods=('post',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsVehicleReceiver,),
        url_path='assign-vehicle'
    )
    def assign_vehicle(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk, 'request_user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ExpensesViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ExpensesType.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'courier_expenses':
            return CourierShiftExpensesSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    @decorators.action(
        methods=('post',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='courier_expenses'
    )
    def courier_expenses(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CashierViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = CashierSerializer
    queryset = CashierShift.objects.all()
    permission_classes = (permissions.IsAuthenticated, custom_permissions.IsCashier)

    def list(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @decorators.action(
        methods=('post',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsCashier),
        url_path='start'
    )
    def start(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk, 'action': 'create'})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DailyRansomViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = DailyRansomSerializer
    queryset = DailyRansom.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = DailyRansomFilterSet

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CityViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DistrictViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    # filter_backends = (DjangoFilterBackend, )
    # filter_class = DistrictFilterSet

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StreetViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = StreetSerializer
    queryset = Street.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = StreetFilterSet

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all().select_related('city', 'district', 'street')
    filter_backends = (DjangoFilterBackend,)
    filter_class = AddressFilterSet

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OperatorViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = OperatorSerializer
    queryset = OperatorShift.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = OperatorFilterSet

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    @decorators.action(
        methods=('post',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsOperator),
        url_path='start',
    )
    def start(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk, 'action': 'create'})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'check_shift':
            return OperatorShiftSerializer
        if self.action == 'end':
            return OperatorEndShiftSerializer
        return self.serializer_class

    @decorators.action(
        methods=('get',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsOperator),
        url_path='check_shift',
    )
    def check_shift(self, request):
        serializer_class = self.get_serializer_class()
        qs = self.filter_queryset(self.get_queryset())
        serializer = serializer_class(qs, many=True)

        return Response(
            self.check_operator_shift(serializer.data, request.query_params)
        )

    def check_operator_shift(self, data, query_params):
        current_operator_shift = OperatorShift.objects.filter(
            operator_id=query_params.get('user'),
            end_time__isnull=True
        ).order_by(
            '-created_at'
        ).first()
        now = timezone.now()
        if current_operator_shift:
            started = current_operator_shift.created_at
            diff = now - started
            diff_days, diff_hour = diff.days, diff.seconds // 3600
            if diff_days or diff_hour > 10:
                return {
                    'non_field_errors': ['to old for this shit']
                }
        return data

    @decorators.action(
        methods=('put',),
        detail=True,
        permission_classes=(permissions.IsAuthenticated, custom_permissions.IsOperator),
        url_path='end',
    )
    def end(self, request, pk=None, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if pk and request.user.id != int(pk):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializer_class(data=request.data, context={'pk': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related(
        'courier_shift',
        'created_by',
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrderFilterSet
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @decorators.action(
        methods=('put',),
        permission_classes=(permissions.IsAuthenticated,),
        detail=True,
        url_path='delivery_to'
    )
    def delivery_to(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk, 'action': 'delivery_to'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @decorators.action(
        methods=('put',),
        permission_classes=(permissions.IsAuthenticated,),
        detail=True,
        url_path='delivery_cost'
    )
    def delivery_cost(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'pk': pk, 'action': 'delivery_cost'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'delivery_to':
            return OrderDeliveryToSerializer
        if self.action == 'delivery_cost':
            return OrderDeliveryCostSerializer
        return self.serializer_class


class FinesViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FinesSerializer
    queryset = Fines.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = FinesFilterSet

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
