# -*- coding: utf-8 -*-
import os
import urllib
import xbmcplugin, xbmcgui, xbmcaddon
from urlparse import parse_qs

__addon__ = xbmcaddon.Addon()
__language__  = __addon__.getLocalizedString
sys.path.append(os.path.join( xbmc.translatePath( __addon__.getAddonInfo('path') ), 'resources', 'lib' ))
from logic import *

def Main():
	for menu in TOP_MENU_LIST:
		tmp = menu.split('|')
		addDir(tmp[1], None, None, True, 'ChannelList', tmp[0], None, None)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ChannelList(p):
	type = p['param']
	list = GetChannelList(type)
	for item in list:
		param = item['id']
		isUrl = 'N'
		if 'url' in item:
			param = item['url']
			isUrl = 'Y'
		infoLabels = {"mediatype":"episode","label":item['title'] ,"title":item['title'],"plot":item['summary']}
		addDir(item['title'], item['img'], infoLabels, False, 'PlayVideo', type, param, isUrl)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo( p ):
	LOG('PlayVideo : %s' % p)
	type = p['param']
	id = p['param2']
	isUrl = p['pageNo']
	if isUrl == 'Y':
		url = id
	else:
		url = GetURL(type, id)
		if url is None:
			addon_noti('Can\'t see')
			return
	LOG('PLAYVIDEO %s' % url)
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

#########################
def addDir(title, img, infoLabels, isFolder, mode, param, param2, pageNo):
	params = {'mode': mode, 'param':param, 'param2':param2, 'pageNo':pageNo}
	url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
	listitem = xbmcgui.ListItem(title, thumbnailImage=img)
	if infoLabels: listitem.setInfo(type="Video", infoLabels=infoLabels)
	if not isFolder: listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder)

def addon_noti(sting):
	try:
		dialog = xbmcgui.Dialog()
		dialog.notification(__addon__.getAddonInfo('name'), sting)
	except:
		LOG('addonException: addon_noti')

def get_params():
	p = parse_qs(sys.argv[2][1:])
	for i in p.keys():
		p[i] = p[i][0]
	return p


params = get_params()
try:
	mode = params['mode']
except:
	mode = None
if mode == None: Main()
elif mode == 'ChannelList': ChannelList(params)
elif mode == 'PlayVideo': PlayVideo(params)
else: LOG('NOT FUNCTION!!')
