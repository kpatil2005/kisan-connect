# Kisan Connect - Agricultural Marketplace Platform

## 📋 Project Overview

**Kisan Connect** is a comprehensive Django-based agricultural e-commerce platform designed to empower farmers with modern digital solutions. The platform provides a complete marketplace for agricultural products, AI-powered assistance, weather-based farming advice, and community features.

**Live URL:** https://kisan-connect.onrender.com  
**GitHub:** https://github.com/kpatil2005/kisan-connect

---

## 🚀 Key Features

### 1. **E-Commerce Marketplace**
- Complete product catalog (Seeds, Fertilizers, Equipment, Machinery)
- Product categories with filters
- Shopping cart functionality
- Checkout with Cash on Delivery (COD)
- Order management and tracking
- Product search with advanced filters

### 2. **Smart Authentication System**
- User registration with auto-login
- Smart session management (30-minute timeout)
- Persistent login while browsing
- Password reset functionality
- Profile management

### 3. **AI-Powered Features**
- **Gemini AI Chatbot**: Multi-language support (English/Marathi)
- **Voice Input/Output**: Speech recognition and text-to-speech
- **Weather-Based Farming Advice**: Location-specific recommendations
- **Plant Disease Prediction**: Image-based disease detection

### 4. **Search & Filters**
- Search by product name, description, composition
- Price range filters (Min/Max)
- Category filters
- Sort by: Price (Low/High), Name (A-Z)
- Real-time search results

### 5. **Community Features**
- Community forum with WhatsApp/Telegram groups
- State and district-based group organization
- Admin approval system for groups
- Agricultural news feed

### 6. **Additional Features**
- Multi-language support (English/Marathi)
- Responsive design (Mobile/Tablet/Desktop)
- Weather information integration
- Crop and fertilizer recommendations
- Contact and support pages

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 5.2.6
- **Database:** PostgreSQL (Production), SQLite (Local)
- **Authentication:** Django Auth System
- **Session Management:** Django Sessions

### Frontend
- **Framework:** Bootstrap 5.3.8
- **Icons:** Bootstrap Icons
- **JavaScript:** Vanilla JS, jQuery
- **Styling:** Custom CSS with animations

### AI & APIs
- **AI Model:** Google Gemini 1.5 Flash
- **Weather API:** OpenWeather API
- **News API:** Newsdata.io
- **Translation:** Google Translator (deep-translator)

### Deployment
- **Hosting:** Render.com
- **Web Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Database:** PostgreSQL (Render)

---

## 📁 Project Structure

```
kisan-connect/
├── app/                          # Main application
│   ├── migrations/               # Database migrations
│   ├── static/app/              # Static files (CSS, JS, Images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/app/           # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── home.html           # Homepage
│   │   ├── search.html         # Search results
│   │   ├── category.html       # Category page
│   │   ├── productdetail.html  # Product details
│   │   ├── login.html          # Login page
│   │   └── ...
│   ├── admin.py                # Admin configuration
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # URL routing
│   ├── forms.py                # Django forms
│   ├── middleware.py           # Custom middleware
│   ├── context_processors.py  # Context processors
│   ├── chatbot_standalone.py  # AI chatbot
│   └── utils.py                # Utility functions
├── ec/                          # Project settings
│   ├── settings.py             # Production settings
│   ├── settings_local.py       # Local development settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
├── media/                       # User uploaded files
│   └── product/                # Product images
├── staticfiles/                # Collected static files
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version
├── manage.py                   # Django management script
├── create_superuser.py         # Auto superuser creation
├── products_backup.json        # Product data backup
└── README.md                   # Project readme

```

---

## 🗄️ Database Models

### 1. **Product**
```python
- title: CharField (Product name)
- selling_price: FloatField (Original price)
- discounted_price: FloatField (Sale price)
- description: TextField (Product description)
- composition: TextField (Product composition)
- prodapp: TextField (Product application)
- category: CharField (Product category)
- product_image: ImageField (Product image)
```

### 2. **Customer**
```python
- user: ForeignKey (User)
- name: CharField
- locality: CharField
- city: CharField
- zipcode: IntegerField
- state: CharField
- mobile: CharField
```

### 3. **Cart**
```python
- user: ForeignKey (User)
- product: ForeignKey (Product)
- quantity: PositiveIntegerField
```

### 4. **OrderPlaced**
```python
- user: ForeignKey (User)
- customer: ForeignKey (Customer)
- product: ForeignKey (Product)
- quantity: PositiveIntegerField
- ordered_date: DateTimeField
- status: CharField (Pending, Accepted, Packed, etc.)
- payment: ForeignKey (Payment)
```

### 5. **Payment**
```python
- user: ForeignKey (User)
- amount: FloatField
- razorpay_order_id: CharField
- razorpay_payment_status: CharField
- paid: BooleanField
```

### 6. **CommunityGroup**
```python
- state: CharField
- district: CharField
- region: CharField
- group_name: CharField
- group_link: URLField
- platform: CharField (WhatsApp/Telegram/Signal)
- is_approved: BooleanField
- created_at: DateTimeField
```

---

## 🔐 Authentication & Session Management

### Session Configuration
```python
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Extend on each page visit
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire when browser closes
SESSION_COOKIE_HTTPONLY = True  # Security
SESSION_COOKIE_SECURE = True  # HTTPS only (production)
```

### How It Works
- **Active Browsing:** Session stays active indefinitely while user browses
- **Inactivity:** Session expires after 30 minutes of inactivity
- **Browser Close:** Session expires immediately when browser closes
- **Auto-Login:** Users are automatically logged in after registration

---

## 🎨 Product Categories

| Code | Category | Description |
|------|----------|-------------|
| CR | Seeds | Cereal crop seeds |
| ML | Vegetables | Vegetable seeds |
| LS | Fruits | Fruit seeds |
| MS | Paddy | Paddy/Rice seeds |
| PN | Nutrients | Plant nutrients |
| FT | Fertilizers | Chemical & organic fertilizers |
| EQ | Equipment | Farm tools & equipment |
| MC | Machinery | Tractors, harvesters, etc. |
| GH | Ghee | Dairy products |
| CZ | Cheese | Dairy products |
| IC | Ice-Creams | Dairy products |

---

## 🔍 Search Functionality

### Search Features
1. **Text Search:** Search by product name, description, composition
2. **Price Filter:** Min/Max price range
3. **Category Filter:** Filter by product category
4. **Sorting Options:**
   - Price: Low to High
   - Price: High to Low
   - Name: A to Z

### Search URL
```
/search/?q=wheat&min_price=500&max_price=2000&category=CR&sort=price_low
```

---

## 🤖 AI Chatbot Features

### Capabilities
- Multi-language support (English/Marathi)
- Voice input using Web Speech API
- Text-to-speech output
- Context-aware responses
- Agricultural knowledge base
- Powered by Google Gemini 1.5 Flash

### Integration
```javascript
// Chatbot endpoint
POST /ai-chat/
{
  "message": "How to grow wheat?",
  "language": "en"
}
```

---

## 🌦️ Weather-Based Farming Advice

### Features
- Real-time weather data from OpenWeather API
- Location-specific farming recommendations
- AI-generated actionable advice
- Cached results for 30 minutes
- Multi-language support

### How It Works
1. User enters city name
2. System fetches weather data
3. AI generates farming advice based on weather
4. Advice translated to Marathi if needed
5. Results cached for performance

---

## 📦 Deployment Guide

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/kpatil2005/kisan-connect.git
cd kisan-connect
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run Migrations**
```bash
python manage.py migrate --settings=ec.settings_local
```

4. **Create Superuser**
```bash
python manage.py createsuperuser --settings=ec.settings_local
```

5. **Run Server**
```bash
python manage.py runserver --settings=ec.settings_local
```

6. **Access Application**
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

### Production Deployment (Render)

1. **Push to GitHub**
```bash
git add .
git commit -m "Your message"
git push origin main
```

2. **Render Configuration**
- **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python create_superuser.py
  ```
- **Start Command:**
  ```bash
  gunicorn ec.wsgi
  ```

3. **Environment Variables**
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
OPENWEATHER_API_KEY=your-api-key
GEMINI_API_KEY=your-api-key
NEWSDATA_API_KEY=your-api-key
DATABASE_URL=postgresql://... (auto-configured by Render)
```

4. **Database Setup**
- Render automatically creates PostgreSQL database
- Run in Render Shell:
  ```bash
  python manage.py loaddata products_backup.json
  ```

---

## 🔑 Admin Credentials

### Production (Hosted Site)
- **URL:** https://kisan-connect.onrender.com/admin/
- **Username:** root
- **Password:** root1234

### Local Development
- Create your own superuser using:
  ```bash
  python manage.py createsuperuser --settings=ec.settings_local
  ```

---

## 📊 Key URLs

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Landing page |
| Marketplace | `/schemes/` | Product homepage |
| Search | `/search/` | Search results |
| Category | `/category/<code>/` | Category products |
| Product Detail | `/product-detail/<id>/` | Product details |
| Cart | `/cart/` | Shopping cart |
| Checkout | `/checkout/` | Order checkout |
| Login | `/accounts/login/` | User login |
| Register | `/registration/` | User registration |
| Profile | `/profile/` | User profile |
| Orders | `/orders/` | Order history |
| Forum | `/forum/` | Community forum |
| News | `/news/` | Agricultural news |
| Weather | `/weather/` | Weather info |
| Advice | `/advice/` | Farming advice |
| Admin | `/admin/` | Admin panel |

---

## 🎯 User Workflows

### 1. New User Registration
```
1. Visit homepage → Click "Registration"
2. Fill registration form
3. Submit → Auto-login → Redirect to marketplace
4. Browse products → Add to cart → Checkout
```

### 2. Existing User Login
```
1. Visit homepage → Click "Login"
2. Enter credentials → Submit
3. Redirect to marketplace
4. Session stays active while browsing
5. Session expires after 30 min of inactivity or browser close
```

### 3. Product Purchase
```
1. Browse marketplace or search products
2. Click product → View details
3. Click "Add to Cart"
4. Go to cart → Review items
5. Click "Checkout" → Select address
6. Place order (COD) → Order confirmation
```

### 4. Admin Product Management
```
1. Login to admin panel
2. Go to "Products" → "Add Product"
3. Fill product details and upload image
4. Save → Product appears on marketplace
5. Products stay in database forever
```

---

## 🔧 Configuration Files

### requirements.txt
```
Django==5.2.6
Pillow==11.1.0
django-widget-tweaks==1.5.0
deep-translator==1.11.4
google-generativeai==0.8.4
beautifulsoup4==4.14.2
requests==2.32.3
gunicorn==23.0.0
dj-database-url==2.2.0
whitenoise==6.8.2
psycopg2-binary==2.9.10
django-redis==5.4.0
```

### Procfile
```
web: gunicorn ec.wsgi
```

### runtime.txt
```
python-3.13.0
```

---

## 🐛 Common Issues & Solutions

### 1. Products Not Showing on Hosted Site
**Problem:** Products added locally don't appear on hosted site  
**Solution:** Add products directly via hosted admin panel or import using:
```bash
python manage.py loaddata products_backup.json
```

### 2. Images Not Loading (404 Error)
**Problem:** Product images show 404 error  
**Solution:** Upload images directly via hosted admin panel

### 3. Session Expires Too Quickly
**Problem:** User logged out unexpectedly  
**Solution:** Session extends automatically on each page visit (30 min timeout)

### 4. Login Required on Every Page
**Problem:** User needs to login on each page  
**Solution:** Fixed with SESSION_SAVE_EVERY_REQUEST = True

### 5. Build Failed on Render
**Problem:** Deployment fails with module errors  
**Solution:** Check requirements.txt for corrupted lines, ensure proper encoding

---

## 📈 Future Enhancements

### High Priority
1. ✅ Product search with filters (COMPLETED)
2. Product reviews and ratings
3. Wishlist functionality
4. Email notifications
5. Payment gateway integration (Razorpay/Stripe)

### Medium Priority
6. Product recommendations
7. Bulk order discounts
8. Seller dashboard (multi-vendor)
9. Advanced analytics
10. Mobile app (React Native/Flutter)

### Low Priority
11. Video tutorials
12. Loyalty program
13. Live chat support
14. Social media integration
15. Advanced reporting

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is developed for educational and commercial purposes.

---

## 👨‍💻 Developer Information

**Project:** Kisan Connect - Agricultural Marketplace  
**Developer:** Kisan Connect Team  
**GitHub:** https://github.com/kpatil2005/kisan-connect  
**Live Site:** https://kisan-connect.onrender.com  
**Contact:** kpatil800083@gmail.com

---

## 🙏 Acknowledgments

- Django Framework
- Bootstrap UI Framework
- Google Gemini AI
- OpenWeather API
- Newsdata.io API
- Render Hosting Platform
- GitHub for version control

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact via email: kpatil800083@gmail.com
- Visit: https://kisan-connect.onrender.com/contact/

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
