from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class GroupRequiredMixin(AccessMixin):
    group_names = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.groups.filter(name__in=self.group_names).exists():
            raise PermissionDenied("Нямате необходимите права за достъп.")

        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(GroupRequiredMixin):
    group_names = ['Managers']


class MechanicRequiredMixin(GroupRequiredMixin):
    group_names = ['Mechanics', 'Managers']