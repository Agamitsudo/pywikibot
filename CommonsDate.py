# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "/home/benoit/Documents/Projets Python/core")
import pywikibot
from pywikibot import pagegenerators	     
siteC = pywikibot.Site(u'commons', u'commons')
siteC.login()

category = pywikibot.Category(siteC, u'Images of Sézéria by Benoît Prieur')
print "this category is analysed..."
gen = pagegenerators.CategorizedPageGenerator(category)
for page in gen:
  text = page.text	
  page.text = text.replace("[[Category:Photographs taken on 2017-10-07]]", "[[Category:Photographs taken on 2017-10-08]]")
  page.save(u"fix date category")	
