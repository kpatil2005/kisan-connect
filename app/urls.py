from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm , MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth.views import LogoutView
from .chatbot_standalone import ai_chatbot

app_name = "app"

urlpatterns = [
   # Basic pages
path("", views.home, name="home"),              # loads index.html
path("schemes/", views.home_page, name="schemes"),  # loads home.html
path("about/", views.about, name="about"),
path("contact/", views.contact, name="contact"),


# Navbar extra pages
path("weather/", views.weather, name="weather"),
path("crops/", views.crops, name="crops"),
path("fertilizers/", views.fertilizers, name="fertilizers"),
path("marketplace/", views.marketplace, name="marketplace"),
path("search/", views.search, name="search"),
path("forum/", views.forum, name="forum"),
path("news/", views.news, name="news"),
path("support/", views.support, name="support"),
path("signin/", views.signin, name="signin"),
path("prediction/", views.prediction, name="prediction"),
# farming advice
 path("advice/", views.farming_advice, name="farming_advice"),
 path("advice/", views.farming_advice, name="advice"),






    # Category and product
    path("category/<str:val>/", views.CategoryView.as_view(), name="category"),
    path("category-title/<str:val>/", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),

    # Customer profile and addresses
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('orders/', views.orders, name='orders'),
    path("address/", views.address, name="address"),
    path("updateAddress/<int:pk>", views.UpdateAddress.as_view(), name="updateAddress"),
    path('add-to-cart/',views.add_to_cart, name='addtocart'),
    path('cart/',views.show_cart, name='showcart'),
    path('checkout/',views.checkout.as_view(), name='checkout'),
    path("place-order/", views.place_order, name="place_order"),
    path("order-success/", views.order_success, name="order_success"),
    path("capture_and_predict/", views.capture_and_predict, name="capture_and_predict"),


    path('pluscart/', views.plus_cart, name='pluscart'),

    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    

    # Authentication
    path("registration/", views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path(
        "accounts/login/",
        auth_view.LoginView.as_view(
            template_name='app/login.html',
            authentication_form=LoginForm
        ),
        name="login"
    ),

    # Password management
    path(
        "passwordchange/",
        auth_view.PasswordChangeView.as_view(
            template_name="app/changepassword.html",
            form_class=MyPasswordChangeForm,
            success_url="/passwordchangedone/"
        ),
        name="passwordchange"
    ),
    path(
        "passwordchangedone/",
        auth_view.PasswordChangeDoneView.as_view(
            template_name="app/passwordchangedone.html"
        ),
        name="passwordchangedone"
    ),
    path(
    'logout/',
    LogoutView.as_view(next_page='app:login'),  # redirects to login
    name='logout'
    ),
    path(
    'password-reset/',
    auth_view.PasswordResetView.as_view(
        template_name='app/password_reset.html',
        email_template_name='app/password_reset_email.html',
        form_class=MyPasswordResetForm,
        success_url=reverse_lazy('app:password_reset_done')  # <-- Add this
    ),
    name='password_reset'
),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    
    path(
    'password-reset-confirm/<uidb64>/<token>/',
    auth_view.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm,
        success_url=reverse_lazy('app:password_reset_complete')  # <-- Add this
    ),
    name='password_reset_confirm'
),
    
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    # urls.py
    path('addresses/', views.addresses, name='addresses'),  # not updateAddress
    path('address/update/<int:pk>/', views.update_address, name='update_address'),  # ✅ Add this
    
    
     # Forum URLs (updated)
    path('forum/', views.forum, name='forum'),
    path('forum/get_districts/', views.get_districts, name='get_districts'),
    path('forum/add_group/', views.add_group, name='add_group'),

    # AI Chatbot
    path('ai-chat/', ai_chatbot, name='ai_chatbot'),
    
    # Disease Prediction
    path('disease-detection/', views.disease_detection, name='disease_detection'),
    path('predict-disease/', views.predict_disease, name='predict_disease'),
    path('download-disease-pdf/', views.download_disease_pdf, name='download_disease_pdf'),
    path('weather-disease-alert/', views.weather_disease_alert, name='weather_disease_alert'),
    
    # Newsletter
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('admin/send-newsletter/', views.send_newsletter_view, name='send_newsletter'),
]
