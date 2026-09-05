import random
import string
import io
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
import qrcode

from .models import Notification


def generate_ticket_code():
    """
    Generates a unique, human-readable ticket code, e.g. MEMBER-7X92K4.
    Guaranteed unique across all EventMember registrations — checks the
    database on every attempt and retries on collision. Never hardcoded.
    """
    from .models import EventMember
    while True:
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        code = f"MEMBER-{random_part}"
        if not EventMember.objects.filter(ticket_code=code).exists():
            return code


def generate_qr_for_member(member):
    """
    Assigns a unique ticket code to the member (if not already set) and
    generates a QR code image that encodes that exact ticket code. Each
    QR code is unique per registration — never reused across participants
    or events, since generate_ticket_code() guarantees uniqueness against
    the database.
    """
    if not member.ticket_code:
        member.ticket_code = generate_ticket_code()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(member.ticket_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    filename = f"{member.ticket_code}.png"
    member.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
    member.save()


def notify(user, message, link=''):
    Notification.objects.create(user=user, message=message, link=link)


def notify_admins(message, link=''):
    admin_users = User.objects.filter(profile__role='admin')
    for admin in admin_users:
        Notification.objects.create(user=admin, message=message, link=link)