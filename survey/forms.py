from django import forms
from survey.models import SurveyAnswer


class SurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        for field_name in ['fever', 'cough', 'cold', 'diarrhea', 'sore_throat', 'body_ache', 'headache', 'breathless', 'fatigue', 'diabetes', 'heart', 'lever', 'smoking', 'cancer_therapy', 'steroid', 'travel_14_days', 'travel_infected_3_month', 'close_contact']:
            self.fields[field_name].required = False

    class Meta:
        model = SurveyAnswer
        # fields = ['', '']
        # fields = '__all__'

        # These fields will be calculated after submission by the user
        exclude = ['submission_time', 'captcha_score', 'infection_score']

        widgets = {
            'fever': forms.RadioSelect,

            'cough': forms.CheckboxInput,
            'cold': forms.CheckboxInput,
            'diarrhea': forms.CheckboxInput,
            'sore_throat': forms.CheckboxInput,
            'body_ache': forms.CheckboxInput,
            'headache': forms.CheckboxInput,
            'breathless': forms.CheckboxInput,
            'fatigue': forms.CheckboxInput,

            'age_group': forms.Select,

            'diabetes': forms.CheckboxInput,
            'heart': forms.CheckboxInput,
            'lever': forms.CheckboxInput,
            'smoking': forms.CheckboxInput,
            'cancer_therapy': forms.CheckboxInput,
            'steroid': forms.CheckboxInput,

            'travel_14_days': forms.RadioSelect,
            'travel_infected_3_month': forms.RadioSelect,
            'close_contact': forms.RadioSelect,

            'postcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'postal'}),

            'lat': forms.HiddenInput,
            'lon': forms.HiddenInput,
        }
        labels = {
            'fever': 'আপনার জ্ব‌রের মাত্রা কি ৩৭.৮ ডিগ্রী সেল‌সিয়া‌স বা ১০০ ডিগ্রী ফারেনহেইট অ‌ধিক?',

            'cough': 'কফ/কা‌শি',
            'cold': 'ঠান্ডা/স‌র্দি',
            'diarrhea': 'পাতলা পায়খানা',
            'sore_throat': 'গলা ব্যথা, খুসখু‌সে ভাব বা ঘা',
            'body_ache': 'মাংস‌পে‌শি‌তে কিংবা শরীরে ব্যথা',
            'headache': 'মাথা ব্যথা',
            'breathless': 'শ্বাস কষ্ট',
            'fatigue': 'দূর্বল/ অবসাদগ্রস্ত',

            'age_group': 'আপনার বয়স কোন গ্রুপে?',

            'diabetes': 'ডায়াবেটিস/বহুমূত্র',
            'heart': 'হৃদরোগ',
            'lever': 'লিভার/যকৃতে সমস্যা',
            'smoking': 'ধূমপানে আসক্ত',
            'cancer_therapy': 'ক্যান্সার/কেমো/রেডিও থেরাপি দিয়েছেন',
            'steroid': 'স্টেরয়েড (যেমনঃ প্রেডনিসোলন) ট্যাবলেট খাচ্ছেন',

            'travel_14_days': 'গত ১৪ দিনে আপনি কোথাও ভ্রমণ করেছেন?',
            'travel_infected_3_month': 'গত ৩ মাসে আপনি করোনাএ ব্যাপক আক্রান্ত দেশগুলোতে গিয়েছেন?',
            'close_contact': 'এমন ব্যক্তির সংস্পর্শে এসেছিলেন যার জ্বর, কাশি ও শ্বাসকষ্ট ছিল?',

            'postcode': 'আপনার বর্তমান পোস্টাল কোড কী?'
        }
