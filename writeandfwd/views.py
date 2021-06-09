from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect

from .forms import myfwd_random
## from .forms import AppointmentForm
## from .forms import PaintingForm

## from .models import art_client
## from .models import art_appointment
## from .models import art_painting
## from .models import paintcolor
## from .models import clientmood

## from .navhelper import getnavdictfromparamsdict

## for 'default new Appointment to the current datetime'
import datetime


from .fushelper import  createnew_randomstring, createone_fus


#############################
##
##    BASICS
##



# Create your views here.
class HomePageView(TemplateView):
   def get(self, request, **kwargs):
      dfeatures = {
      	'./addfwd': 'Add a URL',
      	'./addfwdcustom': 'Add a URL with Custom Forwarder',
      	'./listfwds': 'Show All URLs',
      	'./testfus': 'Random Url String Demo',
      }
      context = {
         'dfeatures': dfeatures
      }
      return render(request, 'writeandfwd/index.html', context=context)


class addfwd(TemplateView):
   def get(self, request):
      form = myfwd_random()
      context = {
         'form': form,
      }
      return render(request, 'writeandfwd/fwdwrite.html', context=context)

   def post(self, request):
      thisform = myfwd_random(request.POST)
      if thisform.is_valid():
      
         ## does this website already exist?
         qalready = myfwd.objects.filter( fwdtourl = thisform.cleaned_data.get("fwdtourl") )
         if len(qalready) > 0:
            ## (show the user a PRE-EXISTING webpage forwarder)
            ## (at some point we consider saying "this already existed..")
            thisstr = qalready.myfwd_customtitle
            if thisstr == '':
               thisstr = randomnumber_to_fus(qalready.myfwd_randomnumber)
            return HttpResponseRedirect('/see/' + thisstr)
            
         else:
            ## process:
            newrand = createnew_randomstring()
            if len(newrand) > 0:
               qf = myfwd.objects.create(
                  fwdtourl = thisform.cleaned_data.get("fwdtourl"),
                  myfwdurlstring = newrand
               )
               qf.save()
               ## show the user this Webpage Forwarder:
               return HttpResponseRedirect('/see/' + newrand)
            else:
               ## it failed for some reason; this shouldn't happen, but for now we'll at least acknowledge it to the user:
               context = {
                  'form': thisform,
                  'error': 'FAILED to create a Url Shortener!'
               }
               return render(request, 'writeandform/fwdwrite.html', context=context)
                           
      else:
         ## send them back to form
         form = myfwd_random(request.POST)
         context = {
            'form': thisform
         }
         return render(request, 'writeandform/fwdwrite.html', context=context)


class addfwdcustom(TemplateView):
   def get(self, request):
      return


class listfwds(TemplateView):
   def get(self, request):
      return


class seeafwd(TemplateView):
   def get(self, request, fwdurlstring):
      qf = myfwd.objects.filter( myfwdurlstring = newfus )
      context = {
         'qmyfwd': qf
      }
      return render(request, 'writeandfwd/see.html', context=context)



## backend / testing things

class testfus(TemplateView):
   def get(self, request):
      ##newfus = ''
      ##for i in range(0,64):
      ##   newfus += fus_charint_to_char(i)
      newfus = createone_fus()
      context = {
         'newfus': newfus
      }
      return render(request, 'writeandfwd/testfus.html', context=context)
