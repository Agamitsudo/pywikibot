# -*- coding: utf-8 -*-
# Usage of .ogg files on fr.wiktionary.py

import sys
import pywikibot

sys.path.insert(0, "/home/benoit/Documents/pywikibot-core/core/pywikibot")

import pagegenerators
import re
import math

EXTENSION = u".ogg"
PREFIX = u"File:Fr-"
PARIS = u"Paris--"
TEMPLATE = u"{{écouter"
	     
siteWiktionary = pywikibot.Site(u'fr', u'wiktionary')
siteWiktionary.login()

siteCommons = pywikibot.Site(u'commons', u'commons')
siteCommons.login()

topCategoryName = u"Category:French pronunciation"

result = u"La liste ci-dessous regroupe les fichiers .ogg existants sur WikiCommons mais non repris sur les articles du Wiktionnaire correspondants. Ils sont tous issus de l'arborescence [[:Commons:" + topCategoryName + "]]. Si vous utilisez un fichier .ogg dans son article, merci de barrer la ligne correspondante ci-dessous.\n\n"

wordsDone = []

#
# recursiveMethod
#
def recursiveMethod(topCategoryName, result, count):

	category = pywikibot.Category(siteCommons, topCategoryName)
	print "this category is analysed..." + topCategoryName
	
	items = pagegenerators.CategorizedPageGenerator(category, recurse=False)
	for item in items:
			
		ready = True
		
		title = item.title()
		titleBis = title.replace(PARIS, "")
		
		# extension control
		ext = titleBis.find(EXTENSION) 
		if ext < 0: 
			ready = False	

		# prefix control
		pref = titleBis.find(PREFIX)
		if pref != 0:
			ready = False

		if ready == True:
			
			print str(count)

			# General case
			word = titleBis[len(PREFIX):ext]
			word = word.replace (u"‐", "-")
			print word

			# Marginal case in the goal to manage "à-propos" => "à propos"
			wordBis = word.replace ("-", " ")
			print wordBis

			wikt = pywikibot.Page(siteWiktionary, word)
			wiktBis = pywikibot.Page(siteWiktionary, wordBis)
			
			# if "à-propos" does not exist we try "à propos"
			if len(wikt.text) == 0:
				wikt = wiktBis	
				word = wordBis
			
			# existence test of the correspondent article (red link or not)
			if len(wikt.text) > 0:   

				# test if the template is already used or not
				#templates = siteWiktionary.pagetemplates(wikt, namespaces=None, step=None, total=None, content=False)
				if wikt.text.find(TEMPLATE) < 0:			
 					try:
    						val=wordsDone.index(word)
					except ValueError:
						count = count + 1 
   						wordsDone.append(word)
						print ("***** template is non used ***** : " + word)
						result += "# [[" + word + "]] : " + "[[:Commons:" + title + "|" + title + "]]" + "\n" 
				else:
					print ("template already used : " + word)
			else: 
				print ("this article does not exist on fr.wiktionary : " + word)
		else:
			print ("we ignore this file : " + title)

		print " "		
		print "*********"

	categories = pagegenerators.SubCategoriesPageGenerator(category, recurse=False)
	for cat in categories:
		result = recursiveMethod(cat.title(), result, count)		

	return result	
	
#
# Main
#

count = 0
result = recursiveMethod(topCategoryName, result, count)
page = pywikibot.Page(siteWiktionary, u"Utilisateur:Benoît Prieur/French_pronunciation")
page.text = result
page.save("done")	



