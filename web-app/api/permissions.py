from typing import Optional, Sequence

from rest_framework.permissions import IsAuthenticated

from permission_constants import ProfilePermissions


class IsEmployee(IsAuthenticated):
    def has_permission(self, request, view) -> bool:
        if not super().has_permission(request, view):
            return False

        if not request.user.is_active:
            return False

        profile = request.user
        return profile

    def has_object_permission(self, request, view, obj) -> bool:
        return self.has_permission(request, view)


class DjangoPermissionMixin:
    permissions: Optional[Sequence] = None

    def has_permission(self, request, view) -> bool:
        if not super().has_permission(request, view):
            return False

        if self.permissions is None:
            return True

        return request.user.has_perms(self.permissions)

    def has_object_permission(self, request, view, obj) -> bool:
        if not super().has_object_permission(request, view, obj):
            return False

        return self.has_permission(request, view)


class IsHeadOperator(DjangoPermissionMixin, IsEmployee):
    permissions = (
        ProfilePermissions.CAN_VIEW_HEAD_OPERATOR_TAB,
        ProfilePermissions.CAN_VIEW_OPERATOR_TAB,
        ProfilePermissions.CAN_VIEW_CASHIER_TAB,
    )


class IsOperator(DjangoPermissionMixin, IsEmployee):
    permissions = (
        ProfilePermissions.CAN_VIEW_OPERATOR_TAB,
    )


class IsCashier(DjangoPermissionMixin, IsEmployee):
    permissions = (
        ProfilePermissions.CAN_VIEW_CASHIER_TAB,
    )


class IsCourier(DjangoPermissionMixin, IsEmployee):
    permissions = (
        ProfilePermissions.CAN_VIEW_COURIER_TAB,
    )


class IsVehicleReceiver(DjangoPermissionMixin, IsEmployee):
    permissions = (
        ProfilePermissions.CAN_VIEW_TECH_STUFF_TAB
    )