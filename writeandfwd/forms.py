from django import forms
##from .models import myfwd


class myfwd_random(forms.Form):
   fwdtourl = forms.CharField(label='Webpage to Shorten', max_length=2048)
