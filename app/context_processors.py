# app/context_processors.py
from django.db.models import Sum
from .models import Cart

def cart_count(request):
    """
    Adds `totalitem` (sum of quantities in the user's cart) to every template.
    Shows 0 for anonymous users.
    """
    totalitem = 0
    user = getattr(request, "user", None)

    if user and user.is_authenticated:
        totalitem = (
            Cart.objects.filter(user=user).aggregate(total=Sum("quantity"))["total"] or 0
        )

    return {"totalitem": totalitem}
