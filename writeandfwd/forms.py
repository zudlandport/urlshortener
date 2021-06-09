from django import forms
##from .models import myfwd


class myfwd_random(forms.Form):
   fwdtourl = forms.URLField(label='Webpage to Shorten', max_length=2048)
   
   
class myfwd_custom(forms.Form):
   fwdtourl = forms.URLField(label='Webpage to Shorten', max_length=2048)
   myfwdurlstring = forms.CharField(label='Custom Short Url', max_length=50)
   