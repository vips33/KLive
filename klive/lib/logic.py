# -*- coding: utf-8 -*-
def LOG(str):
	try :
		import xbmc, xbmcaddon
		try:
			xbmc.log("[%s-%s]: %s" %(xbmcaddon.Addon().getAddonInfo('id'), xbmcaddon.Addon().getAddonInfo('version'), str), level=xbmc.LOGNOTICE)
			log_message = str.encode('utf-8', 'ignore')
		except:
			log_message = 'KLIVE Exception'
		xbmc.log("[%s-%s]: %s" %(xbmcaddon.Addon().getAddonInfo('id'), xbmcaddon.Addon().getAddonInfo('version'), log_message), level=xbmc.LOGNOTICE)
		return
	except:
		pass

	try:
		Log(str)
		return
	except:
		pass


def GetSetting(type):
	try:
		import xbmc, xbmcaddon
		ret = xbmcaddon.Addon().getSetting(type)
		if type == 'POOQ_QUALITY':
			POOQ_QUALITY_LIST = ['5000', '2000', '1000', '500']
			ret = POOQ_QUALITY_LIST[int(ret)]
		elif type == 'TVING_LOGIN_TYPE':
			TVING_LOGIN_TYPE = ['CJONE', 'TVING']
			ret = TVING_LOGIN_TYPE[int(ret)]
		elif type == 'TVING_QUALITY':
			TVING_QUALITY_LIST = ['stream50', 'stream40', 'stream30']
			ret = TVING_QUALITY_LIST[int(ret)]
		elif type == 'OKSUSU_QUALITY':
			OKSUSU_QUALITY_LIST = ['FHD', 'HD', 'SD']
			ret = OKSUSU_QUALITY_LIST[int(ret)]
		elif type == 'OLLEH_QUALITY':
			OLLEH_QUALITY_LIST = ['4000', '2000', '1000']
			ret = OLLEH_QUALITY_LIST[int(ret)]
		return ret
	except:
		pass

	
	try:
		ret = Prefs[type]
		return ret
	except:
		pass


from kbs import *
from mbc import *
from sbs import *
from pooq import *
from tving import *
from oksusu import *
from olleh import *
from videoportal import *
from everyon import *
from radio import *
from util import *

TOP_MENU_LIST = ['KBS|KBS', 'MBC|MBC', 'SBS|SBS', 'POOQ|푹', 'TVING|티빙', 'OKSUSU|옥수수', 'OLLEH|올레', 'VIDEOPORTAL|비디오포털', 'EVERYON|에브리온', 'TVING_VOD|티빙 정주행채널', 'RADIO1|라디오 1', 'RADIO2|라디오 2' ]

def GetChannelList(type):
	if type == 'KBS': list = KBS().GetChannelList()
	if type == 'MBC': list = MBC().GetChannelList()
	if type == 'SBS': list = SBS().GetChannelList()
	if type == 'POOQ': list = POOQ().GetChannelList()
	if type == 'TVING': list = TVING().GetChannelList(0)
	if type == 'TVING_VOD': list = TVING().GetChannelList(1)
	if type == 'OKSUSU': list = OKSUSU().GetChannelList()
	if type == 'OLLEH': list = OLLEH().GetChannelList()
	if type == 'VIDEOPORTAL': list = VIDEOPORTAL().GetChannelList()
	if type == 'EVERYON': list = EVERYON().GetChannelList()
	if type == 'RADIO1': list = RADIO1().GetChannelList()
	if type == 'RADIO2': list = RADIO2().GetChannelList()
	return list


def GetURL(type, id):
	if type == 'KBS':
		ret = KBS().GetURLWithLocalID(id)
	elif type == 'MBC':
		MBC().DoLoginFromSC(GetSetting('MBC_ID'), GetSetting('MBC_PW'))
		ret = MBC().GetURLWithLocalID(id)
	elif type == 'SBS': 
		#SBS().DoLoginFromSC(SBS_ID, SBS_PW)
		ret = SBS().GetURL(id)
	elif type == 'POOQ': 
		POOQ().DoLoginFromSC(GetSetting('POOQ_ID'), GetSetting('POOQ_PW'))
		ret = POOQ().GetURL(id, GetSetting('POOQ_QUALITY'))
	elif type == 'TVING' or type == 'TVING_VOD':
		TVING().DoLoginFromSC(GetSetting('TVING_ID'), GetSetting('TVING_PW'), GetSetting('TVING_LOGIN_TYPE'))
		ret = TVING().GetURL(id, GetSetting('TVING_QUALITY'))
	elif type == 'OKSUSU':
		OKSUSU().DoLoginFromSC(GetSetting('OKSUSU_ID'), GetSetting('OKSUSU_PW'))
		ret = OKSUSU().GetURLFromSC(id, GetSetting('OKSUSU_QUALITY'))
	elif type == 'OLLEH':
		OLLEH().DoLoginFromSC(GetSetting('OLLEH_ID'), GetSetting('OLLEH_PW'))
		ret = OLLEH().GetURLFromSC(id, GetSetting('OLLEH_QUALITY'))
	elif type == 'VIDEOPORTAL':
		ret = VIDEOPORTAL().GetURL(id)
	elif type == 'EVERYON': 
		ret = EVERYON().GetURLFromSC(id)
	return ret
