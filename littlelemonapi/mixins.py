
from rest_framework.exceptions import PermissionDenied

class IsManagerMixin:
    def check_manager_permissions(self):
        if not self.request.user.is_manager:
            raise PermissionDenied("You do not have permission to perform this action.")

class IsDeliveryCrewMixin:
    def check_delivery_crew_permissions(self):
        if not self.request.user.is_delivery_crew:
            raise PermissionDenied("You do not have permission to perform this action.")
