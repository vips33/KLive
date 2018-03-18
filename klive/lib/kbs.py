# -*- coding: utf-8 -*-
import urllib, urllib2
import json
from util import *

class KBS:
	MENU_KBS =	[	
		'01|KBS 1TV|Y|http://hls.live.kbskme.gscdn.com/1tv/_definst_/1tv_5.stream/playlist.m3u8|11',
		'02|KBS 2TV|Y|http://hls.live.kbskme.gscdn.com/2tv/_definst_/2tv_5.stream/playlist.m3u8|12',
		'03|KBS 24뉴스|Y|http://hls.live.kbskme.gscdn.com/news24/_definst_/news24_800.stream/playlist.m3u8|81',
		'04|KBSN Sports|Y|http://hls.live.kbskme.gscdn.com/kbsn_sports/_definst_/kbsn_sports_5.stream/playlist.m3u8|N95',
		'05|KBSN Drama|Y|http://hls.live.kbskme.gscdn.com/kbsn_drama/_definst_/kbsn_drama_5.stream/playlist.m3u8|N91',
		'06|KBSN Joy|Y|http://hls.live.kbskme.gscdn.com/kbsn_joy/_definst_/kbsn_joy_5.stream/playlist.m3u8|N92',
		'07|KBSN W|Y|http://hls.live.kbskme.gscdn.com/kbsn_wtv/_definst_/kbsn_wtv_5.stream/playlist.m3u8|N94',
		'08|KBSN Kids|Y|http://hls.live.kbskme.gscdn.com/kbsn_kids/_definst_/kbsn_kids_5.stream/playlist.m3u8|N96',
		'09|KBSN Life|Y|http://hls.live.kbskme.gscdn.com/kbsn_prime/_definst_/kbsn_prime_5.stream/playlist.m3u8|N93',
		#'10|IDEAK 쇼핑|Y|http://hls.live.mesnvod.gscdn.com/nvod009/definst/nvod009.stream/playlist.m3u8',
		'11|KBS 1Radio|N|21|N',
		'12|KBS 2Radio Happy FM|N|22|N',
		'13|KBS 2Radio Happy FM 보라|B|22|Y',
		'14|KBS 3Radio|N|23|N',
		'15|KBS 1FM Classic FM|N|24|N',
		'16|KBS 2FM Cool FM|N|25|N',
		'17|KBS 2FM Cool FM 보라|B|25|Y',
		'18|KBS 한민족방송|N|26|N',
		'19|KBS WorldRadio|N|I92|N']

	# LIST
	def GetChannelList(self, includeURL = False):
		list = []
		for item in self.MENU_KBS:
			temp = item.split('|')
			info = {}
			info['id'] = temp[0]
			info['title'] = temp[1]
			info['isTv'] = temp[2]
			info['param'] = temp[3]
			
			if info['isTv'] == 'Y':
				info['kbs_id'] = temp[4]
			else:
				info['kbs_id'] = info['param']
				info['isBora'] = temp[4]
			info['img'] = 'http://img.kbs.co.kr/kplayer/WebV4/assets/images/channel_logo/large/channel_%s.png' % info['kbs_id']
			info['summary'] = ''
			if includeURL == True:
				if info['isTv'] == 'Y':
					info['url'] = self.GetURLTV(info['param'])
				else:
					info['url'] = self.GetURLRadio(info['param'], info['isBora'])
				
			list.append(info)
		return list
	

	#URL
	def GetURLWithLocalID(self, id):
		for item in self.MENU_KBS:
			temp = item.split('|')
			if id == temp[0]:
				if temp[2] == 'Y':
					return self.GetURLTV(temp[3])
				else:
					return self.GetURLRadio(temp[3], temp[4])
				break

	def GetURLRadio(self, id, is_bora='N'):
		url = 'http://kongapi.kbs.co.kr/api/kp_cms/live_stream'
		params = {	
				#'welcome' : '1_1984_2_1_0_2',
				#'beta' : '0',
				'is_bora' : is_bora,
				'channel_code' : id,
				'device_type' : 'android_phone', #android_pad
				}
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		response = urllib2.urlopen(request)
		data = json.load(response, encoding='utf8')
		ret = None if 'real_service_url' not in data else data['real_service_url']
		return ret


	def GetURLTV(self, param):
		url = 'http://kapi.kbs.co.kr/api/kp_cms/live_stream'
		params = {	
				#'service_url' : 'http://hls.live.kbskme.gscdn.com/2tv/_definst_/2tv_3.stream/playlist.m3u8',
				'service_url' : param,
				#'beta' : '0',
				'device_type' : 'android_phone',
				}
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		
		response = urllib2.urlopen(request)
		data = json.load(response, encoding='utf8')
		ret = None if 'real_service_url' not in data else data['real_service_url']
		return ret

	# M3U
	def MakeM3U(self, php):
		type = 'KBS'
		str = ''
		for item in self.GetChannelList():
			url = BROAD_URL % (php, type, item['id'])
			tvgid = '%s|%s' % (type, item['id'])
			tvgname = '%s|%s' % (type, item['title'])
			if item['isTv'] == 'Y':
				str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], url)
			else :
				str += M3U_RADIO_FORMAT % (tvgid, tvgname, item['img'], 'RADIO1', item['title'], url)				
		return str

