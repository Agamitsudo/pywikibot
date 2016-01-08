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
	
#
# Main
#

result = ""
page = pywikibot.Page(siteWiktionary, u"Utilisateur:Benoît Prieur/French_pronunciation")
text = page.text

links = siteWiktionary.pagelinks(page, namespaces=None, follow_redirects=False, step=None, total=None, content=False)
for link in links: 

	print " *************** " 
	
	linkTitle = link.title()
	print linkTitle

	# [[Aigurande]] : [[:Commons:File:Fr-Paris--Aigurande.ogg|File:Fr-Paris--Aigurande.ogg]]
	index = text.find(linkTitle)
	index2 = text.find(u"|", index)
	oggfile = text[index+len(linkTitle):index2]
	oggfile = oggfile.replace(u"]] : [[:Commons:File:", "")
	print oggfile

	templates = siteWiktionary.pagetemplates(link, namespaces=None, step=None, total=None, content=False)
	
