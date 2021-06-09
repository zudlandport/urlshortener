##
## these are functions that help encode / decode / query-to FUSs --
## (Fwd Url Strings) -- the key element of all this stuff.
##
##
##    size:  6 columns of base-64 gives us 68 million possible URLs.

import random
from .models import myfwd


def createnew_randomstring():
   ## roll it
   ## MySQL unsigned INT size = 4,294,967,295;
   ## we don't want a very large variety of tiny-url bit sizes, so let's go with something like "(1 - 4 billion) + 100 thousand"
   tries = 0
   maxtries = 5
   while tries < maxtries:
      tries += 1
      newfus = createone_fus()
      qalready = myfwd.objects.filter( myfwdurlstring = newfus )
      if len(qalready) < 1:
         break
      else:
         newfus = ''
   ## return whatever we're left with (SHOULD be not-emptystring unless we failed all our tries)
   return newfus
   

def createone_fus():
   fus = ''
   cols = 6
   for i in range(0,cols):
      fus += createone_fus_char()   
   return fus
   

def createone_fus_char():
   ## one of 64 characters: 0-9A-Za-z plus - and _
   charint = random.randint(0,63)
   return fus_charint_to_char(charint)

def fus_charint_to_char(charint):
   thischar = ''
   asciioffset = 0
   if charint < 10:
      thischar = str(charint)
   elif charint < 36:
      asciioffset = 55  ## (65 - 10)
   elif charint < 62:
      asciioffset = 61  ## (97 - 36)
   elif charint == 62:
      thischar = '-'
   else:
      thischar = '_'
         
   if asciioffset > 0:
      thischar = chr( charint + asciioffset )
   
   ### thischar = '[' +str(charint)+ '=' +thischar+ ']'
   
   return thischar

