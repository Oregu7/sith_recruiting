from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, HttpResponseBadRequest
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sith_recruiting.settings import SENDGRID_API_KEY
from recruit.models import ShadowHandSession
from .models import Sith, ShadowHand


def sith_list(request):
    page = request.GET.get('page', 1)
    sith_list = Sith.pagination(page=page, limit=10)
    return render(request, "sith/sith_list.html", context={ 'sith_list': sith_list })


def sith_card(request, sith_id):
   sith = get_object_or_404(Sith, id=sith_id)
   return render(request, "sith/sith_card.html", context={ 'sith': sith }) 


def sith_recruits(request, sith_id):
    sith = get_object_or_404(Sith, id=sith_id)
    page = request.GET.get('page', 1)
    session_list = ShadowHandSession.pagination_actual(page=page, limit=10)
    return render(request, "sith/sith_recruits.html", context={ 'sith': sith, 'session_list': session_list })
    

def set_shadowhand(request, sith_id):
    session_id = request.GET.get('session', None)
    session = get_object_or_404(ShadowHandSession, id=session_id)
    sith = get_object_or_404(Sith, id=sith_id)
    if sith.shadowhand_set.count() >= 3:
        return JsonResponse({"message": "У вас уже достаточное количество Рук Теней"}, status=403)

    try:
        shadowhand = ShadowHand(sith_master=sith, recruit=session.recruit)
        session.success = True
        shadowhand.save()
        session.save(update_fields=['success'])
    except:
        return JsonResponse({"message": "Данного рекрута уже завербовали!"}, status=400)
    
    send_message_to_recruit(sith, session.recruit)
    return JsonResponse({"message": "Вы повисили рекрута до Руки Тени"})


def send_message_to_recruit(sith, recruit):
    message = Mail(
    from_email='Palpatine@sith-recruiting.herokuapp.com',
    to_emails=recruit.email,
    subject=f'{recruit.name}, добро пожаловать в Орден Ситхов!',
    html_content=f'Ситх <strong>{sith.name}</strong> выбрал Вас в качестве Руки Тьмы. {recruit.name}, Вам необходимо прибыть на планету <strong>{sith.planet}</strong>.')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e.message)