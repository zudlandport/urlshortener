from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect

from .forms import myfwd_random, myfwd_custom

from .models import myfwd, myfwdhit

from django.db.models import Count
from django.db.models.functions import TruncDate

# import RE module
import re

## for 'default new Appointment to the current datetime'
import datetime


from .fushelper import  createnew_randomstring, createone_fus


#############################
##
##    homepage
##



# Create your views here.
class HomePageView(TemplateView):
   def get(self, request, **kwargs):
      dfeatures = {
      	'./addfwd': 'Add a URL',
      	'./addfwdcustom': 'Add a URL with Custom Forwarder',
      	'./listfwds': 'Show All URLs',
      	## './testfus': 'Random Url String Demo',
      }
      context = {
         'dfeatures': dfeatures
      }
      return render(request, 'writeandfwd/index.html', context=context)





#############################
##
##    ADDS:
##


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
            thisstr = qalready[0].myfwdurlstring
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



##    IF I HAD MORE TIME:
## I'd like to build addfwdcustom() more integrated into addfwd() --
## it mainly made sense to keep it this strictly separate when I was
## going to store randomly-generated Forwarder strings as Ints

class addfwdcustom(TemplateView):
   def get(self, request):
      form = myfwd_custom()
      context = {
         'form': form,
         'writingcustom': True
      }
      return render(request, 'writeandfwd/fwdwrite.html', context=context)


   def post(self, request):
      thisform = myfwd_custom(request.POST)
      if thisform.is_valid():
         myfus = thisform.cleaned_data.get("myfwdurlstring")
         
         ## and strip out any weird characters (with more time this belongs as Validation rather than cleanup)
         myfus = re.sub('( |\&|\\\|\?|\/|`|\.|\!|\#)', '_', myfus)
         
         ## does this CUSTOM fwd text already exist?
         qalready = myfwd.objects.filter( myfwdurlstring = myfus )
         if len(qalready) > 0:
            ## IF it's directing to the URL they wanted, that's cool:
            if qalready[0].fwdtourl == thisform.cleaned_data.get("fwdtourl"):
               return HttpResponseRedirect('/see/' + myfus )
            else:
               ## otherwise it failed for some reason; this shouldn't happen, but for now we'll at least acknowledge it to the user:
               context = {
                  'form': thisform,
                  'writingcustom': True,
                  'error': 'That Custom URL is already taken!'
               }
               return render(request, 'writeandform/fwdwrite.html', context=context)            
         else:
            ## process:
            qf = myfwd.objects.create(
               fwdtourl = thisform.cleaned_data.get("fwdtourl"),
               myfwdurlstring = myfus,
               wascustomtitle = 1
            )
            qf.save()
            ## show the user this Webpage Forwarder:
            return HttpResponseRedirect('/see/' + myfus)
      else:
         ## send them back to form
         form = myfwd_custom(request.POST)
         context = {
            'form': thisform,
            'writingcustom': True
         }
         return render(request, 'writeandform/fwdwrite.html', context=context)




#############################
##
##    LISTS AND DISPLAYS
##


class listfwds(TemplateView):
   def get(self, request):
      qf = myfwd.objects.all().order_by('fwdtourl')
      context = {
         'qfwds': qf
      }
      return render(request, 'writeandfwd/listfwds.html', context=context)



class seeafwd(TemplateView):
   def get(self, request, fwdurlstring):
      qf = myfwd.objects.filter( myfwdurlstring = fwdurlstring )
      qfzero = ''
      if len(qf):
         qfzero = qf[0]
      context = {
         'qmyfwd': qfzero
      }
      return render(request, 'writeandfwd/see.html', context=context)


class seeafwd_details(TemplateView):
   def get(self, request, fwdurlstring, seemore):
      qf = myfwd.objects.filter( myfwdurlstring = fwdurlstring )
      hitcount = 0
      qbyday = ''
      if len(qf):
         if seemore == 'count':
            qhit = myfwdhit.objects.filter(
                  myfwdid = qf[0].id
               )
            hitcount = len(qhit)
         elif seemore == 'byday':
            qbyday = myfwdhit.objects.filter(
                  myfwdid = qf[0].id
               ).annotate(
                  justdate = TruncDate('hitdate')
               ).values('justdate'
               ).annotate(hitcount=Count('justdate')
               ).order_by('-justdate')

      qfzero = ''
      if len(qf):
         qfzero = qf[0]
      context = {
         'qmyfwd': qfzero,
         'hitcalc': True,
         'hitcount': hitcount,
         'qbyday': qbyday
      }
      return render(request, 'writeandfwd/see.html', context=context)


class fwdthemaway(TemplateView):
   def get(self, request, fwdurlstring):
      qf = myfwd.objects.filter( myfwdurlstring = fwdurlstring )
      if len(qf) < 1:
         return HttpResponseRedirect('/notfound/' + fwdurlstring)
      else:
         # log that we used it
         qhit = myfwdhit.objects.create(
            myfwdid = qf[0]
         )
         qhit.save()
         # fwd them
         return HttpResponseRedirect(qf[0].fwdtourl)


class badfwdurlstring(TemplateView):
   def get(self, request, fwdurlstring):
      fus = re.sub('(<|>|\'|")', '*', fwdurlstring)
      context = {
         'badfus': fus
      }
      return render(request, 'writeandfwd/notfound.html', context=context)




## testing

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
