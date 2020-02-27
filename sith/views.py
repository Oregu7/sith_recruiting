from django.shortcuts import render, get_object_or_404

from recruit.models import ShadowHandSession
from .models import Sith, ShadowHand


def sith_list(request):
    page = request.GET.get('page', 1)
    sith_list = Sith.pagination(page=page, limit=10)
    return render(request, "sith/sith_list.html", context={ 'sith_list': sith_list })


def sith_recruits(request, sith_id):
    sith = get_object_or_404(Sith, id=sith_id)
    page = request.GET.get('page', 1)
    session_list = ShadowHandSession.pagination_actual(page=page, limit=10)
    return render(request, "sith/sith_recruits.html", context={ 'sith': sith, 'session_list': session_list })