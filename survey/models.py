from django.db import models


class SurveyAnswer(models.Model):
    SEVERE = 'SV'
    MILD = 'MD'
    SPREADER = 'SP'
    SAFE = 'SF'
    INFECTED_CHOICES = (
        (SEVERE, 'severe'),
        (MILD, 'mild'),
        (SPREADER, 'spreader'),
        (SAFE, 'safe'),
    )
    BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))

    fever = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    cough = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    breathless = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    older_than_60 = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    med_history = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    outside_BD = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    close_contact = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    postcode = models.IntegerField()
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    submission_time = models.TimeField(auto_now=True)
    captcha_score = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    infected = models.CharField(
        max_length=2,
        choices=INFECTED_CHOICES,
        default=SAFE,
    )

    def classify_infection(self):
        if (self.close_contact or self.outside_BD) and (self.fever or self.cough):
            if self.breathless:
                self.infected = self.SEVERE
            else:
                self.infected = self.MILD
        else:
            self.infected = self.SAFE
        return self

    def __str__(self):
        return f'<Survey: {self.infected}, postcode: {self.postcode}>'

