from django.http import HttpResponseRedirect
from django.shortcuts import render

from survey.forms import SurveyForm


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SurveyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():  # TODO: Also validated form in js on client side
            # process the data in form.cleaned_data as required
            new_survey = form.save()
            print(new_survey)
            # redirect to a new URL:
            return HttpResponseRedirect('')
        else:
            return HttpResponseRedirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SurveyForm()

    return render(request, 'survey/index.html', context={'form': form})
