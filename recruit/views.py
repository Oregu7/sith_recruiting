from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .forms import RecruitForm
from .models import Recruit, ShadowHandTest, ShadowHandSession, ShadowHandQuestion, ShadowHandAnswer


class RecruitCreate(View):
    def get(self, request):
        form = RecruitForm()
        return render(request, 'recruit/recruit_create.html', context={'form': form })
    
    def post(self, request):
        bound_form = RecruitForm(request.POST)
        if bound_form.is_valid():
            new_recruit = bound_form.save()
            #создаем сессию тестирования и делаем редирект
            session = self.create_session(new_recruit)
            redirect_url = self.create_session_url(session)
            return redirect(redirect_url)
        return render(request, 'recruit/recruit_create.html', context={'form': bound_form })

    def create_session(self, recruit: Recruit) -> ShadowHandSession:
        test = ShadowHandTest.get_random()
        session = ShadowHandSession.create(test, recruit)
        return session

    def create_session_url(self, session: ShadowHandSession) -> str:
        return f"/recruit/test/{session.token}"

    
class RecruitTesting(View):
    def get(self, request, token):
        session = get_object_or_404(ShadowHandSession, token=token)
        questions = ShadowHandQuestion.objects.filter(test=session.test)
        return render(request, 'recruit/recruit_testing.html', context={ 'session': session, 'questions': questions })

    def post(self, request, token):
        session = get_object_or_404(ShadowHandSession, token=token)
        questions = ShadowHandQuestion.objects.filter(test=session.test)
        answers = request.POST.getlist('question[]', [])
        if len(answers) < 1:
            return render(request, 'recruit/recruit_testing.html', context={ 
                'session': session, 
                'questions': questions,
                'error_message': 'Ответьте хотя бы на один вопрос!' 
            })
        # сохраняем ответы и завершаем сессию тестирования
        self.create_answers(session, questions, answers)
        session.done = True
        session.save(update_fields=['done'])

        return render(request, 'recruit/recruit_testing.html', context={ 'session': session })

    def create_answers(self, session, questions, answers):
        shadow_hand_answers = []
        for question in questions:
            answer = str(question.id) in answers
            shadow_hand_answer = ShadowHandAnswer(session = session, question = question, answer = answer)
            shadow_hand_answers.append(shadow_hand_answer)

        ShadowHandAnswer.objects.bulk_create(shadow_hand_answers)
