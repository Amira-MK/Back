from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from hubspot import HubSpot
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# HubSpot constants
HUBSPOT_BASE_URL = "https://api.hubapi.com"
HUBSPOT_TOKEN = os.getenv("HUBSPOT_API_KEY")

def get_hubspot_headers():
    """Returns the headers required for HubSpot API calls."""
    return {
        "Authorization": f"Bearer {HUBSPOT_TOKEN}",
        "Content-Type": "application/json"
    }

@api_view(['GET'])
def get_contacts(request):
    """Fetch contacts from HubSpot."""
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts"
        response = requests.get(url, headers=get_hubspot_headers())
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return Response(response.json(), status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_deals(request):
    """Fetch deals from HubSpot."""
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals"
        response = requests.get(url, headers=get_hubspot_headers())
        response.raise_for_status()
        return Response(response.json(), status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def link_contact_deal(request):
    """Link a contact to a deal in HubSpot."""
    contact_id = request.data.get('contact_id')
    deal_id = request.data.get('deal_id')

    if not contact_id or not deal_id:
        return Response({"error": "Both contact_id and deal_id are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    url = f"{HUBSPOT_BASE_URL}/crm/v4/objects/0-1/{contact_id}/associations/0-3/{deal_id}"
    body = [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 4}]

    try:
        response = requests.put(url, headers=get_hubspot_headers(), json=body)
        response.raise_for_status()
        return Response({"message": "Contact successfully linked to deal."}, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def link_deal_contact(request):
    """Link a deal to a contact in HubSpot."""
    deal_id = request.data.get('deal_id')
    contact_id = request.data.get('contact_id')

    if not deal_id or not contact_id:
        return Response({"error": "Both deal_id and contact_id are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    url = f"{HUBSPOT_BASE_URL}/crm/v4/objects/0-3/{deal_id}/associations/0-1/{contact_id}"
    body = [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]

    try:
        response = requests.put(url, headers=get_hubspot_headers(), json=body)
        response.raise_for_status()
        return Response({"message": "Deal successfully linked to contact."}, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
