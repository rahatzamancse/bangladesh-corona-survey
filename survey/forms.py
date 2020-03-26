from django import forms
from survey.models import SurveyAnswer


class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyAnswer
        fields = ['fever', 'cough', 'breathless', 'older_than_60', 'med_history', 'outside_BD', 'close_contact', 'postcode', 'lat', 'lon']
        # fields = '__all__'
        # exclude = ['corona']

        widgets = {
            'fever': forms.RadioSelect,
            'cough': forms.RadioSelect,
            'breathless': forms.RadioSelect,
            'older_than_60': forms.RadioSelect,
            'med_history': forms.RadioSelect,
            'outside_BD': forms.RadioSelect,
            'close_contact': forms.RadioSelect,
            'postcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'postal'})
        }
        labels = {
            'fever': 'আপনার কি জ্বর, সর্দি বা কাঁপুনি আছে?',
            'cough': 'আপনার কি নতুন বা ক্রমবর্ধমান কাশি হচ্ছে?',
            'breathless': 'আপনি কি শ্বাসকষ্ট অনুভব করছেন?',
            'older_than_60': 'আপনি 60 বছর বা তার বেশি বয়সী?',
            'med_history': 'আপনার কি নিম্নলিখিত চিকিত্সা শর্তাবলী রয়েছে: ডায়াবেটিস, হৃদরোগ, সক্রিয় ক্যান্সার, স্ট্রোকের ইতিহাস, হাঁপানি, সিওপিডি, ডায়ালাইসিস, বা ইমিউনোকম্প্রাইজড?',
            'outside_BD': 'আপনি কি গত ১৪ দিনের মধ্যে বাংলাদেশের বাইরে ভ্রমণ করেছেন?',
            'close_contact': 'সর্দি কাশি, জ্বরে আক্রান্ত, বা অন্যথায় অসুস্থ এবং গত ১৪ দিনে বাংলাদেশের বাইরে ছিলেন এমন কারও সাথে আপনার ঘনিষ্ঠ যোগাযোগ রয়েছে?',
            'postcode': 'আপনার বর্তমান পোস্টাল কোড কী?'
        }
