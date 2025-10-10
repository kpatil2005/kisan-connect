# 🌾 Kisan Connect - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Features](#features)
4. [Project Structure](#project-structure)
5. [Database Models](#database-models)
6. [Installation Guide](#installation-guide)
7. [Configuration](#configuration)
8. [API Integrations](#api-integrations)
9. [User Roles & Authentication](#user-roles--authentication)
10. [Core Functionalities](#core-functionalities)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**Kisan Connect** is a comprehensive agricultural marketplace platform designed to empower farmers with modern technology, AI assistance, and direct market access. The platform bridges the gap between farmers and agricultural resources by providing an all-in-one solution for buying/selling products, getting farming advice, weather updates, and community support.

### Project Goals
- Provide farmers with easy access to agricultural products
- Offer AI-powered farming advice based on weather conditions
- Create a community platform for farmers to connect
- Enable multilingual support (23 Indian languages)
- Deliver real-time weather and news updates

---

## 💻 Technology Stack

### Backend
- **Framework**: Django 5.2.6
- **Language**: Python 3.13
- **Database**: SQLite3 (Development) / PostgreSQL (Production)
- **ORM**: Django ORM

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with custom animations
- **JavaScript** - Interactive features
- **Bootstrap 5** - Responsive design framework
- **Bootstrap Icons** - Icon library

### AI & APIs
- **Google Gemini AI** - Farming advice generation
- **OpenWeather API** - Real-time weather data
- **NewsData.io API** - Agricultural news
- **Google Translator API** - Multi-language support (via deep-translator)

### Storage & Deployment
- **Cloudinary** - Media file storage (images)
- **WhiteNoise** - Static file serving
- **Gunicorn** - WSGI HTTP Server
- **Render** - Cloud hosting platform

### Additional Libraries
- `dj-database-url` - Database configuration
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing
- `requests` - HTTP library
- `django-widget-tweaks` - Form rendering

---

## ✨ Features

### 1. E-Commerce Platform
- **Product Categories**:
  - Seeds (SD)
  - Fertilizers (FT)
  - Machinery (MC)
  - Equipment (EQ)
- Product browsing with filters
- Advanced search functionality
- Shopping cart management
- Checkout & order placement
- Order tracking
- Cash on Delivery (COD) payment

### 2. AI-Powered Farming Advice
- Weather-based recommendations
- City-specific advice
- Multilingual support (English & Marathi)
- Cached responses for faster access
- Actionable bullet-point format

### 3. Weather Integration
- Real-time weather data
- Temperature, humidity, pressure
- Wind speed information
- Weather-based farming tips

### 4. Community Forum
- State and district-based groups
- WhatsApp/Telegram/Signal integration
- Admin-approved group listings
- Farmer networking platform

### 5. Agricultural News
- Latest farming news from India
- Curated agricultural updates
- Real-time news feed

### 6. User Management
- User registration & authentication
- Profile management
- Multiple shipping addresses
- Order history
- Password reset functionality

### 7. AI Chatbot
- Voice-enabled assistant
- 23 Indian language support
- Context-aware responses
- Farming queries assistance

### 8. Additional Features
- Plant disease prediction (image-based)
- Crop recommendations
- Fertilizer suggestions
- Mobile-responsive design
- Session management (30-minute timeout)

---

## 📁 Project Structure

```
ec/
├── app/                          # Main application
│   ├── migrations/               # Database migrations
│   ├── static/app/              # Static files
│   │   ├── css/                 # Stylesheets
│   │   ├── images/              # Images & videos
│   │   └── js/                  # JavaScript files
│   ├── templates/app/           # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Landing page
│   │   ├── home.html            # Main home page
│   │   ├── category.html        # Product categories
│   │   ├── productdetail.html   # Product details
│   │   ├── addtocart.html       # Shopping cart
│   │   ├── checkout.html        # Checkout page
│   │   ├── orders.html          # Order history
│   │   ├── profile.html         # User profile
│   │   ├── advice.html          # Farming advice
│   │   ├── forum.html           # Community forum
│   │   ├── news.html            # News page
│   │   └── ...                  # Other templates
│   ├── admin.py                 # Admin configuration
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── urls.py                  # URL routing
│   ├── forms.py                 # Form definitions
│   ├── middleware.py            # Custom middleware
│   ├── context_processors.py   # Context processors
│   ├── utils.py                 # Utility functions
│   └── chatbot_standalone.py   # AI chatbot logic
├── ec/                          # Project settings
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL config
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
├── media/                       # User-uploaded files
├── staticfiles/                 # Collected static files
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── Procfile                     # Deployment config
└── README.md                    # Project readme
```

---

## 🗄️ Database Models

### 1. Product
Stores agricultural product information.

```python
Fields:
- title: CharField(max_length=100)
- selling_price: FloatField()
- discounted_price: FloatField()
- description: TextField()
- composition: TextField()
- prodapp: TextField()
- category: CharField(choices=CATEGORY_CHOICES)
- product_image: ImageField(upload_to='product')
```

### 2. Customer
Stores customer shipping addresses.

```python
Fields:
- user: ForeignKey(User)
- name: CharField(max_length=100)
- locality: CharField(max_length=200)
- city: CharField(max_length=50)
- zipcode: IntegerField()
- state: CharField(choices=STATE_CHOICES)
- mobile: CharField(max_length=15)
```

### 3. Cart
Manages shopping cart items.

```python
Fields:
- user: ForeignKey(User)
- product: ForeignKey(Product)
- quantity: PositiveIntegerField(default=1)

Methods:
- total_cost: Property that calculates item total
```

### 4. Payment
Tracks payment information.

```python
Fields:
- user: ForeignKey(User)
- amount: FloatField()
- razorpay_order_id: CharField()
- razorpay_payment_status: CharField()
- razorpay_payment_id: CharField()
- paid: BooleanField(default=False)
```

### 5. OrderPlaced
Stores order details.

```python
Fields:
- user: ForeignKey(User)
- customer: ForeignKey(Customer)
- product: ForeignKey(Product)
- quantity: PositiveIntegerField()
- ordered_date: DateTimeField(auto_now_add=True)
- status: CharField(choices=STATUS_CHOICES)
- payment: ForeignKey(Payment)

Methods:
- total_cost: Property that calculates order total
```

### 6. CommunityGroup
Manages farmer community groups.

```python
Fields:
- state: CharField(max_length=50)
- district: CharField(max_length=100)
- region: CharField(max_length=100)
- group_name: CharField(max_length=200)
- group_link: URLField(unique=True)
- platform: CharField(choices=PLATFORM_CHOICES)
- is_approved: BooleanField(default=False)
- created_at: DateTimeField(auto_now_add=True)
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd Plant_Disease_Dataset/Plant_Disease_Dataset/ec
```

#### 2. Create Virtual Environment
```bash
python -m venv env
```

#### 3. Activate Virtual Environment
**Windows:**
```bash
env\Scripts\activate
```

**Linux/Mac:**
```bash
source env/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Set Up Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# API Keys
GEMINI_API_KEY=your-gemini-api-key
OPENWEATHER_API_KEY=your-openweather-api-key
NEWSDATA_API_KEY=your-newsdata-api-key

# Cloudinary (Optional - for production)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

#### 6. Run Migrations
```bash
python manage.py migrate
```

#### 7. Create Superuser
```bash
python manage.py createsuperuser
```

#### 8. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### 9. Run Development Server
```bash
python manage.py runserver
```

#### 10. Access the Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## ⚙️ Configuration

### Django Settings (settings.py)

#### Debug Mode
```python
DEBUG = os.environ.get("DEBUG", "False") == "True"
```

#### Allowed Hosts
```python
ALLOWED_HOSTS = ['kisan-connect.onrender.com', 'localhost', '127.0.0.1']
```

#### Database Configuration
```python
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

#### Static Files
```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
```

#### Media Files
```python
# Local Development
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Production (Cloudinary)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

#### Session Configuration
```python
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
```

---

## 🔌 API Integrations

### 1. Google Gemini AI
**Purpose**: Generate farming advice based on weather conditions

**Configuration**:
```python
import google.generativeai as genai
genai.configure(api_key=settings.GEMINI_API_KEY)
```

**Usage**:
```python
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
advice = response.text.strip()
```

**Get API Key**: https://makersuite.google.com/app/apikey

### 2. OpenWeather API
**Purpose**: Fetch real-time weather data

**Endpoint**:
```
http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric
```

**Response Data**:
- Temperature
- Feels like temperature
- Humidity
- Pressure
- Wind speed
- Weather description

**Get API Key**: https://openweathermap.org/api

### 3. NewsData.io API
**Purpose**: Fetch agricultural news from India

**Endpoint**:
```
https://newsdata.io/api/1/latest
```

**Parameters**:
```python
params = {
    "apikey": API_KEY,
    "q": "farming OR agriculture OR crops OR farmers",
    "language": "en",
    "country": "in",
    "size": 10
}
```

**Get API Key**: https://newsdata.io/

### 4. Google Translator (deep-translator)
**Purpose**: Translate farming advice to regional languages

**Usage**:
```python
from deep_translator import GoogleTranslator
translator = GoogleTranslator(source="auto", target="mr")
translated_text = translator.translate(text)
```

**Supported Languages**: 23 Indian languages

---

## 🔐 User Roles & Authentication

### User Types
1. **Anonymous Users**: Can view landing page only
2. **Registered Users**: Full access to all features
3. **Admin Users**: Access to Django admin panel

### Authentication Flow

#### Registration
1. User fills registration form
2. System validates input
3. User account created
4. Auto-login after registration
5. Redirect to home page

#### Login
1. User enters credentials
2. System authenticates
3. Session created (30-minute timeout)
4. Redirect to requested page or home

#### Password Reset
1. User requests password reset
2. Email sent with reset link
3. User sets new password
4. Confirmation message displayed

### Login Required Middleware
Custom middleware ensures users are logged in for protected pages:

```python
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        # Redirect to login if not
        return self.get_response(request)
```

**Exempt URLs**:
- `/` (landing page)
- `/accounts/login/`
- `/registration/`
- `/password-reset/`
- `/admin/`

---

## 🎯 Core Functionalities

### 1. Product Management

#### Browse Products
- View all products by category
- Filter by price range
- Sort by price/name
- Search functionality

#### Product Detail
- Full product information
- Image display
- Pricing details
- Add to cart button

#### Categories
- **Seeds (SD)**: Wheat, Maize, Paddy, Pulses
- **Fertilizers (FT)**: Urea, DAP, NPK, Vermicompost
- **Machinery (MC)**: Tractors, Harvesters, Rotavators
- **Equipment (EQ)**: Sprayers, Pumps, Tools, Irrigation

### 2. Shopping Cart

#### Add to Cart
```python
@login_required
def add_to_cart(request):
    product_id = request.GET.get("prod_id")
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, 
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
```

#### Update Quantity
- Plus button: Increase quantity
- Minus button: Decrease quantity
- Remove button: Delete item

#### Cart Calculations
```python
amount = sum(item.quantity * item.product.discounted_price for item in cart)
shipping = 40
total = amount + shipping
```

### 3. Checkout & Orders

#### Checkout Process
1. Select shipping address
2. Review cart items
3. Confirm order details
4. Place order (COD)

#### Order Placement
```python
@login_required
def place_order(request):
    # Create payment record
    payment = Payment.objects.create(
        user=user,
        amount=total,
        paid=False,
        razorpay_payment_status="COD"
    )
    
    # Create order records
    for item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            payment=payment,
            status="Pending"
        )
    
    # Clear cart
    cart_items.delete()
```

#### Order Status
- Pending
- Accepted
- Packed
- On The Way
- Delivered
- Cancelled

### 4. Farming Advice System

#### Weather-Based Advice
```python
@login_required
def farming_advice(request):
    city = request.POST.get("city")
    
    # Fetch weather data
    weather = get_weather(city)
    
    # Generate AI advice
    prompt = f"""
    Weather in {city}:
    - Temperature: {temp}°C
    - Humidity: {humidity}%
    - Condition: {description}
    
    Provide short farming advice in bullet points.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    advice_en = response.text.strip()
    
    # Translate to Marathi
    advice_mr = GoogleTranslator(
        source="auto", 
        target="mr"
    ).translate(advice_en)
    
    # Cache for 30 minutes
    cache.set(cache_key, data, 1800)
```

#### Advice Format
- Short bullet points
- Actionable tips
- Weather-specific recommendations
- Bilingual (English & Marathi)

### 5. Community Forum

#### Group Management
- State-based filtering
- District-based filtering
- Platform selection (WhatsApp/Telegram/Signal)
- Admin approval required

#### Add Group
```python
@login_required
def add_group(request):
    form = CommunityGroupForm(request.POST)
    if form.is_valid():
        group = form.save(commit=False)
        group.is_approved = False
        group.save()
        return JsonResponse({
            'success': True,
            'message': 'Group submitted for approval'
        })
```

#### Dynamic Districts
```python
@login_required
def get_districts(request):
    state = request.GET.get('state')
    districts = DISTRICTS_BY_STATE.get(state, [])
    return JsonResponse({'districts': districts})
```

### 6. Search Functionality

#### Advanced Search
```python
@login_required
def search(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', '')
    
    products = Product.objects.all()
    
    # Text search
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(composition__icontains=query)
        )
    
    # Price filter
    if min_price:
        products = products.filter(
            discounted_price__gte=float(min_price)
        )
    if max_price:
        products = products.filter(
            discounted_price__lte=float(max_price)
        )
    
    # Category filter
    if category:
        products = products.filter(category=category)
    
    # Sorting
    if sort == 'price_low':
        products = products.order_by('discounted_price')
    elif sort == 'price_high':
        products = products.order_by('-discounted_price')
```

### 7. Profile Management

#### User Profile
- View personal information
- Manage multiple addresses
- Update profile details
- View order history

#### Address Management
```python
@login_required
def update_address(request, pk):
    address = get_object_or_404(Customer, pk=pk, user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("app:addresses")
```

---

## 🌐 Deployment

### Production Deployment (Render)

#### 1. Prepare for Deployment

**Procfile**:
```
web: gunicorn ec.wsgi:application
```

**runtime.txt**:
```
python-3.13.0
```

**build.sh** (if needed):
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

#### 2. Environment Variables
Set in Render dashboard:
```
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgresql://...
GEMINI_API_KEY=...
OPENWEATHER_API_KEY=...
NEWSDATA_API_KEY=...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

#### 3. Database Setup
- Use PostgreSQL for production
- Run migrations after deployment
- Create superuser via Render shell

#### 4. Static Files
- Collected automatically via build script
- Served by WhiteNoise

#### 5. Media Files
- Uploaded to Cloudinary
- Automatic URL generation

### Local Development

#### Quick Start Script (start_local.bat)
```batch
@echo off
echo Starting Django Development Server...

if exist env\Scripts\activate (
    call env\Scripts\activate
) else (
    echo No virtual environment found
)

echo Running migrations...
python manage.py migrate

echo Starting server at http://127.0.0.1:8000/
python manage.py runserver

pause
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Module Not Found Error
**Problem**: `ModuleNotFoundError: No module named 'dj_database_url'`

**Solution**:
```bash
pip install -r requirements.txt
```

#### 2. Media Files Not Loading (404)
**Problem**: Product images showing 404 errors

**Solution**:
- Check if files exist in `media/product/` folder
- Verify `MEDIA_URL` and `MEDIA_ROOT` settings
- For production, ensure Cloudinary is configured

#### 3. Static Files Not Loading
**Problem**: CSS/JS files not loading

**Solution**:
```bash
python manage.py collectstatic --noinput
```

#### 4. Database Migration Errors
**Problem**: Migration conflicts

**Solution**:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. API Key Errors
**Problem**: Weather/News/AI features not working

**Solution**:
- Verify API keys in `.env` file
- Check API key validity
- Ensure environment variables are loaded

#### 6. Session Timeout Issues
**Problem**: Users logged out too quickly

**Solution**:
Adjust in `settings.py`:
```python
SESSION_COOKIE_AGE = 3600  # 1 hour
```

#### 7. CSRF Token Errors
**Problem**: Form submission fails with CSRF error

**Solution**:
- Ensure `{% csrf_token %}` in forms
- Check middleware configuration
- Verify `CSRF_TRUSTED_ORIGINS` setting

### Debug Mode

Enable detailed error messages:
```python
# settings.py
DEBUG = True
```

**Warning**: Never enable DEBUG in production!

### Logging

Check logs for errors:
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## 📊 Admin Panel

### Access Admin
URL: `http://127.0.0.1:8000/admin/`

### Admin Features
1. **Product Management**
   - Add/Edit/Delete products
   - Upload product images
   - Set pricing

2. **Order Management**
   - View all orders
   - Update order status
   - Track payments

3. **User Management**
   - View registered users
   - Manage permissions
   - Reset passwords

4. **Community Groups**
   - Approve/Reject groups
   - Moderate content

5. **Customer Addresses**
   - View shipping addresses
   - Edit customer details

---

## 🔒 Security Features

1. **CSRF Protection**: Enabled on all forms
2. **SQL Injection Prevention**: Django ORM
3. **XSS Protection**: Template auto-escaping
4. **Secure Cookies**: HTTPOnly, Secure flags
5. **Password Hashing**: PBKDF2 algorithm
6. **Session Security**: 30-minute timeout
7. **Login Required**: Middleware protection

---

## 📱 Mobile Responsiveness

### Responsive Design
- Bootstrap 5 grid system
- Mobile-first approach
- Touch-friendly buttons
- Optimized images

### Breakpoints
- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

---

## 🚀 Future Enhancements

1. **Payment Gateway Integration**
   - Razorpay/Paytm integration
   - Online payment support

2. **Advanced Analytics**
   - Sales reports
   - User behavior tracking
   - Product performance metrics

3. **Mobile App**
   - Native Android/iOS apps
   - Push notifications

4. **Enhanced AI Features**
   - Crop disease detection
   - Yield prediction
   - Market price prediction

5. **Social Features**
   - Farmer profiles
   - Product reviews
   - Discussion forums

6. **Multilingual Support**
   - Complete UI translation
   - Regional language content

---

## 📞 Support & Contact

For issues or questions:
- **Email**: support@kisanconnect.com
- **GitHub**: [Repository Issues](https://github.com/your-repo/issues)
- **Documentation**: This file

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Contributors

- **Developer**: Your Name
- **Project Type**: Agricultural Technology Platform
- **Year**: 2025

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Google Gemini AI](https://ai.google.dev/)
- [OpenWeather API](https://openweathermap.org/api)
- [Cloudinary Documentation](https://cloudinary.com/documentation)

---

**Last Updated**: October 2025
**Version**: 1.0.0
