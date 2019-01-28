# -*- coding: utf-8 -*-
# Diagrams for thesaurus fr.wiktionary

import sys

sys.path.insert(0, "/home/benoit/Documents/Projets Python Commons/core")
import pywikibot

sys.path.insert(0, "/home/benoit/Documents/Projets Python Commons/core/pywikibot")
import pagegenerators
import re
import math
import time
	     
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
	global_result_dict = {}

	#
	# ci-dessous on met à zéro le dictionnaire de "2004"-1 jusqu'à "2016-12"
	#
	for yg in range(2004, 2019):
		for mg in range (1, 13):

			kg = str(yg) + "-" + str(mg)
			global_result_dict[kg] = 0

	pages = pagegenerators.CategorizedPageGenerator(category, recurse=False)
	for page in pages:
		
		print "this page is analysed..." + page.title()
		local_dict = {}

		#
		# ci-dessous on met pour chaque mois durant lequel il y a eu au moins un édit, la valeur la plus récente
		#
		for info in page.fullVersionHistory(): # loops from the much recent to the much older
			
			size = len(info.text.encode('utf-8'))

			key = str(info.timestamp.year)  + "-" + str(info.timestamp.month)

			if local_dict.get(key) == None:
				local_dict[key] = size;
				print key + " :" + str(size)
		
		local_result_dict = {}
		last = 0

		#
		# ci-dessous on met pour chaque mois la valeur de fin de mois ou celle du mois précédent
		#
		for y in range(2004, 2019):
			for m in range (1, 13):

				k = str(y) + "-" + str(m)

				if y == 2004 and m == 1:

					local_result_dict[k] = 0 # k == 2004-1 here
					last = 0

				elif local_dict.get(k) != None:

					local_result_dict[k] = local_dict.get(k)
					last = local_result_dict[k]

				elif local_dict.get(k) == None: 

					local_result_dict[k] = last	

		for ygr in range(2004, 2019):
			for mgr in range (1, 13):
				kgr = str(ygr) + "-" + str(mgr)
				global_result_dict[kgr] += local_result_dict[kgr]

	values = u""
	legends = u""

	#
	# ci-dessous on cumule les valeurs pour l'ensemble des thésaurus
	#
	for yf in range(2004, 2019):
		for mf in range (1, 13):

			# ici on "s'arrête" à janvier 2016 : à décaler selon la date de lancement de script
			if yf == 2018 and mf > 1:
				values += "0"
			else:
				kf = str(yf) + "-" + str(mf)
				values += str(global_result_dict.get(kf))

			if mf == 1:			
				legends += str(yf)

			if mf != 12 or yf != 2018:
				values += ":"
				legends += ":"

	diagram = u"{{ #invoke:Diagramme | histogramme | largeur = 1000 | hauteur = 550 \n| groupe 1 = "
			
	diags = diagram + values + u"\n| couleurs = green \n| légendes = " + legends + u"\n| noms = L'évolution du poids global des thésaurus en français au fil du temps }}"
	diags += "\n\n"

	return diags

#
# Main
#

result = mainMethod(topCategoryName)
page = pywikibot.Page(siteWiktionary, u"Utilisateur:Benoît Prieur/SizeTime_" + simpleName)
page.text = result
page.save("done")	



