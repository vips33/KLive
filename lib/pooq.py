# -*- coding: utf-8 -*-
import urllib, urllib2
import json 
import os
import pickle
from util import *

class POOQ:
	COOKIE_FILENAME = 'pooq.txt'

	def __init__( self ):
		self.DEVICE_TYPE_ID = 'pc'
		self.MARKET_TYPE_ID = 'generic'
		self.DEVICE_MODEL_ID = 'none'
		self.DRM = 'WC'
		self.COUNTRY = 'KOR'
		self.API_ACCESS_CREDENTIAL = 'EEBE901F80B3A4C4E5322D58110BE95C'
		self.LIMIT = 30

	# 로그인
	def DoLogin( self, user_id, user_pw ):
		credential = ''
		try:
			url = 'https://wapie.pooq.co.kr/v1/login30/'
			params = { 'deviceTypeId' : self.DEVICE_TYPE_ID,
					   'marketTypeId' : self.MARKET_TYPE_ID,
					   'apiAccessCredential' : self.API_ACCESS_CREDENTIAL,
					   'drm' : self.DRM,
					   'country' : self.COUNTRY,
					   'credential' : 'none',
					   'mode' : 'id',
					   'id' : user_id,
					   'password' : user_pw }
			postdata = urllib.urlencode( params )
			request = urllib2.Request('%s?%s' % (url, postdata), '')
			response = urllib2.urlopen(request)
			data = json.load(response, encoding='utf8')
			credential = data['result']['credential']
		except Exception as e:
			#print(e)       
			return None
		return credential

	def DoLoginFromSC(self, id, pw):
		try:
			if not os.path.isfile(GetFilename(self.COOKIE_FILENAME)):
				ret = self.DoLogin(id, pw)
				if ret is not None: WriteFile(GetFilename(self.COOKIE_FILENAME), ret)
		except Exception as e:
			print(e)
			pass

	# 채널 목록
	def GetChannelList( self ):
		try:
			url = 'http://wapie.pooq.co.kr/v1/livesgenresort30/' 
			params = { 'deviceTypeId' : self.DEVICE_TYPE_ID,
					   'marketTypeId' : self.MARKET_TYPE_ID,
					   'apiAccessCredential' : self.API_ACCESS_CREDENTIAL,
					   'drm' : self.DRM,
					   'country' : self.COUNTRY,
					   'authType' : 'cookie',
					   'orderby' : 'g', #'h',
					   'credential' : 'none' }
			postdata = urllib.urlencode( params )
			request = urllib2.Request('%s?%s' % (url, postdata))
			response = urllib2.urlopen(request)
			data = json.load(response, encoding='utf8')
			result = data['result']['list']
			list = []
			for lists in result:
				for item in lists['list']:
					info = {}
					info['title'] = item['channelTitle']
					info['id'] = item['id']
					info['img'] = item['image']
					info['isRadio'] = item['isRadio']
					info['summary'] = item['title']
					list.append(info)
			return list
		except Exception as e:
			print(e)
			result = []
		return result

	# URL
	def GetGUID( self ):
		import hashlib
		m = hashlib.md5()

		def GenerateID( media ):
			from datetime import datetime
			requesttime = datetime.now().strftime('%Y%m%d%H%M%S')
			randomstr = GenerateRandomString(5)
			uuid = randomstr + media + requesttime
			return uuid

		def GenerateRandomString( num ):
			from random import randint
			rstr = ""
			for i in range(0,num):
				s = str(randint(1,5))
				rstr += s
			return rstr

		uuid = GenerateID("POOQ")
		m.update(uuid)

		return str(m.hexdigest())



	
	def GetLiveQualityList( self, channelID ):
		try:
			url = 'http://wapie.pooq.co.kr/v1/lives30/%s' % channelID
			params = { 'deviceTypeId' : self.DEVICE_TYPE_ID,
					   'marketTypeId' : self.MARKET_TYPE_ID,
					   'apiAccessCredential' : self.API_ACCESS_CREDENTIAL,
					   'drm' : self.DRM,
					   'country' : self.COUNTRY,
					   'credential' : 'none' }
			postdata = urllib.urlencode( params )
			request = urllib2.Request('%s?%s' % (url, postdata))
			response = urllib2.urlopen(request)
			data = json.load(response, encoding='utf8')
			result = data['result']['qualityList'][0]['quality']
		except Exception as e:
			print(e)
			result = None
		return result


	def GetURL( self, channelID, quality):
		surl = ''
		result = None
		try:
			credential = ReadFile(GetFilename(self.COOKIE_FILENAME))
			quality_list = self.GetLiveQualityList(channelID)
			if not quality in quality_list: quality = quality_list[0]

			url = 'http://wapie.pooq.co.kr/v1/lives30/%s/url' % channelID
			params = { 'deviceTypeId' : self.DEVICE_TYPE_ID,
					   'marketTypeId' : self.MARKET_TYPE_ID,
					   'deviceModelId' : 'Macintosh',
					   'drm' : self.DRM,
					   'country' : self.COUNTRY,
					   'authType' : 'cookie',
					   'guid' : self.GetGUID(),
					   'lastPlayId' : 'none',
					   'credential' : credential,
					   'quality' : quality }
			postdata = urllib.urlencode( params )
			request = urllib2.Request('%s?%s' % (url, postdata))
			response = urllib2.urlopen(request)
			data = json.load(response, encoding='utf8')
			surl = data['result']['signedUrl']
			###############
			filename = GetFilename('pooq_url.txt')
			if surl is None:
				if os.path.isfile(filename):
					file = open(filename, 'rb')
					urls = pickle.load(file)
					surl = urls[channelID] if channelID in urls else None
					surl = urls['recent'] if surl is None and 'recent' in urls else surl
					file.close()
			else:
				if os.path.isfile(filename):
					file = open(filename, 'rb')
					urls = pickle.load(file)
					file.close()
				else: urls = {}
				urls[channelID] = surl
				urls['recent'] = surl
				file = open(filename, 'wb')
				pickle.dump(urls, file)
				file.close()
			return surl
			"""
			if surl is not None:
				request = urllib2.Request(surl)
				response = urllib2.urlopen(request)
				data = response.read()
				idx1 = surl.find('radio.m3u8')
				if idx1 != -1:
					data = data.replace('live.m3u8', surl[:idx1] + 'live.m3u8')
				return data
			"""
		except Exception as e:
			pass
		return surl

	# M3U
	def MakeM3U(self, php):
		type = 'POOQ'
		str = ''
		
		list = self.GetChannelList()
		for item in list:
			url = BROAD_URL % (php, type, item['id'])
			tvgid = '%s|%s' % (type, item['id'])
			tvgname = '%s|%s' % (type, item['title'])
			if item['isRadio'] == 'N':
				str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], url)
			else:
				str += M3U_RADIO_FORMAT % (tvgid, tvgname, item['img'], '%s RADIO' % type, item['title'], url)
		return str

	# EPG
	def MakeEPG(self, filename):
		list = self.GetChannelList()
		import datetime
		startDate = datetime.datetime.now()
		startParam = startDate.strftime('%Y/%m/%d')
		endDate = startDate + datetime.timedelta(days=2)
		endParam = endDate.strftime('%Y/%m/%d')

		str = ''
		for item in list:
			str += '\t<channel id="POOQ|%s">\n' % item['id']
			str += '\t\t<display-name>POOQ|%s</display-name>\n' % item['title']
			str += '\t</channel>\n'

			url = 'http://wapie.pooq.co.kr/v1/epgs30/%s/?deviceTypeId=pc&marketTypeId=generic&apiAccessCredential=EEBE901F80B3A4C4E5322D58110BE95C&drm=WC&country=KOR&offset=0&limit=1000&startTime=%s+00:00&pooqzoneType=none&credential=none&endTime=%s+00:00' % (item['id'], startParam, endParam)
			
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			data = json.load(response, encoding='utf8')
			currentDate = startDate
			for epg in data['result']['list']:
				startTime = '%s%s' % (epg['startDate'].replace('-',''), epg['startTime'].replace(':', ''))
				temp_startTime = int(epg['startTime'].replace(':', ''))
				temp_endTime = int(epg['endTime'].replace(':', ''))
				if temp_startTime > temp_endTime and epg['startDate'].replace('-','') == currentDate.strftime('%Y%m%d'): #전날에서 넘어온 경우 내일이 되버림.
					currentDate = currentDate + datetime.timedelta(days=1)
				currentDateStr = currentDate.strftime('%Y%m%d')
				endTime = '%s%s' % (currentDateStr, epg['endTime'].replace(':', ''))
				str += '\t<programme start="%s00 +0900" stop="%s00 +0900" channel="POOQ|%s">\n' %  (startTime, endTime, item['id'])
				#str += '\t\t<title lang="kr"><![CDATA[%s]]></title>\n' % epg['programTitle']
				str += '\t\t<title lang="kr">%s</title>\n' % epg['programTitle'].replace('<',' ').replace('>',' ')
				
				age_str = '%s세 이상 관람가' % epg['age'] if epg['age'] != '0' else '전체 관람가'
				str += '\t\t<rating system="KMRB"><value>%s</value></rating>\n' % age_str
				desc = '등급 : %s\n' % age_str

				staring = epg['programStaring'].strip() if 'programStaring' in epg and epg['programStaring'] is not None else None
				if staring is not None and staring != '':
					temp = staring.split(',')
					if len(temp) > 0:
						str += '\t\t<credits>\n'
						for actor in temp:
							str += '\t\t\t<actor>%s</actor>\n' % actor.strip().replace('<',' ').replace('>',' ')
						str += '\t\t</credits>\n'
						desc += '출연 : %s\n' % epg['programStaring'] 
				if 'programSummary' in epg and epg['programSummary'] is not None:
					#desc += epg['programSummary'].replace('<','&lt').replace('>','&gt')
					desc += epg['programSummary']
				str += '\t\t<desc lang="kr">%s</desc>\n' % desc.strip().replace('<',' ').replace('>',' ')
				str += '\t</programme>\n'
		return str
