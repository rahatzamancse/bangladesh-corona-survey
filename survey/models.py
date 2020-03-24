from django.db import models


class SurveyAnswer(models.Model):
    BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))
    fever = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    cough = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    breathless = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    olderThan60 = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    medHistory = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    outsideBD = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    closecontact = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    postcode = models.CharField(max_length=4)

    def __str__(self):
        ret = ''
        for k, v in zip(['fever', 'cough', 'breathless', 'olderThan60', 'medHistory', 'outsideBD', 'closecontact'], [self.fever, self.cough, self.breathless, self.olderThan60, self.medHistory, self.outsideBD, self.closecontact]):
            ret += f'\t{k}: {v}\n'
        return f'Postal code : {self.postcode}\n{ret}\n'
