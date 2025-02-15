from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Holiday
from . serializers import HolidaySerializer
import requests
from datetime import datetime
from django.conf import settings
from django.db import transaction

class HolidayListAPIView(APIView):
    def get(self,request):
        country_code = request.query_params.get('country')
        year = request.query_params.get('year')

        if not country_code or not year:
            return Response({"error":"Country and year are required."},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            year = int(year)
        except ValueError:
            return Response({"error":"Invalid year."},status=status.HTTP_400_BAD_REQUEST)
        

        cache_key = f'holidays_{country_code}_{year}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        

        ###Fetch from Calendarific API###

        api_key = settings.CALENDARIFIC_API_KEY
        if not api_key:
            return Response({"error":"API key missing."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        url = 'https://calendarific.com/api/v2/holidays'
        params = {'api_key':api_key,'country':country_code,'year':year}

        try:
            response  = requests.get(url,params=params)
            response.raise_for_status()
            data = response.json()
            holidays_data = data.get('response', {}).get('holidays', [])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        

        ###Save holidays to DB###

        try:
            with transaction.atomic():
                for h in holidays_data:
                    try:
                        date_iso = h['date']['iso'].split('T')[0]
                        date = datetime.strptime(date_iso, '%Y-%m-%d').date()
                        type_str = ', '.join(h.get('type', []))[:50]
                        Holiday.objects.update_or_create(
                            name=h['name'],
                            country_code=country_code,
                            date=date,
                            defaults={
                                'description': h.get('description', '')[:2000],
                                'type': type_str,
                                'year': year
                            }
                        )
                    except KeyError:
                        continue
        except Exception as e:
            return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        holidays = Holiday.objects.filter(country_code=country_code, year=year)
        serializer = HolidaySerializer(holidays, many=True)
        cache.set(cache_key, serializer.data, timeout=86400)
        return Response(serializer.data)
    
class HolidaySearchAPIView(APIView):
    def get(self,request):
        search_term = request.query_params.get('name', '').strip()
        if not search_term:
            return Response({"error": "Name parameter required."}, status=status.HTTP_400_BAD_REQUEST)
        
        holidays = Holiday.objects.filter(name__icontains=search_term)
        serializer = HolidaySerializer(holidays,many=True)
        return Response(serializer.data)
    












