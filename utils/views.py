import requests
from django.http import JsonResponse
from django.conf import settings

def keep_alive(request):
    try:
        url = f"{settings.SUPABASE_URL}/rest/v1/media?select=id&limit=1"
        headers = {
            "apikey": settings.SUPABASE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_KEY}",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)