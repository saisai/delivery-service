from django_filters import rest_framework as filters
import api.models as models


class DailyRansomFilterSet(filters.FilterSet):
    date = filters.DateFilter(
        method='filter_date',
    )

    def filter_date(self, queryset, name, value):
        queryset = queryset.filter(
            created_at__date=value
        )
        return queryset


class CourierShiftFilterSet(filters.FilterSet):
    date = filters.DateFilter(
        method='filter_date',
    )
    active = filters.CharFilter(
        method='filter_is_active',
    )
    order = filters.CharFilter(
        method='filter_with_orders'
    )

    def filter_with_order(self, qs, name, value):
        qs = qs.filter(courier_order__isnull=False)
        return qs

    def filter_is_active(self, qs, name, value):
        return qs.filter(is_active=True)

    def filter_date(self, queryset, name, value):
        queryset = queryset.filter(
            start_time__date__lte=value,
            end_time__isnull=True,
        )
        return queryset


class AddressFilterSet(filters.FilterSet):
    city = filters.CharFilter(
        method='filter_city'
    )
    district = filters.CharFilter(
        method='filter_district'
    )
    street = filters.CharFilter(
        method='filter_street'
    )
    custom_name = filters.CharFilter(
        method='filter_cutom_name'
    )

    class Meta:
        model = models.Address
        fields = (
            'city',
            'district',
            'street',
        )

    def filter_cutom_name(self, qs, name, value):
        qs = qs.filter(custom_name__icontains=value)
        return qs

    def filter_city(self, qs, name, value):
        qs = qs.filter(city_id=value)
        return qs

    def filter_district(self, qs, name, value):
        qs = qs.filter(district_id=value)
        return qs

    def filter_street(self, qs, name, value):
        qs = qs.filter(street_id=value)
        return qs


class StreetFilterSet(filters.FilterSet):
    city = filters.NumberFilter(
        field_name='city_id'
    )
    district = filters.NumberFilter(
        field_name='district_id'
    )

    class Meta:
        model = models.Street
        fields = (
            'city',
            'district',
        )


class OrderFilterSet(filters.FilterSet):
    date = filters.CharFilter(
        method='filter_date',
    )
    courier = filters.CharFilter(
        field_name='courier_shift_id',
    )
    status = filters.ChoiceFilter(
        choices=models.ORDER_STATUS_CHOICES,
    )

    def filter_date(self, queryset, name, value):
        queryset = queryset.filter(
            created_at__date=value
        )
        return queryset

    class Meta:
        model = models.Order
        fields = (
            'date',
            'courier',
            'status',
        )


class FinesFilterSet(filters.FilterSet):
    class Meta:
        model = models.Fines
        fields = ()


class OperatorFilterSet(filters.FilterSet):
    class Meta:
        model = models.OperatorShift
        fields = (
            'user',
        )

    user = filters.NumberFilter(
        method='operator_filter'
    )

    def operator_filter(self, queryset, name, value):
        queryset = queryset.filter(
            operator_id=value,
            end_time__isnull=True
        )
        return queryset

