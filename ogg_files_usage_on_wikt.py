# -*- coding: utf-8 -*-
# Usage of .ogg files on fr.wiktionary.py

import sys
import pywikibot

sys.path.insert(0, "/home/benoit/Documents/pywikibot-core/core/pywikibot")

import pagegenerators
import re
import math

EXTENSION = ".ogg"
PREFIXE = "File:Fr-"
PARIS = "Paris--"

siteWiktionary = pywikibot.Site(u'fr', u'wiktionary')
siteWiktionary.login()

siteCommons = pywikibot.Site(u'commons', u'commons')
siteCommons.login()

nomCategorieSuperieure = u"Category:French pronunciation"

resultat = "La liste ci-dessous regroupe les fichiers .ogg existants sur WikiCommons mais non repris sur les articles du Wiktionnaire correspondant. Ils sont tous issus de l'arborescence [[:Commons:" + nomCategorieSuperieure + "]]. Si vous utilisez un fichier .ogg dans son article, merci de barrer la ligne correspondante ci-dessous.\n\n"

#
# TraitementRecursif
#
def TraitementRecursif(nomCategorieSuperieure, resultat):

	categorie = pywikibot.Category(siteCommons, nomCategorieSuperieure)
	print "Categorie en cours de traitement..." + nomCategorieSuperieure
	
	items = pagegenerators.CategorizedPageGenerator(categorie, recurse=False)
	for item in items:
			
		ready = True
		
		titre = item.title()
		titreBis = titre.replace(PARIS, "")
		
		# Contrôle de l'extension
		ext = titreBis.find(EXTENSION) 
		if ext < 0: 
			ready = False	

		# Contrôle du préfixe
		pref = titreBis.find(PREFIXE)
		if pref != 0:
			ready = False

		# On ne traite pas les cas à plusieurs "-"
		num = titreBis.count('-')
		if num != 1:
			ready = False

		if ready == True:

			mot = titreBis[len(PREFIXE):ext]
			
			wikt = pywikibot.Page(siteWiktionary, mot)
			if len(wikt.text) > 0: # Test de l'existence (lien rouge ou non)  
				if wikt.text.find(u"{{écouter|") < 0: # Recherche du modèle (on ne teste pas audio=)
					print ("non-utilisation du modele : " + mot)
					resultat += "# [[" + mot + "]] : " + "[[:Commons:" + titre + "|" + titre + "]]" + "\n" 
				else:
					print ("modele deja en place : " + mot)
			else: 
				print ("l'article n'existe pas : " + mot)
		else:
			print ("on ignore ce fichier : " + titre)

	categories = pagegenerators.SubCategoriesPageGenerator(categorie, recurse=False)
	for cat in categories:
		resultat = TraitementRecursif(cat.title(), resultat)		

	return resultat	
	
#
# Principal
#

resultat = TraitementRecursif(nomCategorieSuperieure, resultat)
page = pywikibot.Page(siteWiktionary, u"Utilisateur:Benoît Prieur/French_pronunciation")
page.text = resultat
page.save("MAJ : prise en compte des Paris--")	



