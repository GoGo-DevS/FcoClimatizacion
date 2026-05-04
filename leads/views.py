from urllib.parse import quote
from django.conf import settings
from django.shortcuts import redirect


def quote_request(request):
    message = request.GET.get("msg") or "Hola! Quiero cotizar servicio de climatización."
    phone = settings.WHATSAPP_PHONE.replace("+", "").replace(" ", "")
    return redirect(f"https://wa.me/{phone}?text={quote(message)}")

def quote_success(request):
    return quote_request(request)
