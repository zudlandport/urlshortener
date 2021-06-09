##
##
##          ABANDONED APPROACH - would address with more time.
##

##
## these are functions that help encode / decode / query-to FUSs --
## (Fwd Url Strings) -- the key element of all this stuff.
##


def createnew_randomnumber():
   ## roll it
   ## MySQL unsigned INT size = 4,294,967,295;
   ## we don't want a very large variety of tiny-url bit sizes, so let's go with something like "(1 - 4 billion) + 100 thousand"
   newrand = -1
   tries = 0
   maxtries = 10
   while tries < maxtries:
      tries += 1
      newrand = randint(1, 4000000000) + 100000
      ## (future tweak - we COULD have a dictionary of ones we've already randomly generated and FAILED, thus we wouldn't need to re-query the db to see if they already exist)
      ## make sure it doesn't already exist
      qalready = myfwd.objects.filter( myfwd_randomnumber = newrand )
      if len(qalready) < 1:
         break
   ## return whatever we're left with (SHOULD be GT 0 unless we failed all our tries)
   return newrand



def randomnumber_to_fus( randnum ):
   ## given a random number, this turns it into a FUS (Fwd Url String)
   fusbase = 64
   basecol = 1
   randminus = randnum
   lmods = []
   
   while randminus > 0:
      modby = pow(fusbase, basecol)
      lmods[ basecol - 1 ] = randminus % modby
      randminus -= thismod
      basecol += 1
   
   return fus
