# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.cache import cache
import json
import requests
import google.generativeai as genai
from deep_translator import GoogleTranslator
from .models import Product, Customer, Cart, OrderPlaced, Payment, CommunityGroup
from .forms import CustomerProfileForm, CustomerRegistrationForm, CommunityGroupForm
from .utils import STATE_CHOICES, DISTRICTS_BY_STATE

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)


# =======================
# Basic Views
# =======================
def home(request):
    # Home page is public - no login required
    return render(request, "app/index.html")


@login_required(login_url=reverse_lazy("app:login"))
def home_page(request):
    return render(request, "app/home.html")


@login_required(login_url=reverse_lazy("app:login"))
def about(request):
    return render(request, "app/about.html")


@login_required(login_url=reverse_lazy("app:login"))
def contact(request):
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
    products = Product.objects.all()[:12]  # Show first 12 products
    return render(request, "app/marketplace.html", {"products": products})


@login_required(login_url=reverse_lazy("app:login"))
def support(request):
    return render(request, "app/support.html")


@login_required(login_url=reverse_lazy("app:login"))
def prediction(request):
    return render(request, "app/prediction.html")


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
        return redirect("app:marketplace")
        
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
                return redirect("app:marketplace")
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
    city = city.strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    return response.json()


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
        city = request.POST.get("city", "").strip()
        if not city:
            context["error"] = "Please enter a city name."
        else:
            city_key = city.lower()  # normalize for cache key
            cache_key = f"farming_advice_{city_key}"
            cached_data = cache.get(cache_key)

            if cached_data:
                # Use cached results
                (
                    description,
                    temp,
                    feels_like,
                    humidity,
                    pressure,
                    wind_speed,
                    advice_en,
                    advice_mr,
                ) = cached_data
            else:
                # Fetch weather
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

                    # ======= Short, Point-Based Prompt =======
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
                        advice_mr = advice_en  # fallback

                    # Format advice to HTML
                    advice_en = format_advice(advice_en)
                    advice_mr = format_advice(advice_mr)

                    # Save everything in cache for 30 minutes
                    cache.set(
                        cache_key,
                        (description, temp, feels_like, humidity, pressure, wind_speed, advice_en, advice_mr),
                        1800,  # 30 minutes
                    )

    context.update(
        {
            "city": city,
            "description": description,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "advice_en": advice_en,
            "advice_mr": advice_mr,
        }
    )

    return render(request, "app/advice.html", context)


# =======================
# Category Views
# =======================
class CategoryView(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:login")
    
    def get(self, request, val):
        products = Product.objects.filter(category__iexact=val)
        titles = products.values_list("title", flat=True).distinct()
        return render(request, "app/category.html", {"product": products, "title": titles, "val": val})


class CategoryTitle(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:login")
    
    def get(self, request, val):
        products = Product.objects.filter(category__iexact=val)
        title_counts = products.values("title").annotate(total=Count("title"))
        return render(request, "app/category.html", {"product": products, "title": title_counts, "val": val})


# =======================
# Product Detail View
# =======================
class ProductDetailView(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:login")
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, "app/productdetail.html", {"product": product})


# =======================
# Customer Registration
# =======================
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Congratulations! User registered successfully.")
            return redirect("app:customerregistration")
        else:
            messages.warning(request, "⚠️ Invalid input data, please check again.")
            return render(request, "app/customerregistration.html", {"form": form})


# =======================
# Profile View
# =======================
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", {"form": form, "active": "btn-primary"})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)  # don't save yet
            customer.user = request.user  # assign logged-in user
            customer.save()  # now save
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, "app/profile.html", {"form": form, "active": "btn-primary"})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", locals())


class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "app/updateAddress.html", {"form": form, "pk": pk})

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            for field in ["name", "locality", "city", "mobile", "state", "zipcode"]:
                setattr(add, field, form.cleaned_data[field])
            add.save()
            messages.success(request, "✅ Address Updated Successfully")
        else:
            messages.warning(request, "⚠️ Invalid Input Data")
        return redirect("app:address")


# =======================
# Cart & Order Views
# =======================
@login_required(login_url=reverse_lazy("app:signin"))
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("app:showcart")


@login_required(login_url=reverse_lazy("app:signin"))
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart)
    totalamount = amount + 40 if cart else 0
    return render(request, "app/addtocart.html", locals())


class checkout(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:signin")

    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = sum(p.quantity * p.product.discounted_price for p in cart_items)
        totalamount = famount + 40 if cart_items else 0
        return render(request, "app/checkout.html", locals())


@login_required(login_url=reverse_lazy("app:signin"))
def place_order(request):
    if request.method == "POST":
        user = request.user
        custid = request.POST.get("custid")
        totalamount = request.POST.get("totalamount")

        if not custid:  # If no address is selected
            messages.error(request, "⚠️ Please select a shipping address.")
            return redirect("app:checkout")

        customer = get_object_or_404(Customer, id=custid)

        # Create a Payment entry for COD
        payment = Payment.objects.create(user=user, amount=totalamount, paid=False, razorpay_payment_status="COD")

        # Move cart items into OrderPlaced
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                payment=payment,
                status="Pending",
            )

        # Clear cart after order is placed
        cart_items.delete()

        messages.success(request, "🎉 Your order has been placed successfully with Cash on Delivery!")
        return redirect("app:order_success")

    # If not POST, go back to checkout
    return redirect("app:checkout")


@login_required(login_url=reverse_lazy("app:signin"))
def order_success(request):
    return render(request, "app/order_success.html")


# =======================
# Ajax Cart Update (protected)
# =======================
@login_required(login_url=reverse_lazy("app:signin"))
def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)
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


# =======================
# Profile & Addresses
# =======================
class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy("app:signin")

    def get(self, request):
        addresses = Customer.objects.filter(user=request.user)  # all addresses for user
        # if you want to edit one specific profile (e.g. first address)
        profile = addresses.first()
        form = CustomerProfileForm(instance=profile)
        return render(
            request,
            "app/profile.html",
            {"form": form, "profile": profile, "addresses": addresses, "user": request.user},
        )

    def post(self, request):
        addresses = Customer.objects.filter(user=request.user)
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()

        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("app:profile")
        else:
            messages.error(request, "Please fix the errors below.")
        return render(
            request,
            "app/profile.html",
            {"form": form, "profile": profile, "addresses": addresses, "user": request.user},
        )


@login_required(login_url=reverse_lazy("app:signin"))
def addresses(request):
    addresses = Customer.objects.filter(user=request.user)
    return render(request, "app/addresses.html", {"addresses": addresses})


@login_required(login_url=reverse_lazy("app:signin"))
def update_address(request, pk):
    address = get_object_or_404(Customer, pk=pk, user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("app:addresses")
    else:
        form = CustomerProfileForm(instance=address)
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
    # Get a list of states from the utility file to populate the dropdown
    states = sorted([state[0] for state in STATE_CHOICES])
    groups = CommunityGroup.objects.filter(is_approved=True).order_by('-created_at')
    
    # We can create a form instance here to pass to the template for rendering fields
    form = CommunityGroupForm()

    context = {
        "states": states,
        "groups": groups,
        "form": form,
    }
    return render(request, "app/forum.html", context)

@login_required(login_url=reverse_lazy("app:login"))
def get_districts(request):
    """
    AJAX view to return districts for a selected state.
    """
    state = request.GET.get('state')
    districts = DISTRICTS_BY_STATE.get(state, [])
    return JsonResponse({'districts': districts})

@login_required(login_url=reverse_lazy("app:login"))
def add_group(request):
    """
    Handles the AJAX form submission for adding a new group.
    """
    if request.method == 'POST':
        # The 'form.is_valid()' check is crucial here
        form = CommunityGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.is_approved = False  # needs admin approval
            group.save()
            return JsonResponse({
                'success': True,
                'message': '✅ Group submitted! It will be visible after admin approval.'
            })
        else:
            # Return form errors in the JSON response
            errors = form.errors.as_json()
            return JsonResponse({
                'success': False,
                'message': 'Invalid form data.',
                'errors': json.loads(errors),
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


def get_farming_news():
    """
    Fetches farming news from Newsdata.io API with the corrected URL.
    """
    # Replace this URL with the one found in your Newsdata.io dashboard
    # For example, for the free tier, it might be:
    url = "https://newsdata.io/api/1/latest"
    
    # Your other parameters remain the same
    params = {
        "apikey": settings.NEWSDATA_API_KEY,
        "q": "farming OR agriculture OR crops OR farmers",
        "language": "en",
        "country": "in",
        "size": 10,  # Add this parameter to request 30 articles
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching farming news: {e}")
        return []

# (The rest of your code...)

@login_required(login_url=reverse_lazy("app:login"))
def news(request):
    """
    Renders the news page with articles fetched from the API.
    """
    articles = get_farming_news()
    return render(request, "app/news.html", {"articles": articles})