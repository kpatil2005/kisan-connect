#!/usr/bin/env python
"""Automatically add {% trans %} tags to index.html"""

import re

# Read index.html
with open('app/templates/app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# List of strings to translate (in order of appearance)
translations = [
    ('Profile', '{% trans "Profile" %}'),
    ('Logout', '{% trans "Logout" %}'),
    ('🌾 Empower Your Farm, Every Day', '🌾 {% trans "Empower Your Farm, Every Day" %}'),
    ('🛒 Smart Farming Marketplace', '🛒 {% trans "Smart Farming Marketplace" %}'),
    ('🔬 AI-Powered Disease Detection', '🔬 {% trans "AI-Powered Disease Detection" %}'),
    ('🌤 Weather & Farming Insights', '🌤 {% trans "Weather & Farming Insights" %}'),
    ('🌱 Crop Yield Prediction', '🌱 {% trans "Crop Yield Prediction" %}'),
    ('📜 Find Government Schemes', '📜 {% trans "Find Government Schemes" %}'),
    ('📰 Latest Farming News', '📰 {% trans "Latest Farming News" %}'),
    ('💬 Join the Farmer Community', '💬 {% trans "Join the Farmer Community" %}'),
    ('ℹ️ About Kisan Connect', 'ℹ️ {% trans "About Kisan Connect" %}'),
    ('🌾 Customer Reviews', '🌾 {% trans "Customer Reviews" %}'),
    (' Stay Updated with the Latest Agricultural Products', ' {% trans "Stay Updated with the Latest Agricultural Products" %}'),
    ('>Subscribe<', '>{% trans "Subscribe" %}<'),
    ('>Write Review<', '>{% trans "Write Review" %}<'),
    ('>Total Reviews<', '>{% trans "Total Reviews" %}<'),
    ('>Quality<', '>{% trans "Quality" %}<'),
    ('>Delivery<', '>{% trans "Delivery" %}<'),
    ('>Support<', '>{% trans "Support" %}<'),
    ('>Location<', '>{% trans "Location" %}<'),
    ('>Crop Yield Prediction<', '>{% trans "Crop Yield Prediction" %}<'),
    ('>Data-driven insights using rainfall, temperature, and soil quality for better harvests<', '>{% trans "Data-driven insights using rainfall, temperature, and soil quality for better harvests" %}<'),
    ('>Predict Yield<', '>{% trans "Predict Yield" %}<'),
    ('>Government Schemes & Support<', '>{% trans "Government Schemes & Support" %}<'),
    ('>Discover subsidies, loans, and support programs designed specifically for farmers<', '>{% trans "Discover subsidies, loans, and support programs designed specifically for farmers" %}<'),
    ('>Find Schemes<', '>{% trans "Find Schemes" %}<'),
    ('>Latest Farming News<', '>{% trans "Latest Farming News" %}<'),
    ('>Stay informed with agricultural news, policy changes, and market trends<', '>{% trans "Stay informed with agricultural news, policy changes, and market trends" %}<'),
    ('>Read More<', '>{% trans "Read More" %}<'),
    ('>Farmer Community Forum<', '>{% trans "Farmer Community Forum" %}<'),
    ('>Connect, share knowledge, and learn from experienced agricultural professionals<', '>{% trans "Connect, share knowledge, and learn from experienced agricultural professionals" %}<'),
    ('>Join Forum<', '>{% trans "Join Forum" %}<'),
    ('>Empower Your Farm, Every Day<', '>{% trans "Empower Your Farm, Every Day" %}<'),
    ('>Access tools, seeds, weather updates, and expert advice — everything you need to grow smarter and stronger<', '>{% trans "Access tools, seeds, weather updates, and expert advice — everything you need to grow smarter and stronger" %}<'),
    ('>Premium Seeds<', '>{% trans "Premium Seeds" %}<'),
    ('>High-yield certified seeds<', '>{% trans "High-yield certified seeds" %}<'),
    ('>Weather Insights<', '>{% trans "Weather Insights" %}<'),
    ('>Real-time forecasts<', '>{% trans "Real-time forecasts" %}<'),
    ('>Expert Advice<', '>{% trans "Expert Advice" %}<'),
    ('>24/7 agricultural support<', '>{% trans "24/7 agricultural support" %}<'),
    ('>Modern Tools<', '>{% trans "Modern Tools" %}<'),
    ('>Latest farming equipment<', '>{% trans "Latest farming equipment" %}<'),
    ('>Smart Farming Marketplace<', '>{% trans "Smart Farming Marketplace" %}<'),
    ('>Explore a wide range of seeds, fertilizers, and farming tools. Connect with trusted suppliers and make informed purchases to boost your farm\'s productivity.<', '>{% trans "Explore a wide range of seeds, fertilizers, and farming tools. Connect with trusted suppliers and make informed purchases to boost your farm\'s productivity." %}<'),
    ('>Visit Marketplace<', '>{% trans "Visit Marketplace" %}<'),
    ('>AI-Powered Disease Detection<', '>{% trans "AI-Powered Disease Detection" %}<'),
    ('>Utilize computer vision to analyze your crop photos and accurately detect common diseases, helping you protect your harvest with advanced AI technology.<', '>{% trans "Utilize computer vision to analyze your crop photos and accurately detect common diseases, helping you protect your harvest with advanced AI technology." %}<'),
    ('>Detect Disease<', '>{% trans "Detect Disease" %}<'),
    ('>Weather & Farming Insights<', '>{% trans "Weather & Farming Insights" %}<'),
    ('>Stay updated with real-time weather, temperature, humidity, and get practical farming tips to maximize crop yield and prevent crop damage.<', '>{% trans "Stay updated with real-time weather, temperature, humidity, and get practical farming tips to maximize crop yield and prevent crop damage." %}<'),
    ('>View Advice<', '>{% trans "View Advice" %}<'),
    ('>Crop Yield Prediction<', '>{% trans "Crop Yield Prediction" %}<'),
    ('>Predict your crop yield easily using rainfall, temperature, and soil quality data. Make informed decisions for better harvests with data-driven insights.<', '>{% trans "Predict your crop yield easily using rainfall, temperature, and soil quality data. Make informed decisions for better harvests with data-driven insights." %}<'),
    ('>Predict Yield<', '>{% trans "Predict Yield" %}<'),
    ('>Find Government Schemes<', '>{% trans "Find Government Schemes" %}<'),
    ('>Get access to the best government schemes tailored for you. Discover subsidies, loans, and support programs designed specifically for farmers.<', '>{% trans "Get access to the best government schemes tailored for you. Discover subsidies, loans, and support programs designed specifically for farmers." %}<'),
    ('>Find Schemes<', '>{% trans "Find Schemes" %}<'),
    ('>Latest Farming News<', '>{% trans "Latest Farming News" %}<'),
    ('>Stay updated with the latest agricultural news, policy changes, market trends, and technological innovations affecting the farming industry.<', '>{% trans "Stay updated with the latest agricultural news, policy changes, market trends, and technological innovations affecting the farming industry." %}<'),
    ('>Read More<', '>{% trans "Read More" %}<'),
    ('>Join the Farmer Community<', '>{% trans "Join the Farmer Community" %}<'),
    ('>Connect with other farmers, ask questions, share knowledge, and learn from experienced agricultural professionals in our vibrant community.<', '>{% trans "Connect with other farmers, ask questions, share knowledge, and learn from experienced agricultural professionals in our vibrant community." %}<'),
    ('>Join Forum<', '>{% trans "Join Forum" %}<'),
    ('>About Kisan Connect<', '>{% trans "About Kisan Connect" %}<'),
    ('>Empowering farmers with information, opportunities, and a connected farming community.<', '>{% trans "Empowering farmers with information, opportunities, and a connected farming community." %}<'),
    ('>Who We Are<', '>{% trans "Who We Are" %}<'),
    ('>Kisan Connect is a one-stop digital platform designed to empower farmers by providing easy access to government schemes, expert farming advice, a marketplace for agricultural products, community discussions, and the latest farming news.<', '>{% trans "Kisan Connect is a one-stop digital platform designed to empower farmers by providing easy access to government schemes, expert farming advice, a marketplace for agricultural products, community discussions, and the latest farming news." %}<'),
    ('>We bridge traditional farming practices with modern technology, ensuring farmers have all the resources they need to grow sustainably and profitably.<', '>{% trans "We bridge traditional farming practices with modern technology, ensuring farmers have all the resources they need to grow sustainably and profitably." %}<'),
    ('>Our Mission<', '>{% trans "Our Mission" %}<'),
    ('>To empower farmers with digital tools, transparent pricing, and direct market access. Reducing middlemen and creating opportunities for higher profits and sustainable growth.<', '>{% trans "To empower farmers with digital tools, transparent pricing, and direct market access. Reducing middlemen and creating opportunities for higher profits and sustainable growth." %}<'),
    ('>Our Vision<', '>{% trans "Our Vision" %}<'),
    ('>A connected farming ecosystem where every farmer has equal access to modern resources, buyers, and suppliers, ensuring prosperity for generations to come.<', '>{% trans "A connected farming ecosystem where every farmer has equal access to modern resources, buyers, and suppliers, ensuring prosperity for generations to come." %}<'),
    ('>Customer Reviews<', '>{% trans "Customer Reviews" %}<'),
    ('>See what our farmers are saying<', '>{% trans "See what our farmers are saying" %}<'),
    ('>Write Review<', '>{% trans "Write Review" %}<'),
    ('>Total Reviews<', '>{% trans "Total Reviews" %}<'),
    ('>Quality<', '>{% trans "Quality" %}<'),
    ('>Delivery<', '>{% trans "Delivery" %}<'),
    ('>Support<', '>{% trans "Support" %}<'),
    ('>Location<', '>{% trans "Location" %}<'),
    ('>Stay Updated with the Latest Agricultural Products<', '>{% trans "Stay Updated with the Latest Agricultural Products" %}<'),
    ('>Get exclusive offers, expert farming tips, and seasonal advice delivered straight to your inbox. Don\'t miss out on improving your yield!<', '>{% trans "Get exclusive offers, expert farming tips, and seasonal advice delivered straight to your inbox. Don\'t miss out on improving your yield!" %}<'),
    ('>Join 10,000+ happy farmers who trust us!<', '>{% trans "Join 10,000+ happy farmers who trust us!" %}<'),
    ('>100% spam-free. Unsubscribe anytime.<', '>{% trans "100% spam-free. Unsubscribe anytime." %}<'),
    ('placeholder="Enter your email"', 'placeholder="{% trans \'Enter your email\' %}"'),
    ('>Subscribe<', '>{% trans "Subscribe" %}<'),
    ('>We respect your privacy and never share your information.<', '>{% trans "We respect your privacy and never share your information." %}<'),
    ('>Fast Delivery<', '>{% trans "Fast Delivery" %}<'),
    ('>Trusted Quality<', '>{% trans "Trusted Quality" %}<'),
    ('>Expert Support<', '>{% trans "Expert Support" %}<'),
    ('>Best Offers<', '>{% trans "Best Offers" %}<'),
]

# Apply translations
for old, new in translations:
    if old in content and new not in content:
        content = content.replace(old, new, 1)
        print(f"[OK] Translated: {len(old)} chars")

# Write back
with open('app/templates/app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] All translations added!")
print("Restart server: python manage.py runserver")
