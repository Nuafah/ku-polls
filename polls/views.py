from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Redirect the request to polls/ if polls/k does not
        exist or unavailable.

        """

        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request,
                           message=f"Poll {kwargs['pk']} does not exist.")
            return redirect('polls:index')
        else:
            this_user = request.user
            try:
                prev_vote = Vote.objects.get(user=this_user,
                                             choice__question=question)
            except (Vote.DoesNotExist, TypeError):
                prev_vote = None
            if not question.can_vote():
                messages.error(request,
                               message=f"Poll {kwargs['pk']} "
                                       f"has been closed.")
                return redirect('polls:index')
            elif question.is_published():
                return render(request, self.template_name,
                              {'question': question,
                               "prev_vote": prev_vote})
            else:
                messages.error(request,
                               message=f"Poll {kwargs['pk']} "
                                       f"is not available.")
                return redirect('polls:index')


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "Please select a choice")
        return redirect("polls:detail", pk=question_id)
    # selected_choice.save()
    try:
        # find a vote this user and question
        vote = Vote.objects.get(user=user, choice__question=question)
        # update the vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # create a new vote and save
        vote = Vote(user=user, choice=selected_choice)
    vote.save()
    messages.success(request, message=f"voted for {selected_choice}")
    return HttpResponseRedirect(reverse('polls:results',
                                        args=(question.id,)))


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
