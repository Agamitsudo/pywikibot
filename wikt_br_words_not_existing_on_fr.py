# -*- coding: utf-8 -*-
# br words existing on br.wiktionary and not on fr.wiktionary

import sys

sys.path.insert(0, "/home/benoit/Documents/pywikibot-core/core")
import pywikibot

sys.path.insert(0, "/home/benoit/Documents/pywikibot-core/core/pywikibot")
import pagegenerators
import re
import math
import time

siteBr = pywikibot.Site(u'br', u'wiktionary')
siteBr.login()

siteFr = pywikibot.Site(u'fr', u'wiktionary')
siteFr.login()

result = u""

num = 0
numTot = 0

#
# mainMethod
#
def mainMethod(topCategoryName, result, num, numTot):

	category = pywikibot.Category(siteBr, topCategoryName)
	print "this category is analysed..." + topCategoryName
	
	items = pagegenerators.CategorizedPageGenerator(category, recurse=False)
	for item in items:

		title = item.title()
		#print("reading..." + title )
		numTot = numTot + 1
		pageFr = pywikibot.Page(siteFr, title)
		if pageFr.exists() == False:
			
			result += u"# [[" + title + u"]] <small>([[:br:" + title + u"]])</small>\n"
			#print u"+ " + title
			num = num + 1
			print str(num) + u"/" +	str(numTot)		

	#categories = pagegenerators.SubCategoriesPageGenerator(category, recurse=False)
	#for cat in categories:
	#	result = recursiveMethod(cat.title(), result, num, numTot)		

	result += "\n\n*" + str(num) + u"/" + str(numTot)
	return result		
#
# Main
#

result = mainMethod(u"Rummad:Brezhoneg", result, num, numTot)
page = pywikibot.Page(siteFr, u"Utilisateur:Benoît Prieur/Comparaison_fr_br")
page.text = result
page.save("done")	




