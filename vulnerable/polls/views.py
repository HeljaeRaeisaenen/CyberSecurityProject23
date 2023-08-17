from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice, Users

# import for security fix:
# import re

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def create(request):
    question = request.POST['question']
    user = Users.objects.get(pk=request.session['user'])
    q = user.question_set.create(question_text=question, pub_date=timezone.now())
    q.save()
    q.choice_set.create(choice_text=request.POST['choice_1'], votes=0)
    if request.POST['choice_2']:
        q.choice_set.create(choice_text=request.POST['choice_2'], votes=0)
    if request.POST['choice_3']:
        q.choice_set.create(choice_text=request.POST['choice_3'], votes=0)
    
    return HttpResponseRedirect(reverse('polls:detail', args=(q.id,)))

def results(request, pk):
    # This allows sql injection, which is obviously an injection hazard.
    # SHOULD BE:
    # question = Question.objects.get(pk=pk)
    # INSTEAD OF:
    question = Question.objects.raw('SELECT * FROM polls_question WHERE id ='+pk)[0]
    # end
    print(question)

    return render(request,
                  'polls/results.html',
                  {'question':question})

def login(request):
    return render(request, 'polls/login.html')

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('polls:index'))

def loginAction(request):
    username = request.POST['username']
    passw = request.POST['password']
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        # this is probably not safe, because you can find out
        # which usernames are in use
        return render(request,
            'polls/login.html',
            {'error_message':'User not found'})
    if user.check_password(passw):
        request.session['user'] = user.id
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request,
            'polls/login.html',
            {'error_message':'Wrong credentials'})

def signup(request):
    return render(request, 'polls/signup.html')

def signupAction(request):
    username = request.POST['username']
    passw = request.POST['password']
    # Allowing to use weak passwords is an authentication failure.
    # SHOULD INCLUDE:
    # strong_passw = "^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-.()]).{8,}$"
    # if not re.match(strong_passw, passw):
    #     return render(request,
    #         'polls/signup.html',
    #         {'error_message':'Password is not strong enough. It should be at least 8 symbols long'
    #          ' and contain at least one upper-case, special, and numeric character.'})
    # if re.search(username, passw):
    #     return render(request,
    #          'polls/signup.html',
    #          {'error_message':'Please don\'t include your username in your password.'})
    try:
        user = Users.objects.get(username=username)
        return render(request,
            'polls/signup.html',
            {'error_message':'Username is taken'})
    except Users.DoesNotExist:
        user = Users(username=username)
        user.set_password(passw)
        user.save()
        request.session['user'] = user.id
        return HttpResponseRedirect(reverse('polls:index'))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def userPage(request, pk):
    # this doesn't check the session, and thus allows unathorized access
    # by url manipulation, which is a Broken Access Control flaw.
    # SHOULD INCLUDE:
    # if request.session['user'] != pk:
    #    raise PermissionDenied()

    user = Users.objects.get(pk=pk)
    polls = Question.objects.filter(user=pk)

    return render(request, 'polls/userpage.html', 
                  {'user':user.username,'polls':polls})

def deletePoll(request):
    poll_id = request.POST['to_delete_id']
    poll = Question.objects.get(pk=poll_id)

    if not (poll.user_id == int(request.session['user'])):
        raise PermissionDenied()
    poll.delete()
    return HttpResponseRedirect(reverse('polls:index'))