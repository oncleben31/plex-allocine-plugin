# -*- coding: utf-8 -*-
'''
Created on June 18, 2009

@summary: A Plex Media Server plugin that integrates trailers of French web site Allocine.
@version: 0.2
@author: Oncleben31
'''

# Import the parts of the Plex Media Server Plugin API we need
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *


# Plugin parameters
PLUGIN_TITLE						= "Allociné"					# The plugin Title
PLUGIN_PREFIX   					= "/video/Allocine"				# The plugin's contextual path within Plex
PLUGIN_HTTP_CACHE_INTERVAL			= 0

# Plugin Icons
PLUGIN_ICON_DEFAULT					= "icon-default.png"
PLUGIN_ICON_BA_ANEPASMANQUER		= "icon-default.png"
PLUGIN_ICON_BA_CETTESEMAINE			= "icon-default.png"
PLUGIN_ICON_BA_ALAFFICHE			= "icon-default.png"
PLUGIN_ICON_BA_PROCHAINEMENT		= "icon-default.png"
PLUGIN_ICON_PREFS					= "icon-default.png"


# Plugin Artwork
PLUGIN_ARTWORK						= "art-default.jpg"

#Some URLs for the script
PLUGIN_URL_BA_ANEPASMANQUER			= "http://rss.allocine.fr/ac/bandesannonces/anepasmanquer"
PLUGIN_URL_BA_CETTESEMAINE			= "http://rss.allocine.fr/ac/bandesannonces/cettesemaine"
PLUGIN_URL_BA_ALAFFICHE				= "http://rss.allocine.fr/ac/bandesannonces/alaffiche"
PLUGIN_URL_BA_PROCHAINEMENT			= "http://rss.allocine.fr/ac/bandesannonces/prochainement"



####################################################################################################

def Start():
	# Register our plugins request handler
	Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE.decode('utf-8'), PLUGIN_ICON_DEFAULT, PLUGIN_ARTWORK)
	
	# Add in the views our plugin will support
	
	Plugin.AddViewGroup("Menu", viewMode="InfoList", mediaType="items")
	
	# Set up our plugin's container
	
	#MediaContainer.title1 = PLUGIN_TITLE
	MediaContainer.title1 = PLUGIN_TITLE.decode('utf-8')
	MediaContainer.viewGroup = "Menu"
	MediaContainer.art = R(PLUGIN_ARTWORK)
	
	# Configure HTTP Cache lifetime
	
#	HTTP.SetCacheTime(PLUGIN_HTTP_CACHE_INTERVAL)

####################################################################################################
# The plugin's main menu. 

def MainMenu():
	dir = MediaContainer(art = R(PLUGIN_ARTWORK), viewGroup = "Menu")
	dir.Append(Function(DirectoryItem(ListeANePasManquer, title=L("ANEPASMANQUER_MENU_TITLE"), thumb=R(PLUGIN_ICON_BA_ANEPASMANQUER), summary=L("ANEPASMANQUER_MENU_SUMMARY"))))
	dir.Append(Function(DirectoryItem(ListeCetteSemaine, title=L("CETTESEMAINE_MENU_TITLE"), thumb=R(PLUGIN_ICON_BA_CETTESEMAINE), summary=L("CETTESEMAINE_MENU_SUMMARY"))))
	dir.Append(Function(DirectoryItem(ListeALAffiche, title=L("ALAFFICHE_MENU_TITLE"), thumb=R(PLUGIN_ICON_BA_ALAFFICHE), summary=L("ALAFFICHE_MENU_SUMMARY"))))
	dir.Append(Function(DirectoryItem(ListeProchainement, title=L("PROCHAINEMENT_MENU_TITLE"), thumb=R(PLUGIN_ICON_BA_PROCHAINEMENT), summary=L("PROCHAINEMENT_MENU_SUMMARY"))))
		 
	return dir

####################################################################################################
# The A Ne pas Manquer menu
def TraiteFluxRSS(urlFluxRSS, titreFluxRSS):
	dir = MediaContainer(art = R(PLUGIN_ARTWORK), viewGroup = "Menu", title2 = titreFluxRSS)
		
	fluxXML = XML.ElementFromURL(urlFluxRSS, encoding="iso-8859-1")
	
	for c in fluxXML.xpath("//item"):
		titleEtSubtitle = c.find('title').text.encode("iso-8859-1").rsplit(' - ',1)
		title = titleEtSubtitle[0]
		subtitle = titleEtSubtitle[1]
		thumb = c.find('enclosure').get('url')
		
		url = "http://www.allocine.fr/video/player_gen_cmedia" + c.find('link').text.rsplit("player_gen_cmedia")[1]
		Log("url %s" % (url.encode("utf8")))
		
		dir.Append(WebVideoItem(url, title=title.decode("utf-8"), subtitle=subtitle.decode("utf-8"), thumb=thumb))    
	
	return dir


####################################################################################################
# The A Ne pas Manquer menu
def ListeANePasManquer(sender):
	dir = TraiteFluxRSS(PLUGIN_URL_BA_ANEPASMANQUER, L("ANEPASMANQUER_MENU_TITLE"))
	return dir

####################################################################################################
# The Cette Semaine menu
def ListeCetteSemaine(sender):
	dir = TraiteFluxRSS(PLUGIN_URL_BA_CETTESEMAINE, L("CETTESEMAINE_MENU_TITLE"))
	return dir

####################################################################################################
# The A L'Affichie menu
def ListeALAffiche(sender):
	dir = TraiteFluxRSS(PLUGIN_URL_BA_ALAFFICHE, L("ALAFFICHE_MENU_TITLE"))
	return dir

####################################################################################################
# The Prochainement menu
def ListeProchainement(sender):
	dir = TraiteFluxRSS(PLUGIN_URL_BA_PROCHAINEMENT, L("PROCHAINEMENT_MENU_TITLE"))
	return dir

####################################################################################################





