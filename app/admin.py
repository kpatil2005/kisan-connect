from django.contrib import admin
from .models import Product, Customer, OrderPlaced, Payment
from .models import Cart

# Register your models here.

@admin.register(Product)
class productModel(admin.ModelAdmin):
    list_display = ['id','title', 'discounted_price', 'category','product_image']
   
   
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']    
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']    
    
from django.contrib import admin
from .models import Product, Customer, OrderPlaced, Payment, Cart, CommunityGroup

# ... (Keep your existing admin registrations) ...
    
@admin.register(CommunityGroup)
class CommunityGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'state', 'district', 'region', 'is_approved', 'platform', 'created_at']
    list_filter = ['state', 'is_approved', 'platform']
    search_fields = ['group_name', 'state', 'district']
    actions = ['approve_groups']

    def approve_groups(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected groups have been approved.")
    approve_groups.short_description = "Approve selected community groups"   