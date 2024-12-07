
from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('deals/', views.get_deals, name='get_deals'),
    path('link-contact-deal/', views.link_contact_deal, name='link_contact_deal'),
    path('link_deal_contact/', views.link_deal_contact, name='link_contact_deal'),
]
