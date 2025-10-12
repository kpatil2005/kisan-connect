# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.cache import cache
from django.core.mail import send_mail
import json
import requests
import google.generativeai as genai
from deep_translator import GoogleTranslator
import threading
from .models import Product, Customer, Cart, OrderPlaced, Payment, CommunityGroup
from .forms import CustomerProfileForm, CustomerRegistrationForm, CommunityGroupForm
from .utils import STATE_CHOICES, DISTRICTS_BY_STATE
from .ml_predict import predict_disease as ml_predict

# Configure Gemini AI
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    import logging
    logging.error(f"Gemini API configuration error: {e}")


# =======================
# Basic Views
# =======================
def home(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            rating = request.POST.get('rating')
            review_text = request.POST.get('review')
            if rating and review_text:
                from .models import Review
                Review.objects.create(user=request.user, rating=rating, review_text=review_text)
                messages.success(request, "✅ Thank you for your review!")
        except:
            pass
        return redirect('home')
    
    from .models import Review
    reviews = Review.objects.filter(is_approved=True)[:6]
    return render(request, "app/index.html", {'reviews': reviews})


@login_required(login_url=reverse_lazy("app:login"))
def home_page(request):
    context = {'products': []}
    try:
        from .models import Product
        products = Product.objects.all()[:8]
        context['products'] = products
    except Exception as e:
        # Log error but don't crash
        print(f"Error loading products: {e}")
        context['products'] = []
    
    return render(request, "app/home.html", context)


@login_required(login_url=reverse_lazy("app:login"))
def about(request):
    return render(request, "app/about.html")


@login_required(login_url=reverse_lazy("app:login"))
def contact(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            message = request.POST.get('message', '').strip()
            
            if name and email and message:
                def send_email():
                    try:
                        import sib_api_v3_sdk
                        from django.template.loader import render_to_string
                        import os
                        
                        configuration = sib_api_v3_sdk.Configuration()
                        configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY', '')
                        
                        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                        
                        html_content = render_to_string('app/contact_thank_you_email.html', {
                            'user_name': name,
                            'user_message': message,
                            'site_url': f"{request.scheme}://{request.get_host()}"
                        })
                        
                        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                            to=[{"email": email, "name": name}],
                            sender={"name": "Kisan Connect", "email": "kisansetu1@gmail.com"},
                            subject="🙏 Thank You for Contacting Kisan Connect",
                            html_content=html_content
                        )
                        api_instance.send_transac_email(send_smtp_email)
                    except:
                        pass
                
                threading.Thread(target=send_email).start()
                messages.success(request, "✅ Thank you! Your message has been sent. We'll get back to you soon.")
            else:
                messages.error(request, "Please fill in all fields")
        except Exception as e:
            messages.error(request, "Failed to send message. Please try again.")
        return redirect('app:contact')
    return render(request, "app/contact.html")


@login_required(login_url=reverse_lazy("app:login"))
def weather(request):
    return render(request, "app/weather.html")


@login_required(login_url=reverse_lazy("app:login"))
def crops(request):
    return render(request, "app/crops.html")


@login_required(login_url=reverse_lazy("app:login"))
def fertilizers(request):
    return render(request, "app/fertilizers.html")


@login_required(login_url=reverse_lazy("app:login"))
def marketplace(request):
    context = {'products': []}
    try:
        from .models import Product
        products = Product.objects.all()[:12]
        context['products'] = products
    except Exception as e:
        print(f"Error loading products: {e}")
        context['products'] = []
    
    return render(request, "app/home.html", context)


@login_required(login_url=reverse_lazy("app:login"))
def support(request):
    return render(request, "app/support.html")


@login_required(login_url=reverse_lazy("app:login"))
def search(request):
    try:
        query = request.GET.get('q', '').strip()
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        category = request.GET.get('category', '')
        sort = request.GET.get('sort', '')
        
        products = Product.objects.all()
        
        if query:
            from django.db.models import Q
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(composition__icontains=query) |
                Q(prodapp__icontains=query)
            )
        
        if min_price:
            try:
                products = products.filter(discounted_price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                products = products.filter(discounted_price__lte=float(max_price))
            except ValueError:
                pass
        
        if category:
            products = products.filter(category=category)
        
        if sort == 'price_low':
            products = products.order_by('discounted_price')
        elif sort == 'price_high':
            products = products.order_by('-discounted_price')
        elif sort == 'name':
            products = products.order_by('title')
        
        context = {
            'products': products,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'category': category,
            'sort': sort,
        }
    except Exception as e:
        messages.error(request, "Error performing search")
        context = {'products': [], 'query': '', 'min_price': '', 'max_price': '', 'category': '', 'sort': ''}
    return render(request, "app/search.html", context)


@login_required(login_url=reverse_lazy("app:login"))
def prediction(request):
    return render(request, "app/prediction.html")


@login_required(login_url=reverse_lazy("app:login"))
def disease_detection(request):
    """Render disease prediction page"""
    return render(request, 'app/disease_prediction.html')


@login_required(login_url=reverse_lazy("app:login"))
def predict_disease(request):
    """API endpoint for disease prediction"""
    if request.method == "POST" and request.FILES.get('image'):
        try:
            import os
            
            image = request.FILES['image']
            
            # Save temporarily
            temp_dir = 'media/temp'
            os.makedirs(temp_dir, exist_ok=True)
            image_path = os.path.join(temp_dir, image.name)
            
            with open(image_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            
            # Predict
            result = ml_predict(image_path)
            
            # Clean up
            try:
                os.remove(image_path)
            except:
                pass
            
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url=reverse_lazy("app:login"))
def weather_disease_alert(request):
    """Get weather-based disease risk alert"""
    try:
        city = 'Mumbai'
        weather = get_weather(city)  # Use existing weather function
        
        if weather.get("cod") != 200:
            return JsonResponse({
                'alert': True,
                'risk': 'Medium',
                'weather': 'Weather data unavailable',
                'preventive_measures': [
                    'Monitor plants daily for disease symptoms',
                    'Maintain good field hygiene',
                    'Apply preventive neem oil spray'
                ],
                'city': city
            })
        
        temp = weather['main']['temp']
        humidity = weather['main']['humidity']
        description = weather['weather'][0]['description']
        
        # Disease risk prediction logic
        risk = 'Low'
        measures = []
        
        if humidity > 80:
            risk = 'High'
            measures = [
                'High humidity detected - fungal diseases likely',
                'Apply fungicide preventively',
                'Ensure proper air circulation',
                'Avoid overhead watering'
            ]
        elif humidity > 60 and temp > 25:
            risk = 'Medium'
            measures = [
                'Moderate conditions for disease spread',
                'Monitor plants daily for symptoms',
                'Apply neem oil spray',
                'Remove infected leaves immediately'
            ]
        elif 'rain' in description.lower():
            risk = 'High'
            measures = [
                'Rainy conditions increase disease risk',
                'Avoid working in wet fields',
                'Apply copper-based fungicide',
                'Improve drainage in fields'
            ]
        else:
            measures = [
                'Weather conditions are favorable',
                'Continue regular monitoring',
                'Maintain good field hygiene'
            ]
        
        return JsonResponse({
            'alert': True,
            'risk': risk,
            'weather': f"{description.title()}, {temp}°C, {humidity}% humidity",
            'preventive_measures': measures,
            'city': city
        })
        
    except Exception as e:
        return JsonResponse({
            'alert': True,
            'risk': 'Medium',
            'weather': 'Weather monitoring active',
            'preventive_measures': [
                'Monitor plants daily for disease symptoms',
                'Maintain good field hygiene',
                'Apply preventive neem oil spray'
            ],
            'city': 'Your Area'
        })


@login_required(login_url=reverse_lazy("app:login"))
def download_disease_pdf(request):
    """Generate and download PDF report for disease detection"""
    if request.method == "POST":
        try:
            from django.http import HttpResponse
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            import json
            import base64
            from io import BytesIO
            from datetime import datetime
            
            data = json.loads(request.body)
            result = data.get('result', {})
            image_data = data.get('image', '')
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="plant-disease-report-{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'
            
            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#2e7d32'), alignment=TA_CENTER, spaceAfter=30)
            elements.append(Paragraph('Plant Disease Detection Report', title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Image
            if image_data and 'base64,' in image_data:
                try:
                    img_data = base64.b64decode(image_data.split('base64,')[1])
                    img = RLImage(BytesIO(img_data), width=3*inch, height=2.5*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 0.3*inch))
                except:
                    pass
            
            # Results Table
            data_table = [
                ['Disease:', result.get('disease', 'N/A')],
                ['Plant:', result.get('plant', 'N/A')],
                ['Confidence:', f"{result.get('confidence', 0)}%"],
                ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            table = Table(data_table, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Treatment Recommendations
            elements.append(Paragraph('Treatment Recommendations:', styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            for i, rec in enumerate(result.get('recommendations', []), 1):
                elements.append(Paragraph(f"{i}. {rec}", styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
            
            # Footer
            elements.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, textColor=colors.grey, alignment=TA_CENTER)
            elements.append(Paragraph('Generated by Kisan Connect - AI-Powered Plant Disease Detection', footer_style))
            
            doc.build(elements)
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url=reverse_lazy("app:login"))
def capture_and_predict(request):
    return render(request, "app/capture_and_predict.html")


@login_required(login_url=reverse_lazy("app:login"))
def advice_page(request):
    return render(request, "app/advice.html")


# =======================
# Signin (authenticate and respect ?next=)
# =======================
def signin(request):
    # If user is already authenticated, redirect them
    if request.user.is_authenticated:
        return redirect("app:schemes")
        
    if request.method == "POST":
        username = request.POST.get("username") or request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Check for next URL in session first, then GET/POST params
                next_url = request.session.get('next') or request.GET.get("next") or request.POST.get("next")
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
                ):
                    # Clear the session next URL
                    if 'next' in request.session:
                        del request.session['next']
                    return redirect(next_url)
                return redirect("app:schemes")
            else:
                messages.error(request, "Invalid username or password.")
        except Exception as e:
            messages.error(request, f"Login failed: {str(e)}")
    
    # Pass the next URL to the template for the form
    next_url = request.session.get('next') or request.GET.get('next', '')
    return render(request, "app/login.html", {'next': next_url})


# =======================
# Helper functions: weather + format advice
# =======================
def get_weather(city):
    """Fetch weather from OpenWeather API (case-insensitive)"""
    try:
        city = city.strip()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"cod": 500, "message": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"cod": 500, "message": str(e)}
    except Exception as e:
        return {"cod": 500, "message": "Weather service unavailable"}


def format_advice(advice_text):
    """Convert AI bullet points to HTML list with bold headings and proper alignment."""
    lines = advice_text.split("\n")
    html = "<ul style='padding-left:20px; line-height:1.6;'>"
    for line in lines:
        if line.strip():
            # Look for '**Heading:**' style
            if "**" in line:
                parts = line.split("**")
                if len(parts) >= 3:
                    heading = parts[1].strip()
                    content = parts[2].replace(":", "").strip()
                    html += f"<li><strong>{heading}:</strong> {content}</li>"
                else:
                    html += f"<li>{line}</li>"
            else:
                html += f"<li>{line}</li>"
    html += "</ul>"
    return html


# =======================
# Farming advice view (with cache)
# =======================
@login_required(login_url=reverse_lazy("app:signin"))
def farming_advice(request):
    """Render form + weather results + advice with caching for faster repeat access."""
    context = {}
    advice_en = ""
    advice_mr = ""
    city = ""
    description = temp = feels_like = humidity = pressure = wind_speed = None

    if request.method == "POST":
        try:
            city = request.POST.get("city", "").strip()
            if not city:
                context["error"] = "Please enter a city name."
            else:
                city_key = city.lower()
                cache_key = f"farming_advice_{city_key}"
                cached_data = cache.get(cache_key)

                if cached_data:
                    (description, temp, feels_like, humidity, pressure, wind_speed, advice_en, advice_mr) = cached_data
                else:
                    weather = get_weather(city)

                    if weather.get("cod") != 200:
                        context["error"] = f"❌ Could not fetch weather for {city}"
                    else:
                        description = weather["weather"][0]["description"]
                        temp = weather["main"]["temp"]
                        feels_like = weather["main"]["feels_like"]
                        humidity = weather["main"]["humidity"]
                        pressure = weather["main"]["pressure"]
                        wind_speed = weather["wind"]["speed"]

                        prompt = f"""
                        You are an agricultural expert. The weather in {city} today is:
                        - Condition: {description}
                        - Temperature: {temp}°C (feels like {feels_like}°C)
                        - Humidity: {humidity}%
                        - Pressure: {pressure} hPa
                        - Wind Speed: {wind_speed} m/s

                        Provide **short and actionable farming advice** in bullet points.
                        Each point should be 1–2 sentences.
                        Output only the points, no long paragraphs.
                        Example:
                        1. Tip heading in bold: short advice.
                        """

                        try:
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            response = model.generate_content(prompt)
                            advice_en = response.text.strip()
                        except Exception:
                            advice_en = (
                                "1. 🌱 Irrigation: Water crops early morning or late evening.\n"
                                "2. 🌿 Fertilizer: Apply only as needed.\n"
                                "3. 🐞 Pests: Check crops daily for insects.\n"
                                "4. 🌾 Harvest: Harvest on time to avoid loss.\n"
                                "5. 🏡 Soil: Add compost for healthy soil.\n"
                                "6. ☔ Weather: Protect crops from heavy rain.\n"
                                "7. 🧹 Hygiene: Clean tools to prevent disease."
                            )

                        try:
                            advice_mr = GoogleTranslator(source="auto", target="mr").translate(advice_en)
                        except Exception:
                            advice_mr = advice_en

                        advice_en = format_advice(advice_en)
                        advice_mr = format_advice(advice_mr)

                        cache.set(cache_key, (description, temp, feels_like, humidity, pressure, wind_speed, advice_en, advice_mr), 1800)
        except Exception as e:
            context["error"] = "Unable to fetch farming advice. Please try again."

    context.update({
        "city": city,
        "description": description,
        "temp": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "advice_en": advice_en,
        "advice_mr": advice_mr,
    })

    return render(request, "app/advice.html", context)


# =======================
# Category Views
# =======================
class CategoryView(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:login")
    
    def get(self, request, val):
        try:
            products = Product.objects.filter(category__iexact=val.upper())
            from .models import CATEGORY_CHOICES
            category_name = dict(CATEGORY_CHOICES).get(val.upper(), val)
            return render(request, "app/category.html", {
                "product": products,
                "val": val.upper(),
                "category_name": category_name
            })
        except Exception as e:
            messages.error(request, "Error loading category")
            return redirect("app:schemes")


class CategoryTitle(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:login")
    
    def get(self, request, val):
        try:
            products = Product.objects.filter(category__iexact=val)
            title_counts = products.values("title").annotate(total=Count("title"))
            return render(request, "app/category.html", {"product": products, "title": title_counts, "val": val})
        except Exception as e:
            messages.error(request, "Error loading category")
            return redirect("app:schemes")


# =======================
# Product Detail View
# =======================
class ProductDetailView(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:login")
    
    def get(self, request, pk):
        try:
            product = get_object_or_404(Product, pk=pk)
            return render(request, "app/productdetail.html", {"product": product})
        except Exception as e:
            messages.error(request, "Product not found")
            return redirect("app:schemes")


# =======================
# Customer Registration
# =======================
class CustomerRegistrationView(View):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                return redirect("app:schemes")
            form = CustomerRegistrationForm()
            return render(request, "app/customerregistration.html", {"form": form})
        except Exception as e:
            messages.error(request, "Error loading registration form")
            return redirect("app:home")

    def post(self, request):
        try:
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "🎉 Welcome! Your account has been created successfully.")
                return redirect("app:schemes")
            else:
                messages.warning(request, "⚠️ Invalid input data, please check again.")
                return render(request, "app/customerregistration.html", {"form": form})
        except Exception as e:
            messages.error(request, "Registration failed. Please try again.")
            return render(request, "app/customerregistration.html", {"form": CustomerRegistrationForm()})


# =======================
# Profile View
# =======================
class ProfileView(View):
    def get(self, request):
        try:
            form = CustomerProfileForm()
            return render(request, "app/profile.html", {"form": form, "active": "btn-primary"})
        except Exception as e:
            messages.error(request, "Error loading profile")
            return redirect("app:schemes")

    def post(self, request):
        try:
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.user = request.user
                customer.save()
                messages.success(request, "Profile updated successfully!")
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            messages.error(request, "Failed to update profile")
        return render(request, "app/profile.html", {"form": form, "active": "btn-primary"})


def address(request):
    try:
        add = Customer.objects.filter(user=request.user)
    except Exception as e:
        messages.error(request, "Error loading addresses")
        add = []
    return render(request, "app/address.html", locals())


class UpdateAddress(View):
    def get(self, request, pk):
        try:
            add = Customer.objects.get(pk=pk)
            form = CustomerProfileForm(instance=add)
            return render(request, "app/updateAddress.html", {"form": form, "pk": pk})
        except Exception as e:
            messages.error(request, "Address not found")
            return redirect("app:address")

    def post(self, request, pk):
        try:
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                add = Customer.objects.get(pk=pk)
                for field in ["name", "locality", "city", "mobile", "state", "zipcode"]:
                    setattr(add, field, form.cleaned_data[field])
                add.save()
                messages.success(request, "✅ Address Updated Successfully")
            else:
                messages.warning(request, "⚠️ Invalid Input Data")
        except Exception as e:
            messages.error(request, "Failed to update address")
        return redirect("app:address")


# =======================
# Cart & Order Views
# =======================
@login_required(login_url=reverse_lazy("app:signin"))
def add_to_cart(request):
    try:
        user = request.user
        product_id = request.GET.get("prod_id")
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, "Item added to cart!")
    except Exception as e:
        messages.error(request, "Failed to add item to cart")
    return redirect("app:showcart")


@login_required(login_url=reverse_lazy("app:signin"))
def show_cart(request):
    try:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40 if cart else 0
    except Exception as e:
        messages.error(request, "Error loading cart")
        cart = []
        amount = 0
        totalamount = 0
    return render(request, "app/addtocart.html", locals())


class checkout(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:signin")

    def get(self, request):
        try:
            user = request.user
            add = Customer.objects.filter(user=user)
            cart_items = Cart.objects.filter(user=user)
            famount = sum(p.quantity * p.product.discounted_price for p in cart_items)
            totalamount = famount + 40 if cart_items else 0
        except Exception as e:
            messages.error(request, "Error loading checkout")
            return redirect("app:showcart")
        return render(request, "app/checkout.html", locals())


@login_required(login_url=reverse_lazy("app:signin"))
def place_order(request):
    if request.method == "POST":
        try:
            user = request.user
            custid = request.POST.get("custid")
            totalamount = request.POST.get("totalamount")

            if not custid:
                messages.error(request, "⚠️ Please select a shipping address.")
                return redirect("app:checkout")

            customer = get_object_or_404(Customer, id=custid)
            payment = Payment.objects.create(user=user, amount=totalamount, paid=False, razorpay_payment_status="COD")

            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                messages.error(request, "Your cart is empty")
                return redirect("app:showcart")
            
            order_items = []
            for item in cart_items:
                order = OrderPlaced.objects.create(
                    user=user,
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment,
                    status="Pending",
                )
                order_items.append(f"{item.product.title} x {item.quantity} = ₹{item.product.discounted_price * item.quantity}")

            # Prepare email data before deleting cart
            items_html = ""
            subtotal = 0
            for item in cart_items:
                item_total = item.product.discounted_price * item.quantity
                subtotal += item_total
                items_html += f'<div style="padding:12px 0;border-bottom:1px solid #e0e0e0;"><strong style="color:#333;font-size:15px;">{item.product.title}</strong><br><span style="color:#666;font-size:13px;">Quantity: {item.quantity} × ₹{item.product.discounted_price} = ₹{item_total}</span></div>'
            
            cart_items.delete()

            # Send email via Brevo API
            def send_email():
                try:
                    import sib_api_v3_sdk
                    from django.template.loader import render_to_string
                    import os
                    
                    configuration = sib_api_v3_sdk.Configuration()
                    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY', '')
                    
                    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                    
                    html_content = render_to_string('app/order_confirmation_email.html', {
                        'customer_name': customer.name,
                        'order_items': items_html,
                        'subtotal': subtotal,
                        'total_amount': totalamount,
                        'locality': customer.locality,
                        'city': customer.city,
                        'state': customer.state,
                        'zipcode': customer.zipcode,
                        'mobile': customer.mobile,
                        'site_url': f"{request.scheme}://{request.get_host()}"
                    })
                    
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                        to=[{"email": user.email, "name": customer.name}],
                        sender={"name": "Kisan Connect", "email": "kisansetu1@gmail.com"},
                        subject="🎉 Order Confirmed - Kisan Connect",
                        html_content=html_content
                    )
                    api_instance.send_transac_email(send_smtp_email)
                except:
                    pass
            
            threading.Thread(target=send_email).start()

            messages.success(request, "🎉 Your order has been placed successfully with Cash on Delivery!")
            return redirect("app:order_success")
        except Exception as e:
            messages.error(request, "Failed to place order. Please try again.")
            return redirect("app:checkout")

    return redirect("app:checkout")


@login_required(login_url=reverse_lazy("app:signin"))
def order_success(request):
    return render(request, "app/order_success.html")


# =======================
# Ajax Cart Update (protected)
# =======================
@login_required(login_url=reverse_lazy("app:signin"))
def orders(request):
    try:
        orders = OrderPlaced.objects.filter(user=request.user)
    except Exception as e:
        messages.error(request, "Error loading orders")
        orders = []
    return render(request, "app/orders.html", locals())


@login_required(login_url=reverse_lazy("app:signin"))
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
            cart_item.quantity += 1
            cart_item.save()

            amount = sum(p.quantity * p.product.discounted_price for p in Cart.objects.filter(user=request.user))
            totalamount = amount + 40
            return JsonResponse({"quantity": cart_item.quantity, "amount": amount, "totalamount": totalamount})
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Failed to update cart"}, status=500)


@login_required(login_url=reverse_lazy("app:signin"))
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

            amount = sum(p.quantity * p.product.discounted_price for p in Cart.objects.filter(user=request.user))
            totalamount = amount + 40
            return JsonResponse({"quantity": cart_item.quantity, "amount": amount, "totalamount": totalamount})
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Failed to update cart"}, status=500)


@login_required(login_url=reverse_lazy("app:signin"))
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
            cart_item.delete()

            amount = sum(p.quantity * p.product.discounted_price for p in Cart.objects.filter(user=request.user))
            totalamount = amount + 40
            return JsonResponse({"amount": amount, "totalamount": totalamount})
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Failed to remove item"}, status=500)


# =======================
# Profile & Addresses
# =======================
class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:signin")

    def get(self, request):
        try:
            addresses = Customer.objects.filter(user=request.user)
            profile = addresses.first()
            form = CustomerProfileForm(instance=profile)
            return render(
                request,
                "app/profile.html",
                {"form": form, "profile": profile, "addresses": addresses, "user": request.user},
            )
        except Exception as e:
            messages.error(request, "Error loading profile")
            return redirect("app:schemes")

    def post(self, request):
        try:
            addresses = Customer.objects.filter(user=request.user)
            profile = addresses.first()
            form = CustomerProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile_obj = form.save(commit=False)
                profile_obj.user = request.user
                profile_obj.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("app:profile")
            else:
                messages.error(request, "Please fix the errors below.")
        except Exception as e:
            messages.error(request, "Failed to update profile")
            profile = None
            addresses = []
            form = CustomerProfileForm()
        return render(
            request,
            "app/profile.html",
            {"form": form, "profile": profile, "addresses": addresses, "user": request.user},
        )


@login_required(login_url=reverse_lazy("app:signin"))
def addresses(request):
    try:
        addresses = Customer.objects.filter(user=request.user)
    except Exception as e:
        messages.error(request, "Error loading addresses")
        addresses = []
    return render(request, "app/addresses.html", {"addresses": addresses})


@login_required(login_url=reverse_lazy("app:signin"))
def update_address(request, pk):
    try:
        address = get_object_or_404(Customer, pk=pk, user=request.user)
        if request.method == "POST":
            form = CustomerProfileForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
                messages.success(request, "Address updated successfully")
                return redirect("app:addresses")
            else:
                messages.error(request, "Invalid form data")
        else:
            form = CustomerProfileForm(instance=address)
    except Exception as e:
        messages.error(request, "Failed to update address")
        return redirect("app:addresses")
    return render(request, "app/updateAddress.html", {"form": form})


# Districts per state
DISTRICTS_BY_STATE = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Mangalore"],
    "Punjab": ["Amritsar", "Ludhiana", "Patiala"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi"],
}

@login_required(login_url=reverse_lazy("app:login"))
def forum(request):
    """
    Renders the community forum page with a list of groups and the
    'Add Group' form in a modal.
    """
    try:
        states = sorted([state[0] for state in STATE_CHOICES])
        groups = CommunityGroup.objects.filter(is_approved=True).order_by('-created_at')
        form = CommunityGroupForm()
        context = {
            "states": states,
            "groups": groups,
            "form": form,
        }
    except Exception as e:
        messages.error(request, "Error loading forum")
        context = {"states": [], "groups": [], "form": CommunityGroupForm()}
    return render(request, "app/forum.html", context)

@login_required(login_url=reverse_lazy("app:login"))
def get_districts(request):
    """
    AJAX view to return districts for a selected state.
    """
    try:
        state = request.GET.get('state')
        districts = DISTRICTS_BY_STATE.get(state, [])
        return JsonResponse({'districts': districts})
    except Exception as e:
        return JsonResponse({'districts': []}, status=500)

@login_required(login_url=reverse_lazy("app:login"))
def add_group(request):
    """
    Handles the AJAX form submission for adding a new group.
    """
    try:
        if request.method == 'POST':
            form = CommunityGroupForm(request.POST)
            if form.is_valid():
                group = form.save(commit=False)
                group.is_approved = False
                group.save()
                return JsonResponse({
                    'success': True,
                    'message': '✅ Group submitted! It will be visible after admin approval.'
                })
            else:
                errors = form.errors.as_json()
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid form data.',
                    'errors': json.loads(errors),
                })
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Server error occurred'}, status=500)


def get_farming_news():
    """
    Fetches farming news from Newsdata.io API with the corrected URL.
    """
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": settings.NEWSDATA_API_KEY,
        "q": "farming OR agriculture OR crops OR farmers",
        "language": "en",
        "country": "in",
        "size": 10,
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.Timeout:
        print("News API timeout")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching farming news: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# (The rest of your code...)

@login_required(login_url=reverse_lazy("app:login"))
def news(request):
    """
    Renders the news page with articles fetched from the API.
    """
    try:
        articles = get_farming_news()
    except Exception as e:
        articles = []
        messages.warning(request, "Unable to load news at this time")
    return render(request, "app/news.html", {"articles": articles})


@login_required(login_url=reverse_lazy("app:login"))
def subscribe_newsletter(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email', '').strip()
            if email:
                from .models import Newsletter
                Newsletter.objects.get_or_create(email=email)
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            return JsonResponse({'success': False, 'message': 'Please enter a valid email'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Subscription failed'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def send_newsletter_email(subject, message):
    """Send email to all active newsletter subscribers"""
    from .models import Newsletter
    import sib_api_v3_sdk
    import os
    
    subscribers = Newsletter.objects.filter(is_active=True)
    
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY', '')
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
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


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def send_newsletter_view(request):
    from .models import Newsletter
    import sib_api_v3_sdk
    import os
    
    subscriber_count = Newsletter.objects.filter(is_active=True).count()
    
    if request.method == "POST":
        email_type = request.POST.get('email_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        subscribers = Newsletter.objects.filter(is_active=True)
        
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY', '')
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        
        sent_count = 0
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
            except:
                pass
        
        messages.success(request, f"✅ Newsletter sent to {sent_count} subscribers!")
        return redirect('app:send_newsletter')
    
    return render(request, 'app/send_newsletter.html', {'subscriber_count': subscriber_count})
