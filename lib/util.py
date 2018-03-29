# -*- coding: utf-8 -*-
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

M3U_FORMAT = '#EXTINF:-1 tvg-id=\"%s\" tvg-name=\"%s\" tvg-logo=\"%s\" group-title=\"%s\",%s\n%s\n'
M3U_RADIO_FORMAT = '#EXTINF:-1 tvg-id=\"%s\" tvg-name=\"%s\" tvg-logo=\"%s\" group-title=\"%s\" radio=\"true\",%s\n%s\n'
BROAD_URL = '%s?mode=url&type=%s&id=%s'

try:
	from io import open
except:
	pass

def ReadFile(filename):
	try:
		with open(filename, "r") as f:
			data = f.read()
		f.close()
	except Exception as e:
		#print(e)
		data = None
	return data

def WriteFile(filename, data ):
	try:
		#with open(filename, "w", encoding='utf8') as f:
		with open(filename, "w") as f:
			f.write( unicode(data) )
		f.close()
		return
	except Exception as e:
		#print('W11:%s' % e)
		pass
	try:
		with open(filename, "w", encoding='utf8') as f:
		#with open(filename, "w") as f:
			f.write( data )
		f.close()
		return
	except Exception as e:
		#print('W22:%s' % e)
		pass

def GetFilename(filename):
	ret = filename
	try:
		import xbmc, xbmcaddon, os
		profile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
		ret = xbmc.translatePath(os.path.join( profile, ret))
		return ret
	except:
		pass

	try:
		temp = Prefs['VERSION']
		import sys, os
		ret = os.path.join( os.getcwd(), filename )
		return ret
	except:
		pass

	try:
		import sys, os
		ret = os.path.join( os.getcwd(), 'data', filename )
		#print(ret)
		return ret
	except:
		pass
