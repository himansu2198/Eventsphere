from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from event import views
from event.api_views import CategoryListAPI, EventListAPI, EventDetailAPI, MemberListAPI, VendorListAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='login'),
    path('signup/', views.participant_signup, name='participant_signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-search/', views.global_admin_search, name='global_admin_search'),
    path('api/global-search/', views.global_search_api, name='global_search_api'),
    path('api/participant-search/', views.participant_search_api, name='participant_search_api'),
    path('participant-dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('faq-chat/', views.chatbot_faq, name='chatbot_faq'),
    path('register-event/<int:event_id>/', views.participant_register_event, name='participant_register_event'),
    path('cancel-registration/<int:member_id>/', views.participant_cancel_registration, name='cancel_registration'),
    path('qr-checkin/', views.qr_checkin, name='qr_checkin'),

    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/notifications/unread-count/', views.notification_unread_count_api, name='notification_unread_count_api'),
    path('api/notifications/recent/', views.notification_recent_api, name='notification_recent_api'),
    path('messages/', views.messages_view, name='chat_messages'),
    path('apps/', views.apps_menu_view, name='apps_menu'),
    path('change-password/', views.change_password_view, name='change_password'),

    path('create-category/', views.create_category, name='create_category'),
    path('category-list/', views.category_list, name='category_list'),
    path('category-edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category-delete/<int:pk>/', views.category_delete_confirm, name='delete_category'),

    path('create-event/', views.create_event, name='create_event'),
    path('event-list/', views.event_list, name='event_list'),
    path('event-detail/<int:pk>/', views.event_detail, name='event_detail'),
    path('event-history/<int:pk>/', views.event_history_view, name='event_history'),
    path('event-edit/<int:pk>/', views.edit_event, name='edit_event'),
    path('event-delete/<int:pk>/', views.delete_event_confirm, name='delete_event'),
    path('event-status/<int:pk>/', views.update_event_status, name='update_event_status'),
    path('events-schedule/', views.participant_event_list, name='participant_event_list'),
    path('events-schedule/<int:pk>/', views.participant_event_detail, name='participant_event_detail'),
    path('api/participant-events-calendar/', views.participant_events_calendar_api, name='participant_events_calendar_api'),

    path('add-event-member/', views.add_event_member, name='add_event_member'),
    path('remove-event-member/<int:pk>/', views.remove_event_member, name='remove_event_member'),
    path('member/status/<int:pk>/', views.update_member_registration_status, name='update_member_registration_status'),

    path('joined-events/', views.joined_events, name='joined_events'),
    path('completed-events/', views.completed_events, name='completed_events'),
    path('complete-event-users/<int:pk>/', views.complete_event_user_list, name='complete_event_user_list'),

    path('mark-attendance/<int:event_pk>/', views.create_user_mark, name='create_user_mark'),
    path('attendance-list/<int:event_pk>/', views.user_mark_list, name='user_mark_list'),
    path('absent-list/<int:event_pk>/', views.absent_user_list, name='absent_user_list'),

    path('add-event-wish/', views.add_event_wish, name='add_event_wish'),
    path('event-wish-list/', views.event_wish_list, name='event_wish_list'),
    path('approve-wish/<int:pk>/', views.approve_wish, name='approve_wish'),
    path('reject-wish/<int:pk>/', views.reject_wish, name='reject_wish'),
    path('remove-event-wish/<int:pk>/', views.remove_event_wish, name='remove_event_wish'),

    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.create_vendor, name='create_vendor'),
    path('vendors/edit/<int:pk>/', views.edit_vendor, name='edit_vendor'),
    path('vendors/delete/<int:pk>/', views.delete_vendor_confirm, name='delete_vendor'),

    path('budget-overview/', views.budget_overview, name='budget_overview'),
    path('expense/create/', views.create_expense, name='create_expense'),
    path('expense/approve/<int:pk>/', views.approve_expense, name='approve_expense'),
    path('expense/reject/<int:pk>/', views.reject_expense, name='reject_expense'),
    path('sponsorship/create/', views.create_sponsorship, name='create_sponsorship'),

    path('contact/', views.contact, name='contact'),
    path('contact-messages/', views.contact_message_list, name='contact_message_list'),
    path('contact-messages/<int:pk>/', views.contact_message_detail, name='contact_message_detail'),
    path('contact-messages/mark-reviewed/<int:pk>/', views.mark_contact_reviewed, name='mark_contact_reviewed'),
    path('my-inquiries/', views.participant_inquiry_list, name='participant_inquiry_list'),
    path('my-inquiries/<int:pk>/', views.participant_inquiry_detail, name='participant_inquiry_detail'),

    path('venues/', views.venue_list, name='venue_list'),
    path('venues/create/', views.create_venue, name='create_venue'),
    path('venues/edit/<int:pk>/', views.edit_venue, name='edit_venue'),
    path('venues/delete/<int:pk>/', views.delete_venue_confirm, name='delete_venue'),


    path('resources/', views.resource_list, name='resource_list'),
    path('resources/create/', views.create_resource, name='create_resource'),
    path('resources/edit/<int:pk>/', views.edit_resource, name='edit_resource'),
    path('resources/delete/<int:pk>/', views.delete_resource_confirm, name='delete_resource'),
    path('resources/allocate/', views.allocate_resource, name='allocate_resource'),
    path('resources/allocation/remove/<int:pk>/', views.remove_resource_allocation, name='remove_resource_allocation'),

    path('sponsors/', views.sponsor_list, name='sponsor_list'),
    path('sponsors/create/', views.create_sponsor, name='create_sponsor'),
    path('sponsors/edit/<int:pk>/', views.edit_sponsor, name='edit_sponsor'),
    path('sponsors/delete/<int:pk>/', views.delete_sponsor_confirm, name='delete_sponsor'),

    path('reports/', views.reports_home, name='reports_home'),
    path('reports/events/csv/', views.export_events_csv, name='export_events_csv'),
    path('reports/events/xlsx/', views.export_events_xlsx, name='export_events_xlsx'),
    path('reports/events/pdf/', views.export_events_pdf, name='export_events_pdf'),
    path('reports/members/csv/', views.export_members_csv, name='export_members_csv'),
    path('reports/members/xlsx/', views.export_members_xlsx, name='export_members_xlsx'),
    path('reports/members/pdf/', views.export_members_pdf, name='export_members_pdf'),
    path('reports/contacts/csv/', views.export_contacts_csv, name='export_contacts_csv'),
    path('reports/contacts/xlsx/', views.export_contacts_xlsx, name='export_contacts_xlsx'),
    path('reports/contacts/pdf/', views.export_contacts_pdf, name='export_contacts_pdf'),

    # ---------- REST API ----------
    path('api/categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('api/events/', EventListAPI.as_view(), name='api_events'),
    path('api/events/<int:pk>/', EventDetailAPI.as_view(), name='api_event_detail'),
    path('api/members/', MemberListAPI.as_view(), name='api_members'),
    path('api/vendors/', VendorListAPI.as_view(), name='api_vendors'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)