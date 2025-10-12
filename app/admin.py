from django.contrib import admin
from .models import Product, Customer, OrderPlaced, Payment
from .models import Cart

# Register your models here.

@admin.register(Product)
class productModel(admin.ModelAdmin):
    list_display = ['id','title', 'discounted_price', 'category','product_image']
    search_fields = ['title', 'description', 'composition', 'category']
    list_filter = ['category']
   
   
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']
    search_fields = ['user__username', 'user__email', 'name', 'city', 'state', 'mobile']
    list_filter = ['state', 'city']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    search_fields = ['user__username', 'product__title']
    list_filter = ['user']
    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']
    search_fields = ['user__username', 'razorpay_order_id', 'razorpay_payment_id']
    list_filter = ['paid', 'razorpay_payment_status']    
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']
    search_fields = ['user__username', 'customer__name', 'product__title', 'status']
    list_filter = ['status', 'ordered_date']
    date_hierarchy = 'ordered_date'    
    
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


from .models import Newsletter
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import os

try:
    import sib_api_v3_sdk
    BREVO_AVAILABLE = True
except ImportError:
    BREVO_AVAILABLE = False

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    date_hierarchy = 'subscribed_at'
    change_list_template = 'app/newsletter_changelist.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-newsletter/', self.admin_site.admin_view(self.send_newsletter_view), name='send_newsletter'),
        ]
        return custom_urls + urls
    
    def send_newsletter_view(self, request):
        subscriber_count = Newsletter.objects.filter(is_active=True).count()
        
        if request.method == "POST":
            email_type = request.POST.get('email_type')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            subscribers = Newsletter.objects.filter(is_active=True)
            
            if not BREVO_AVAILABLE:
                messages.error(request, "Brevo API not available. Install sib-api-v3-sdk")
                return redirect('..')
            
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY', '')
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            
            sent_count = 0
            failed = []
            for subscriber in subscribers:
                try:
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                        to=[{"email": subscriber.email}],
                        sender={"name": "Kisan Connect", "email": "kisansetu1@gmail.com"},
                        subject=subject,
                        html_content=message
                    )
                    api_instance.send_transac_email(send_smtp_email)
                    sent_count += 1
                except Exception as e:
                    failed.append(subscriber.email)
                    print(f"Failed {subscriber.email}: {e}")
            
            if failed:
                messages.warning(request, f"✅ Sent: {sent_count}, Failed: {len(failed)}. Check console.")
            else:
                messages.success(request, f"✅ Newsletter sent to {sent_count} subscribers!")
            return redirect('..')
        
        from django.contrib.admin import site
        context = {
            'subscriber_count': subscriber_count,
            'site': site,
            'has_permission': True,
        }
        return render(request, 'app/send_newsletter.html', context)
