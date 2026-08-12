import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Notification, Profile


def generate_qr_for_member(member):
    qr_data = f"MEMBER-{member.id}"
    img = qrcode.make(qr_data)

    buffer = BytesIO()
    img.save(buffer, format='PNG')

    filename = f"qr_{member.id}.png"
    member.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)


def notify(user, message, link=''):
    if user:
        Notification.objects.create(user=user, message=message, link=link)


def notify_admins(message, link=''):
    admin_profiles = Profile.objects.filter(role='admin').select_related('user')
    for profile in admin_profiles:
        Notification.objects.create(user=profile.user, message=message, link=link)