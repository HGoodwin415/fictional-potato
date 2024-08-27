from rest_framework import generics, permissions, pagination
from rest_framework.exceptions import PermissionDenied
from .mixins import IsManagerMixin, IsDeliveryCrewMixin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter, UserFilter, CategoryFilter, MenuItemFilter
from .models import Category, Cart, Order, OrderItem, MenuItem, User, Testimonial, Reservation
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer, CartSerializer, UserSerializer, TestimonialSerializer, ReservationSerializer
from .permissions import IsCustomer, IsManager, IsDeliveryCrew, ReadOnlyOrIsManager
from rest_framework.views import APIView




class CustomUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user.is_manager and self.kwargs['pk'] != str(user.pk):
            raise PermissionDenied("You do not have permission to view this user's details.")
        return super().get_object()

    def perform_update(self, serializer):
        if not self.request.user.is_manager:
            raise PermissionDenied("You do not have permission to update users.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_manager:
            raise PermissionDenied("You do not have permission to delete users.")
        instance.delete()
        
class ManagerUserListView(generics.ListCreateAPIView, IsManagerMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def perform_create(self, serializer):
        self.check_manager_permissions()
        serializer.save()

class ManagerOrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

class ManagerMenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemFilter

class ManagerRoleUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def perform_update(self, serializer):
        user = self.get_object()
        role_data = self.request.data.get('role')
        if role_data == 'manager':
            user.is_manager = True
            user.is_delivery_crew = False
        elif role_data == 'delivery_crew':
            user.is_delivery_crew = True
            user.is_manager = False
        else:
            user.is_manager = False
            user.is_delivery_crew = False
        user.save()
        
class DeliveryCrewOrderListView(generics.ListAPIView, IsDeliveryCrewMixin):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliveryCrew]

    def get_queryset(self):
        self.check_delivery_crew_permissions()
        return Order.objects.filter(delivery_crew=self.request.user)

class UpdateOrderStatusView(generics.UpdateAPIView, IsDeliveryCrewMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliveryCrew]

    def perform_update(self, serializer):
        self.check_delivery_crew_permissions()
        serializer.save(status=True)
        


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def perform_create(self, serializer):
        serializer.save()

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.filter(featured=True).order_by('id')
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrIsManager]

    def perform_create(self, serializer):
        serializer.save()

class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrIsManager]


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class PaymentView(APIView):
    def post(self, request):
        from rest_framework.response import Response
        from rest_framework import status
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # Process the payment
            order_id = serializer.validated_data['order_id']
            amount = serializer.validated_data['amount']
            payment_successful = self.process_payment(amount)
            
            if payment_successful:
                # Update the order status
                order = Order.objects.get(id=order_id)
                order.status = 'paid'
                order.save()
                
                return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_payment(self, amount):
        
        return True
    
class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]



class AvailableTimesView(APIView):
    def get(self, request):
        from rest_framework.response import Response
        date = request.query_params.get('date')
        party_size = request.query_params.get('party_size')
        available_times = Reservation.get_available_times(date, party_size)
        return Response(available_times)


class TestimonialListCreateView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context