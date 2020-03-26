from django.contrib import admin
from survey.models import SurveyAnswer


class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('submission_time',)


admin.site.register(SurveyAnswer, SurveyAdmin)
