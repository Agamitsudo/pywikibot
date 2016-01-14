# -*- coding: utf-8 -*-
# Usage of .ogg files on fr.wiktionary.py

import sys
import pywikibot

sys.path.insert(0, "/home/benoit/Documents/pywikibot-core/core/pywikibot")

import pagegenerators
import re
import math
	     
siteWiktionary = pywikibot.Site(u'fr', u'wiktionary')
siteWiktionary.login()

simpleName = u"Thésaurus en français"
topCategoryName = u"Catégorie:" + simpleName

new_dict = {}

#
# mainMethod
#
def mainMethod(topCategoryName):

	category = pywikibot.Category(siteWiktionary, topCategoryName)
	print "this category is analysed..." + topCategoryName
	
	for item in category.newest_pages():
		
		year = str(item.oldest_revision.timestamp.year)
		month = str(item.oldest_revision.timestamp.month)
		key =  year + "-" + month

		title = item.title()

		print title + " " + key

		if new_dict.get(key) == None:
			new_dict[key] = 1;
		else:
			new_dict[key] = new_dict[key] + 1;	
	
	#https://fr.wiktionary.org/wiki/Module:Diagramme (documentation)
	diagram = u"{{ #invoke:Diagramme | histogramme | largeur = 1000 | hauteur = 550 \n| groupe 1 = "
	values = u""
	legends = u""

	for y in range(2004, 2016):
		for m in range (1, 13):

			k = str(y) + "-" + str(m)

			if new_dict.get(k) == None:
				values = values + "0"
			else:
				values = values + str(new_dict.get(k))
			
			if m == 1:			
				legends = legends + str(y)			
			
			if m != 12 or y != 2015:
				values = values + ":"
				legends = legends + ":"

	return diagram + values + u"\n| couleurs = green \n| légendes = " + legends + u"\n| noms = Nombre de " + simpleName + u" créés ce mois }}"
#
# Main
#

result = mainMethod(topCategoryName)
page = pywikibot.Page(siteWiktionary, u"Utilisateur:Benoît Prieur/" + simpleName)
page.text = result
page.save("done")	



