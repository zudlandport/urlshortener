from django.db import models

# Create your models here.

class myfwd(models.Model):
   fwdtourl = models.CharField(max_length=2048)
   myfwdurlstring = models.CharField(max_length=50)
   wascustomtitle = models.BooleanField(default=0)
   createdate = models.DateTimeField( auto_now_add=True )
   ## 'summary' of a row, for various admin / display purposes baked into django
   def __str__(self):
      return self.myfwdurlstring +' forwards to '+ self.fwdtourl


class myfwdhit(models.Model):
   myfwdid = models.ForeignKey(myfwd, on_delete=models.CASCADE)
   hitdate = models.DateTimeField( auto_now_add=True )
   def __str__(self):
      return self.myfwdid.__str() + ' at ' + self.hitdate.strftime(myfulltime)
