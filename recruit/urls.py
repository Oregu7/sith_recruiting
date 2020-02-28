from django.urls import path
from .views import RecruitCreate, RecruitTesting

urlpatterns = [
    path('', RecruitCreate.as_view(), name="recruit_create"),
    path('test/<str:token>/', RecruitTesting.as_view(), name="recruit_testing"),
]