from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_manager = models.BooleanField(default=False)
    is_delivery_crew = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Manager: {self.user.username}"

class DeliveryCrew(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Delivery Crew: {self.user.username}"

class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, db_index=True)
    
    def __str__(self):
        return self.title
    

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    photo = models.FileField(upload_to='menu_items/', validators=[FileExtensionValidator(['svg', 'png', 'jpg', 'jpeg'])], 
                             blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    description = models.TextField(null=True)
    featured = models.BooleanField(db_index=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
class FeaturedMenuItem(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ['title']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('menuitem', 'user')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()  
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menuitem')
        
class Reservation(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField()
    
    @classmethod
    def get_available_tables(cls, date, time, number_of_guests):
        
        available_tables = Table.objects.filter(
            capacity__gte=number_of_guests,
            reservations__date=date,
            reservations__time=time
        ).distinct()

    def __str__(self):
        return f'Reservation for {self.name} on {self.date} at {self.time}'
    
class Table(models.Model):
    number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'Table {self.number} in {self.location}'

class Testimonial(models.Model):
    photo_url = models.ImageField(upload_to='testimonial_photos/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Testimonial by {self.user.username} on {self.date_created}'
