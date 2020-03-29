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
        # check whether it's valid:
        if form.is_valid():
            # RECAPTCHA v3 validation
            captcha_result = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'response': request.POST.get('g-recaptcha-response'),
                'secret': settings.RECAPTCHA_SECRET_KEY
            }).json()
            if captcha_result['success']:
                captcha_score = captcha_result['score']
            else:
                captcha_score = 0
            answer: SurveyAnswer = form.save(commit=False)
            answer.captcha_score = captcha_score
            answer = answer.calculate_infection_score()

            if request.COOKIES.get('last_answer'):
                id = int(request.COOKIES.get('last_answer'))
                SurveyAnswer.objects.filter(id=id).update(
                    fever=answer.fever,
                    cough=answer.cough,
                    diarrhea=answer.diarrhea,
                    sore_throat=answer.sore_throat,
                    body_ache=answer.body_ache,
                    headache=answer.headache,
                    breathless=answer.breathless,
                    fatigue=answer.fatigue,
                    age_group=answer.age_group,
                    diabetes=answer.diabetes,
                    heart=answer.heart,
                    lever=answer.lever,
                    smoking=answer.smoking,
                    cancer_therapy=answer.cancer_therapy,
                    steroid=answer.steroid,
                    travel_14_days=answer.travel_14_days,
                    travel_infected_3_month=answer.travel_infected_3_month,
                    close_contact=answer.close_contact,
                    postcode=answer.postcode,
                    lat=answer.lat,
                    lon=answer.lon,
                    captcha_score=captcha_score,
                    infection_score=answer.infection_score
                )
            else:
                answer.save()
                id = answer.id

            html = render(request, 'survey/submitted.html', context={'success': True})
            html.set_cookie('last_answer', id, max_age=999999999)

            return html
        else:
            html = render(request, 'survey/submitted.html', context={'success': False})
            return html

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.COOKIES.get('last_answer'):
            id = int(request.COOKIES.get('last_answer'))
            answer = SurveyAnswer.objects.get(id=id)
            form = SurveyForm(instance=answer)
            cookied = 'true'
        else:
            form = SurveyForm()
            cookied = 'false'

    return render(request, 'survey/index.html', context={'form': form, 'site_key': settings.RECAPTCHA_SITE_KEY, 'cookied': cookied})


def surveydata(request):
    data = serializers.serialize('python', SurveyAnswer.objects.all(), fields=('lat', 'lon', 'infection_score'))
    data = [d['fields'] for d in data]
    for i, d in enumerate(data):
        data[i]['lat'] = float(data[i]['lat'])
        data[i]['lon'] = float(data[i]['lon'])

    new_min = 0.5
    new_max = 1.0
    new_spread = new_max - new_min
    minx = min([i['infection_score'] for i in data])
    maxx = max([i['infection_score'] for i in data])
    spread = maxx - minx
    if spread == 0:
        spread = maxx
    new_data = [[i['lat'], i['lon'], (i['infection_score']-minx)/spread*new_spread + new_min] for i in data]
    return JsonResponse(new_data, safe=False)
