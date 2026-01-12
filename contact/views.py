from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ContactSubmission


@csrf_exempt
@require_http_methods(["POST"])
def submit_contact_form(request):
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    if not all([first_name, last_name, email, subject, message]):
        return JsonResponse({'error': 'All fields are required.'}, status=400)

    full_name = f"{first_name} {last_name}"

    # Save to database
    ContactSubmission.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        subject=subject,
        message=message,
    )

    # Compose email
    email_subject = f"Contact Form: {subject}"
    email_body = (
        f"New message from your website contact form:\n\n"
        f"Name: {full_name}\n"
        f"Email: {email}\n"
        f"Subject: {subject}\n\n"
        f"Message:\n{message}"
    )

    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return JsonResponse({'message': 'Message sent and saved successfully.'})

    except Exception as e:
        return JsonResponse({'error': f'Failed to send email: {str(e)}'}, status=500)