from django.conf import settings

def site_settings(request):
    return {
        "WHATSAPP_PHONE": settings.WHATSAPP_PHONE,
        "WHATSAPP_PHONE_CLEAN": settings.WHATSAPP_PHONE.replace("+", "").replace(" ", ""),
    }
