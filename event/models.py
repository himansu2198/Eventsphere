from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('participant', 'Participant'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class EventCategory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    priority = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('maintenance', 'Under Maintenance'),
    ]

    TYPE_CHOICES = [
        ('auditorium', 'Auditorium'),
        ('classroom', 'Classroom'),
        ('lab', 'Lab'),
        ('ground', 'Ground/Field'),
        ('hall', 'Seminar Hall'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    location = models.CharField(max_length=255, blank=True)
    capacity = models.IntegerField(default=0)
    venue_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)

    has_projector = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    has_sound_system = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_stage = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def facility_list(self):
        items = []
        if self.has_projector: items.append('Projector')
        if self.has_ac: items.append('AC')
        if self.has_sound_system: items.append('Sound System')
        if self.has_wifi: items.append('Wi-Fi')
        if self.has_stage: items.append('Stage')
        return items

    @property
    def upcoming_booking(self):
        return self.events_booked.filter(status__in=['active', 'upcoming']).order_by('start_date').first()


class Event(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
    ]

    SCHEDULED_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('postponed', 'Postponed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    description = models.TextField(blank=True)

    priority = models.IntegerField(default=1)
    scheduled_status = models.CharField(max_length=20, choices=SCHEDULED_STATUS_CHOICES, default='scheduled')
    venue = models.CharField(max_length=200, blank=True)
    venue_ref = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_booked', help_text="Optional: link to a registered Venue for capacity/availability tracking.")
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255, blank=True)

    points = models.IntegerField(default=0)
    max_attendees = models.IntegerField(default=0)
    registration_deadline = models.DateTimeField(null=True, blank=True, help_text="Registrations close after this date/time. Leave blank for no deadline.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    session_name = models.CharField(max_length=150, blank=True)
    speaker_name = models.CharField(max_length=150, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    venue_name = models.CharField(max_length=200, blank=True)

    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sponsors = models.CharField(max_length=300, blank=True, help_text="Comma-separated sponsor names")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('status_changed', 'Status Changed'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.event.name} - {self.action} - {self.timestamp}"


class EventUserWish(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='wishes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_wishes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


class EventMember(models.Model):
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('general', 'General Attendee'),
        ('vip', 'VIP'),
        ('guest', 'Guest'),
        ('speaker', 'Speaker'),
        ('sponsor', 'Sponsor'),
        ('volunteer', 'Volunteer'),
        ('organizer', 'Organizer'),
        ('judge', 'Judge'),
    ]

    # Roles that require attendance tracking and therefore need a QR ticket.
    ATTENDANCE_ROLES = ['participant', 'general', 'volunteer']

    REGISTRATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled', 'Cancelled'),
    ]

    # Statuses allowed to physically check in at the event.
    ELIGIBLE_CHECKIN_STATUSES = ['confirmed']

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrations')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='general')
    department = models.CharField(max_length=100, blank=True, help_text="e.g. Computer Science, Mechanical Engineering")
    academic_year = models.CharField(max_length=20, blank=True, help_text="e.g. 1st Year, 2nd Year, Final Year")
    registration_status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES, default='confirmed')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.name}"

    @property
    def requires_qr(self):
        return self.role in self.ATTENDANCE_ROLES

    @property
    def is_eligible_for_checkin(self):
        return self.registration_status in self.ELIGIBLE_CHECKIN_STATUSES


class UserMark(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]

    member = models.ForeignKey(EventMember, on_delete=models.CASCADE, related_name='marks')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_at = models.DateTimeField(auto_now_add=True)
    checked_out_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.name} - {self.status}"


class Vendor(models.Model):
    SERVICE_CHOICES = [
        ('catering', 'Catering'),
        ('logistics', 'Logistics'),
        ('equipment', 'Equipment Rental'),
        ('decor', 'Decoration'),
        ('security', 'Security'),
        ('other', 'Other'),
    ]

    CONTRACT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='other')
    contract_status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, default='pending')
    contract_document = models.FileField(upload_to='vendor_contracts/', blank=True, null=True, help_text="Upload signed contract/agreement (PDF, DOC, etc.)")
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendors')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:40]}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('venue', 'Venue Booking'),
        ('catering', 'Catering'),
        ('staffing', 'Staffing'),
        ('marketing', 'Marketing'),
        ('logistics', 'Logistics'),
        ('equipment', 'Equipment Procurement'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    HIGH_VALUE_THRESHOLD = 10000

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.CharField(max_length=255, blank=True)
    projected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoice = models.FileField(upload_to='expense_invoices/', blank=True, null=True, help_text="Upload invoice/receipt (PDF, image, etc.)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_expenses')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_high_value(self):
        return self.projected_amount >= self.HIGH_VALUE_THRESHOLD

    def __str__(self):
        return f"{self.event.name} - {self.get_category_display()} - ₹{self.projected_amount}"


class Sponsor(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='sponsor_logos/', blank=True, null=True)
    contact_person = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SponsorshipRevenue(models.Model):
    STATUS_CHOICES = [
        ('pledged', 'Pledged'),
        ('received', 'Received'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sponsorship_revenues')
    sponsor_name = models.CharField(max_length=150)
    sponsor_ref = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True, related_name='sponsorships', help_text="Optional: link to a registered Sponsor for reusable profile/logo.")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pledged')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor_name} - ₹{self.amount} ({self.event.name})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_messages')
    is_reviewed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('av_equipment', 'AV Equipment'),
        ('furniture', 'Furniture'),
        ('signage', 'Signage & Banners'),
        ('catering_supplies', 'Catering Supplies'),
        ('safety', 'Safety Equipment'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    total_quantity = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def allocated_quantity(self):
        return self.allocations.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def available_quantity(self):
        return self.total_quantity - self.allocated_quantity


class ResourceAllocation(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='resource_allocations')
    quantity = models.IntegerField(default=1)
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-allocated_at']

    def __str__(self):
        return f"{self.quantity}x {self.resource.name} -> {self.event.name}"