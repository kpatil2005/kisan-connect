# Kisan Connect - Agricultural Marketplace Platform

## 🌾 Overview
Kisan Connect is a comprehensive agricultural marketplace platform that empowers farmers with modern technology, AI assistance, and direct market access.

## ✨ Features
- **E-commerce Platform** - Buy/sell seeds, fertilizers, equipment, machinery
- **AI Chatbot** - Voice-enabled assistant with 23 Indian languages
- **Weather Integration** - Real-time weather data
- **Community Forum** - Farmer discussions and groups
- **Expert Support** - Agricultural guidance
- **Multi-language** - Support for 23 Indian languages

## 🚀 Technology Stack
- **Backend**: Django 5.2.6, Python 3.13
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite3
- **AI**: Google Gemini API
- **APIs**: OpenWeather, NewsData, Google Translator

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/kisan-connect.git
cd kisan-connect
```

2. **Create virtual environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Start server**
```bash
python manage.py runserver
```

7. **Access the application**
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

## 🔧 Configuration
Add your API keys in `settings.py`:
- GEMINI_API_KEY
- OPENWEATHER_API_KEY
- NEWSDATA_API_KEY

## 📱 Key Features
- **Product Categories**: Seeds, Fertilizers, Equipment, Machinery
- **Shopping Cart**: Add/remove items, checkout
- **User Authentication**: Registration, login, profiles
- **AI Assistant**: Voice + text chatbot
- **Weather Data**: Real-time farming weather
- **Responsive Design**: Mobile-first approach

## 🤝 Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License
This project is licensed under the MIT License.

## 👨‍💻 Author
Your Name - Agricultural Technology Enthusiast