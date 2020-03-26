import requests
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from bangla_corona import settings
from survey.forms import SurveyForm
from survey.models import SurveyAnswer


def classify(survey: SurveyAnswer) -> bool:
    return False


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SurveyForm(request.POST)
        # RECAPTCHA v3 validation
        captcha_result = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'response': request.POST.get('g-recaptcha-response'),
            'secret': settings.RECAPTCHA_SECRET_KEY
        }).json()
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_survey: SurveyAnswer = form.save()
            new_survey = new_survey.classify_infection()
            new_survey.save()

            # redirect to a new URL:
            return HttpResponseRedirect('heatmap')
        else:
            # TODO: Show error message
            return HttpResponseRedirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SurveyForm()

    return render(request, 'survey/index.html', context={'form': form, 'site_key': settings.RECAPTCHA_SITE_KEY})


def surveydata(request):
    data = serializers.serialize('python', SurveyAnswer.objects.all(), fields=('lat', 'lon', 'infected'))
    data = [d['fields'] for d in data]
    for i, d in enumerate(data):
        data[i]['lat'] = float(data[i]['lat'])
        data[i]['lon'] = float(data[i]['lon'])
    # data = json.dumps(data)
    return JsonResponse(data, safe=False)
