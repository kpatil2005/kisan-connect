from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Newsletter
from django.utils import timezone
from datetime import timedelta
import threading

last_email_sent = None

@receiver(post_save, sender=Product)
def send_new_product_email(sender, instance, created, **kwargs):
    global last_email_sent
    if created:
        now = timezone.now()
        if last_email_sent and (now - last_email_sent) < timedelta(minutes=5):
            return
        
        last_email_sent = now
        
        def send_emails():
            import sib_api_v3_sdk
            import os
            from datetime import timedelta
            
            subscribers = Newsletter.objects.filter(is_active=True)
            if not subscribers.exists():
                return
            
            recent_products = Product.objects.filter(
                id__gte=instance.id - 100
            ).order_by('-id')[:5]
            total_new = Product.objects.filter(id__gte=instance.id - 100).count()
            
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY', '')
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            
            products_html = ""
            for p in recent_products:
                products_html += f"""
                <div style="background:#fff;padding:15px;border-radius:10px;margin:15px 0;border-left:4px solid #2e7d32">
                    <h3 style="color:#2e7d32;margin:0 0 10px 0">{p.title}</h3>
                    <p style="color:#555;margin:5px 0">{p.description[:80]}...</p>
                    <p style="font-size:18px;color:#2e7d32;font-weight:bold;margin:10px 0 0 0">₹{p.discounted_price}</p>
                </div>
                """
            
            more_text = ""
            if total_new > 5:
                more_text = f"<p style='text-align:center;color:#666;font-size:16px;margin:20px 0'>...and {total_new - 5} more products!</p>"
            
            subject = f"🌾 {total_new} New Products Added!"
            message = f"""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;background:#f8fdf9">
                <h2 style="color:#2e7d32;text-align:center">🎉 {total_new} New Products Available!</h2>
                <p style="text-align:center;color:#666;font-size:16px">Check out our latest additions</p>
                {products_html}
                {more_text}
                <div style="text-align:center;margin:30px 0">
                    <a href="http://127.0.0.1:8000/schemes" style="background:#2e7d32;color:#fff;padding:15px 40px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block">View All Products</a>
                </div>
            </div>
            """
            
            for subscriber in subscribers:
                try:
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                        to=[{"email": subscriber.email}],
                        sender={"name": "Kisan Connect", "email": "kisansetu1@gmail.com"},
                        subject=subject,
                        html_content=message
                    )
                    api_instance.send_transac_email(send_smtp_email)
                except:
                    pass
        
        threading.Thread(target=send_emails).start()
