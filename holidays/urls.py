from django.urls import path
from . views import HolidayListAPIView,HolidaySearchAPIView

urlpatterns = [
    path('holidays/',HolidayListAPIView.as_view(),name='holiday-list'),
    path('holidays/search/',HolidaySearchAPIView.as_view(),name='holiday-search'),
    
]