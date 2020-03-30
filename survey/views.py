import requests
from django.core import serializers
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect

import plotly.express as px
from plotly.offline import plot
import pandas as pd

from bangla_corona import settings
from survey.forms import SurveyForm
from survey.models import SurveyAnswer


def classify(survey: SurveyAnswer) -> bool:
    return False


def index(request):
    if request.method == 'POST':
        # if 'previous_token' in request.POST:
        #     id = int(request.POST.get('previous_token'))
        #     if SurveyAnswer.objects.filter(id=id).exists():
        #         form = SurveyForm(instance=SurveyAnswer.objects.get(id=id))
        #     else:
        #         form = SurveyForm()
        #         id = 'invalid'
        #     return render(request, 'survey/index.html',
        #                   context={'form': form, 'site_key': settings.RECAPTCHA_SITE_KEY, 'id': id})
        # else:

        # Else start
        # create a form instance and populate it with data from the request:
        form = SurveyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer: SurveyAnswer = form.save(commit=False)
            answer = answer.calculate_infection_score()

            # RECAPTCHA v3 validation
            captcha_result = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'response': request.POST.get('g-recaptcha-response'),
                'secret': settings.RECAPTCHA_SECRET_KEY
            }).json()
            if captcha_result['success']:
                captcha_score = captcha_result['score']
            else:
                captcha_score = 0
            answer.captcha_score = captcha_score

            # Browser id
            if 'browser_id' in request.COOKIES:
                browser_id = int(request.COOKIES.get('browser_id'))
                answer.browser_id = browser_id
            else:
                browser_id = SurveyAnswer.objects.aggregate(Max('browser_id'))['browser_id__max']
                if not browser_id:
                    browser_id = 1
                else:
                    browser_id += 1
                answer.browser_id = browser_id


            # If updating previous data
            if request.POST.get('id'):
                id = int(request.POST.get('id'))
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
                    infection_score=answer.infection_score,
                    browser_id=answer.browser_id
                )

            # Adding new data
            else:
                answer.save()

            html = render(request, 'survey/submitted.html', context={'success': True, 'id': answer.id})
            html.set_cookie('browser_id', browser_id, max_age=999999999)
            # Else end

        else:
            print(form.errors)
            html = render(request, 'survey/submitted.html', context={'success': False})

        return html

    else:
        form = SurveyForm()
        cookied = 'true' if bool(request.COOKIES.get('browser_id')) else 'false'

        return render(request, 'survey/index.html',
                      context={'form': form, 'site_key': settings.RECAPTCHA_SITE_KEY, 'cookied': str(cookied)})


def info(request):
    url = 'https://pomber.github.io/covid19/timeseries.json'
    try:
        data = requests.get(url).json()
        last_updated = data['Bangladesh'][-1]['date']

        total_deaths = 0
        total_confirmed = 0
        total_recovered = 0
        bd_deaths = 0
        bd_confirmed = 0
        bd_recovered = 0

        highest_country = ''
        last_cases = 0
        for k, val in data.items():
            total_deaths += val[-1]['deaths']
            total_confirmed += val[-1]['confirmed']
            total_recovered += val[-1]['recovered']
            if k == 'Bangladesh':
                bd_deaths += val[-1]['deaths']
                bd_confirmed += val[-1]['confirmed']
                bd_recovered += val[-1]['recovered']

            if val[-1]['confirmed'] > last_cases:
                last_cases = val[-1]['confirmed']
                highest_country = k
        del last_cases

        total_active = total_confirmed - total_deaths - total_recovered
        bd_active = bd_confirmed - bd_deaths - bd_recovered

        dic = {
            'country': [],
            'date': [],
            'confirmed': [],
            'deaths': [],
            'recovered': [],
        }
        for k, val in data.items():
            for i in val:
                dic['country'].append(k)
                dic['date'].append(i['date'])
                dic['confirmed'].append(i['confirmed'])
                dic['deaths'].append(i['deaths'])
                dic['recovered'].append(i['recovered'])

        df = pd.DataFrame(dic)

        # fig = px.line(df, x='date', y='confirmed', color='country', title='Confirmed cases in Bangladesh each day')
        fig = px.line(
            df[df['country'] == 'Bangladesh'],
            x='date',
            y='confirmed',
            title='Confirmed cases in Bangladesh each day'
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        def convert_to_bn(number):
            transliterate = {
                '0': '০',
                '1': '১',
                '2': '২',
                '3': '৩',
                '4': '৪',
                '5': '৫',
                '6': '৬',
                '7': '৭',
                '8': '৮',
                '9': '৯',
                ',': ',',
            }
            number_bn = ''
            for v in str(number):
                number_bn += transliterate[v]
            return number_bn

        total_confirmed = convert_to_bn("{:,}".format(total_confirmed))
        total_deaths = convert_to_bn("{:,}".format(total_deaths))
        total_recovered = convert_to_bn("{:,}".format(total_recovered))
        total_active = convert_to_bn("{:,}".format(total_active))
        bd_confirmed = convert_to_bn("{:,}".format(bd_confirmed))
        bd_deaths = convert_to_bn("{:,}".format(bd_deaths))
        bd_recovered = convert_to_bn("{:,}".format(bd_recovered))
        bd_active = convert_to_bn("{:,}".format(bd_active))

        context = {
            'world_total_cases': total_confirmed,
            'world_deaths': total_deaths,
            'world_recovered': total_recovered,
            'world_active': total_active,

            'bd_total_cases': bd_confirmed,
            'bd_deaths': bd_deaths,
            'bd_recovered': bd_recovered,
            'bd_active': bd_active,

            'highest_country': highest_country,
            'last_updated': last_updated,

            'plot': plot_div,
        }
        return render(request, 'info.html', context=context)

    except Exception as e:
        print(e)
        return redirect('/')


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
    new_data = [[i['lat'], i['lon'], (i['infection_score'] - minx) / spread * new_spread + new_min] for i in data]
    return JsonResponse(new_data, safe=False)
