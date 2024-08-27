import django_filters
from .models import Order, User, Category, MenuItem

class OrderFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date')
    status = django_filters.BooleanFilter(field_name='status')

    class Meta:
        model = Order
        fields = ['date', 'status']

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'email']
        
class CategoryFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['slug', 'title']
        
class MenuItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    featured = django_filters.BooleanFilter()
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ['title', 'price_min', 'price_max', 'featured', 'category']
