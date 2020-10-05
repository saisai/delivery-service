from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('token-auth', views.TokenAuthViewSet, basename='token-auth')
router.register('user', views.UserViewSet, basename='user')
router.register('courier', views.CourierViewSet, basename='courier')
router.register('expenses', views.ExpensesViewSet, basename='expenses')
router.register('cashier', views.CashierViewSet, basename='cashier')
router.register('operator', views.OperatorViewSet, basename='operator')
router.register('ransom', views.DailyRansomViewSet, basename='ransom')
# Address
router.register('city', views.CityViewSet, basename='city')
router.register('district', views.DistrictViewSet, basename='district')
router.register('street', views.StreetViewSet, basename='street')
router.register('address', views.AddressViewSet, basename='address')
# Order
router.register('order', views.OrderViewSet, basename='order')
# Fines
router.register('fines', views.FinesViewSet, basename='fines')

urlpatterns = [
    path('auth/', include('rest_framework_social_oauth2.urls')),
    *router.urls,
]
