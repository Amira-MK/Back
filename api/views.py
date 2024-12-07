from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from hubspot import HubSpot
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv


load_dotenv()
HUBSPOT_BASE_URL  = "https://api.hubapi.com"

hubspot_client = HubSpot(api_key=os.getenv("HUBSPOT_API_KEY"))

HUBSPOT_TOKEN = os.getenv("HUBSPOT_API_KEY")

def get_hubspot_headers():
    return {"Authorization": f"Bearer {HUBSPOT_TOKEN}"}

@api_view(['GET'])
def get_contacts(request):
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts"
    response = requests.get(url, headers=get_hubspot_headers())
    return Response(response.json())

@api_view(['GET'])
def get_deals(request):
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals"
    response = requests.get(url, headers=get_hubspot_headers())
    return Response(response.json())

def get_hubspot_headers():
    return {
        "Authorization": f"Bearer {HUBSPOT_TOKEN}",
        "Content-Type": "application/json"
    }

# Link a contact to a deal
@api_view(['POST'])
def link_contact_deal(request):
    # Get data from request
    contact_id = request.data.get('contact_id')
    deal_id = request.data.get('deal_id')
    
    if not contact_id or not deal_id:
        return Response({"error": "Both contact_id and deal_id are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # URL for associating the contact to the deal
    url = f"{HUBSPOT_BASE_URL}/crm/v4/objects/0-1/{contact_id}/associations/0-3/{deal_id}"

    # Body for the request to associate contact with deal
    body = [
        {
            "associationCategory": "HUBSPOT_DEFINED",
            "associationTypeId": 4  # Correct association type ID
        }
    ]

    # Make PUT request to HubSpot API
    response = requests.put(url, headers=get_hubspot_headers(), json=body)
    
    # Check the response status
    if response.status_code == 201:
        return Response({
            "message": "Contact successfully linked to deal.",
            "details": response.json()
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": f"Failed to link contact to deal. Status code: {response.status_code}",
            "details": response.json()
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def link_deal_contact(request):
    # Get data from request
    deal_id = request.data.get('deal_id')
    contact_id = request.data.get('contact_id')
    
    if not deal_id or not contact_id:
        return Response({"error": "Both deal_id and contact_id are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # URL for associating the deal to the contact
    url = f"{HUBSPOT_BASE_URL}/crm/v4/objects/0-3/{deal_id}/associations/0-1/{contact_id}"

    # Body for the request to associate deal with contact
    body = [
        {
            "associationCategory": "HUBSPOT_DEFINED",
            "associationTypeId": 3  # Correct association type ID
        }
    ]

    # Make PUT request to HubSpot API
    response = requests.put(url, headers=get_hubspot_headers(), json=body)
    
    # Check the response status
    if response.status_code == 201:
        return Response({
            "message": "Deal successfully linked to contact.",
            "details": response.json()
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": f"Failed to link deal to contact. Status code: {response.status_code}",
            "details": response.json()
        }, status=status.HTTP_400_BAD_REQUEST)