import inspect
from typing import List, Optional, Tuple
from django.utils.translation import ugettext_lazy as _


class classproperty:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class PermissionEnumField:
    title: str
    full_name: str
    permission_name: str

    def __init__(self, title: str, permission_name: Optional[str] = None):
        self.title = title
        self.permission_name = permission_name

    def __get__(self, instance, owner) -> str:
        return self.full_name

    def __set_name__(self, owner, name: str):
        app_name = getattr(owner.Meta, 'app_name', None)
        full_model_name = getattr(owner.Meta, 'full_model_name', None)

        assert app_name or full_model_name

        if not app_name and full_model_name:
            app_name = full_model_name.split('.')[0]

        if self.permission_name is None:
            self.permission_name = name.lower()

        self.full_name = f'{app_name}.{self.permission_name}'


class PermissionEnum:
    _choices = None

    @classproperty
    def CHOICES(cls) -> List[Tuple[str, str]]:
        if cls._choices is not None:
            return cls._choices

        result = []
        classes = inspect.getmro(cls)

        for obj in classes:
            for field in obj.__dict__.values():
                if isinstance(field, PermissionEnumField):
                    result.append((field.permission_name, field.title,))

        cls._choices = result

        return cls._choices

    @staticmethod
    def get_perm_obj(value: str):
        """
        Returns permission object according its full permission name.

        :param value: PermissionEnumField instance.
        """
        global Permission
        if Permission is None:
            from django.contrib.auth.models import Permission

        assert '.' in value

        app_label, codename = value.split('.', maxsplit=1)
        return Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename,
        )


class ProfilePermissions(PermissionEnum):
    CAN_VIEW_COURIER_TAB = PermissionEnumField(
        title=_('Can view courier tab')
    )
    CAN_VIEW_CASHIER_TAB = PermissionEnumField(
        title=_('Can view cashier tab')
    )
    CAN_VIEW_OPERATOR_TAB = PermissionEnumField(
        title=_('Can view operator tab')
    )
    CAN_VIEW_HEAD_OPERATOR_TAB = PermissionEnumField(
        title=_('Can view head operator tab')
    )
    CAN_VIEW_TECH_STUFF_TAB = PermissionEnumField(
        title=_('Can view tech stuff tab')
    )
    CAN_VIEW_CUSTOMER_TAB = PermissionEnumField(
        title=_('Can view customer tab')
    )

    class Meta:
        app_name = "api"


PERMISSIONS_MAP = {
    ProfilePermissions.CAN_VIEW_COURIER_TAB: 'CAN_VIEW_COURIER_TAB',
    ProfilePermissions.CAN_VIEW_CASHIER_TAB: 'CAN_VIEW_CASHIER_TAB',
    ProfilePermissions.CAN_VIEW_OPERATOR_TAB: 'CAN_VIEW_OPERATOR_TAB',
    ProfilePermissions.CAN_VIEW_HEAD_OPERATOR_TAB: 'CAN_VIEW_HEAD_OPERATOR_TAB',
    ProfilePermissions.CAN_VIEW_TECH_STUFF_TAB: 'CAN_VIEW_TECH_STUFF_TAB',
    ProfilePermissions.CAN_VIEW_CUSTOMER_TAB: 'CAN_VIEW_CUSTOMER_TAB',
}
