from django.http import JsonResponse
from supabase import create_client
from django.conf import settings

def keep_alive(request):
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        supabase.table('media').select('id').limit(1).execute()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)