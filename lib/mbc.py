# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import json
import os
from util import *



class MBC:
	MENU_MBC =	[	
		'01|MBC|Y|http://vodmall.imbc.com/util/player/onairurlutil_secure.ashx|http://img.pooq.co.kr/BMS/ChannelImg/MBC_730x411.jpg',
		#'06|MBC|Y|http://vodmall.imbc.com/util/player/OnairUrlUtil_sports_ch2.ashx|',
		'02|MBC 무한도전24|Y|http://vodmall.imbc.com/util/player/onairurlutil_mudo.ashx?type=m|http://img.pooq.co.kr/BMS/ChannelImg/pooqmudo_730x411.jpg',
		'03|MBC 나혼자산다24|Y|http://vodmall.imbc.com/util/player/OnairUrlUtil_MCast.ashx|',
		'04|MBC 해요TV+|Y|http://vodmall.imbc.com/util/player/OnairUrlUtil_Music.ashx|',
		'05|MBC imbc스포츠 Ch|Y|http://vodmall.imbc.com/util/player/OnairUrlUtil_sports_ch1.ashx|',
		#'06|MBC imbc스포츠 Ch2|Y|http://vodmall.imbc.com/util/player/OnairUrlUtil_sports_ch2.ashx|',
		'07|MBC 표준FM|N|sfm|http://img.pooq.co.kr/BMS/ChannelImg/MBCFM_730x411.jpg',
		'08|MBC FM4U|N|mfm|http://img.pooq.co.kr/BMS/ChannelImg/MBCFM4U_730x411.jpg',
		'09|MBC ChannelM|N|chm|' ]

	COOKIE_FILENAME = 'mbc.txt'
	
	# Login
	def DoLogin(self, id, pw):
		url = 'https://member.imbc.com/Login/LoginProcess.aspx'
		params = {	'TemplateID' : 'main',
				'TURL' : '',
				'confirmMsg' : '',
				'IdsafeURL' : '',
				'id' : id,
				'protocol' : 'http',
				'Uid' : id,
				'Password' : pw,
				'loginStay' : 'Y'}
		ret = ''
		cj = cookielib.CookieJar()
		cookieprocessor = urllib2.HTTPCookieProcessor(cj)
		opener = urllib2.build_opener(urllib2.HTTPRedirectHandler, cookieprocessor)
		urllib2.install_opener(opener)
		postdata = urllib.urlencode(params)
		response =urllib2.urlopen(url, postdata )
		for cookie in cj:
			if cookie.name == 'IMBCSession':
				ret = cookie.value
				break
		cj.clear_session_cookies()
		if ret != '':
			logindata = '%s=%s' % ('IMBCSession', ret)
			WriteFile(GetFilename(self.COOKIE_FILENAME), logindata)
		return 
	
	def DoLoginFromSC(self, id, pw):
		try:
			if not os.path.isfile(GetFilename(self.COOKIE_FILENAME)):
				data = self.DoLogin(id, pw)
		except Exception as e:
			print(e)
			pass

	# List
	def GetChannelList(self, includeURL = False):
		list = []
		for item in self.MENU_MBC:
			temp = item.split('|')
			info = {}
			info['id'] = temp[0]
			info['title'] = temp[1]
			info['isTv'] = temp[2]
			info['param'] = temp[3]
			info['img'] = temp[4]
			info['summary'] = ''
			if includeURL == True:
				if info['isTv'] == 'Y':
					info['url'] = self.GetURLTV(info['param'])
				else:
					info['url'] = self.GetURLRadio(info['param'])
			list.append(info)
		return list
	
	# URL
	def GetURLWithLocalID(self, id):
		for item in self.MENU_MBC:
			temp = item.split('|')
			if id == temp[0]:
				if temp[2] == 'Y':
					if id == '05' or id == '06':
						return self.GetURLTV(temp[3], 'm')
					else:
						return self.GetURLTV(temp[3])
				else:
					return self.GetURLRadio(temp[3])
				break
	
	def GetURLRadio(self, id):
		url = 'http://miniplay.imbc.com/AACLiveURL.ashx?protocol=M3U8&channel=%s&agent=android&androidVersion=24' % id
		params = {}
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		response = urllib2.urlopen(request)
		data = response.read()
		return data

	def GetURLTV(self, param, type='iphone'):
		url = 'http://m.imbc.com/clone/clonelink.ashx'

		params = {	'type' : type,
				'autoplay' : '0', 
				'dest_url' : param}
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		cookie = ReadFile(GetFilename(self.COOKIE_FILENAME))
		if cookie is not None:
			request.add_header('Cookie', cookie)
		response = urllib2.urlopen(request)
		data = response.read()
		#print(data)
		idx1 = data.find('http')
		idx2 = data.find(']', idx1)
		ret = data[idx1:idx2]
		#ret = ret.replace('500k', '1000k') 안됨
		#ret = ret.replace('onairtv_preview', 'imbc_onairtv')
		#ret = ret.replace('preview_500k', 'onairtv_500k')
		return ret

	# M3U
	def MakeM3U(self, php):
		type = 'MBC'
		str = ''
		for item in self.GetChannelList():
			url = BROAD_URL % (php, type, item['id'])
			tvgid = '%s|%s' % (type, item['id'])
			tvgname = '%s|%s' % (type, item['title'])
			if item['isTv'] == 'Y':
				str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], url)
			else:
				str += M3U_RADIO_FORMAT % (tvgid, tvgname, item['img'], 'RADIO1', item['title'], url)
		return str

