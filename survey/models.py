from django.db import models


class SurveyAnswer(models.Model):
    # ENUMS
    # SEVERE = 'SV'
    # MILD = 'MD'
    # SPREADER = 'SP'
    # SAFE = 'SF'
    # INFECTED_CHOICES = (
    #     (SEVERE, 'severe'),
    #     (MILD, 'mild'),
    #     (SPREADER, 'spreader'),
    #     (SAFE, 'safe'),
    # )
    BOOLEAN_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    CHILD = 'CH'
    TEEN = 'TE'
    YOUNG = 'YN'
    ADULT = 'AD'
    OLD = 'OL'
    AGE_GROUP = (
        (CHILD, '1-13'),
        (TEEN, '13-19'),
        (YOUNG, '20-39'),
        (ADULT, '40-59'),
        (OLD, '60+'),
    )

    # Symptoms
    fever = models.BooleanField(choices=BOOLEAN_CHOICES, default=False, )

    cough = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    cold = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    diarrhea = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    sore_throat = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    body_ache = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    headache = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    breathless = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    fatigue = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)

    age_group = models.CharField(
        max_length=2,
        choices=AGE_GROUP
    )

    # Medical Histories
    diabetes = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    heart = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    lever = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    smoking = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    cancer_therapy = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    steroid = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)

    # Travel history
    travel_14_days = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    travel_infected_3_month = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    close_contact = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)

    # Locations
    postcode = models.IntegerField()

    # GPS
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    # Automated
    captcha_score = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    submission_time = models.TimeField(auto_now=True)
    infection_score = models.IntegerField(null=True)

    # infected = models.CharField(
    #     max_length=2,
    #     choices=INFECTED_CHOICES,
    #     default=SAFE,
    # )

    # def classify_infection(self):
    #     if (self.close_contact or self.travel_14_days) and (self.fever or self.cough):
    #         if self.breathless:
    #             self.infected = self.SEVERE
    #         else:
    #             self.infected = self.MILD
    #     else:
    #         self.infected = self.SAFE
    #     return self

    def calculate_infection_score(self):
        score = (int(self.cough) +
                 int(self.cold) +
                 int(self.diarrhea) +
                 int(self.sore_throat) +
                 int(self.body_ache) +
                 int(self.headache) +
                 int(self.fever) +
                 int(self.breathless) * 2 +
                 int(self.fatigue) * 2 +
                 int(self.travel_14_days) * 3 +
                 int(self.travel_infected_3_month) * 3 +
                 int(self.close_contact) * 3)
        self.infection_score = score
        return self

    def __str__(self):
        return f'<Survey: Score: {self.infection_score}, postcode: {self.postcode}>'
