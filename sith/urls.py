from django.urls import path
from .views import sith_list, sith_card, sith_recruits 

urlpatterns = [
    path('', sith_list, name="sith_list"),
    path('<int:sith_id>/', sith_card, name="sith_card"),
    path('<int:sith_id>/recruits/', sith_recruits, name="sith_recruits"),
]