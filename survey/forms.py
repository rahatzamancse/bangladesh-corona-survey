from django import forms
from survey.models import SurveyAnswer


class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyAnswer
        fields = ['fever', 'cough', 'breathless', 'olderThan60', 'medHistory', 'outsideBD', 'closecontact', 'postcode']
        # fields = '__all__'
        # exclude = ['corona']

        widgets = {
            'fever': forms.RadioSelect,
            'cough': forms.RadioSelect,
            'breathless': forms.RadioSelect,
            'olderThan60': forms.RadioSelect,
            'medHistory': forms.RadioSelect,
            'outsideBD': forms.RadioSelect,
            'closecontact': forms.RadioSelect
        }
        labels = {
            'fever': 'আপনার কি জ্বর, সর্দি বা কাঁপুনি আছে?',
            'cough': 'আপনার কি নতুন বা ক্রমবর্ধমান কাশি হচ্ছে?',
            'breathless': 'আপনি কি শ্বাসকষ্ট অনুভব করছেন?',
            'olderThan60': 'আপনি 60 বছর বা তার বেশি বয়সী?',
            'medHistory': 'আপনার কি নিম্নলিখিত চিকিত্সা শর্তাবলী রয়েছে: ডায়াবেটিস, হৃদরোগ, সক্রিয় ক্যান্সার, স্ট্রোকের ইতিহাস, হাঁপানি, সিওপিডি, ডায়ালাইসিস, বা ইমিউনোকম্প্রাইজড?',
            'outsideBD': 'আপনি কি গত ১৪ দিনের মধ্যে বাংলাদেশের বাইরে ভ্রমণ করেছেন?',
            'closecontact': 'সর্দি কাশি, জ্বরে আক্রান্ত, বা অন্যথায় অসুস্থ এবং গত ১৪ দিনে বাংলাদেশের বাইরে ছিলেন এমন কারও সাথে আপনার ঘনিষ্ঠ যোগাযোগ রয়েছে?',
            'postcode': 'আপনার বর্তমান পোস্টাল কোড কী?'
        }
