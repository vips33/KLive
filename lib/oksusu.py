# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import os
import json
import pickle
import time
from util import *

class OKSUSU:
	COOKIE_FILENAME = 'oksusu.txt'

	# Login
	def DoLoginFromSC(self, id, pw):
		if not os.path.isfile(GetFilename(self.COOKIE_FILENAME)):
			self.DoLogin(id, pw)

	def DoLogin(self, user_id, user_pw ):
		try:
			loginData = {}
			url = 'https://www.oksusu.com/user/login'
			params = { 'userId' : user_id,
				'password' : user_pw,
				'loginMode' : '1',
				'rw' : '/',
				'serviceProvide' : '',
				'accessToken' : '' }
			postdata = urllib.urlencode( params )
			request = urllib2.Request(url, postdata)
			response = urllib2.urlopen(request)
			cookie = response.info().getheader('Set-Cookie')
			for c in cookie.split(','):
				c = c.strip()
				if c.startswith('CORN_AC'):
					loginData['t'] = c.split(';')[0]
			if 't' in loginData:
				file = open(GetFilename(self.COOKIE_FILENAME), 'wb')
				pickle.dump(loginData, file)
				file.close()
		except Exception as e:
			pass
		return

	def GetLoginData(self):
		try:
			file = open(GetFilename(self.COOKIE_FILENAME), 'rb')
			login = pickle.load(file)
			file.close()
		except Exception, e:
			#print(e)
			login = []
		return login

	# List
	def GetChannelList(self):
		try:
			result = []
			url = 'http://www.oksusu.com/api/live/organization/list?genreCode=99&orgaPropCode=ALL'
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			data = json.load(response, encoding="utf-8")
			radio = 'N'
			for item in data["channels"]:
				try:
					info = {}
					#if (type == 'LIVE' and item['hlsUrlPhoneSD'] is not None) or (type == 'CH' and item['hlsUrlPhoneSD'] is None):
					info['id'] = item['serviceId']
					if info['id'] == '85': radio = 'Y'
					info['title'] = unicode(item['channelName'])
					info['episode_title'] = item['programs'][0]['programName']
					info['summary'] = info['episode_title']
					info['img'] = 'http://image.oksusu.com:8080/thumbnails/image/0_0_F20/live/logo/387/'+ item['channelImageName']
					info['music_yn'] = radio
					info['adult_yn'] = item['adult_yn']
					if item['erosContent'] != True and info['title'].startswith('ch.') == False:
						result.append(info)
				except:
					pass
		except Exception as e:
			result = []
		return result

	# URL
	def GetURLJSON(self, code):
		try:
			login = self.GetLoginData()
			url = 'http://www.oksusu.com/v/' + code
			request = urllib2.Request(url)
			if login is not None and 't' in login:
				request.add_header('cookie', login['t'])
			#request.add_header('cookie', ' ')
			response = urllib2.urlopen(request)
			data = response.read()
			idx1 = data.find('contentsInfo:') +14
			idx2 = data.find('|| {}')-1
			data = data[idx1:idx2]
			js = json.loads(data)
			return js
		except Exception as e:
			print(e)
		return

	def GetURL(self, code):
		try:
			js = self.GetURLJSON(code)
			info = {}
			info['FHD'] = js['streamUrl']['hlsUrlPhoneFHD'] if 'hlsUrlPhoneFHD' in js['streamUrl'] else None
			info['HD'] = js['streamUrl']['hlsUrlPhoneHD'] if 'hlsUrlPhoneHD' in js['streamUrl'] else None
			info['SD'] = js['streamUrl']['hlsUrlPhoneSD'] if 'hlsUrlPhoneSD' in js['streamUrl'] else None
			info['AUTO'] = js['streamUrl']['hlsUrlAUTO'] if 'hlsUrlAUTO' in js['streamUrl'] else None
			info['PCFHD'] = js['streamUrl']['hlsUrlPcFHDAuto'] if 'hlsUrlPcFHDAuto' in js['streamUrl'] else None
			if 'nvodHlsUrlList' in js['streamUrl'] and js['streamUrl']['nvodHlsUrlList'] is not None:
				vods = js['streamUrl']['nvodHlsUrlList']
				if len(vods) > 0:
					#for i in range(0, len(vods)-1):
					#	info['VOD'][i] = vods['nvod_token']
					info['VOD'] = vods[0]['nvod_token']
			return info
		except Exception as e:
			print(e)
		return

	def GetURLFromSC(self, code, quality):
		url = self.GetURL(code)
		if quality == 'FHD' and url[quality] is None:
			quality = 'HD'
		if quality == 'HD' and url[quality] is None:
			quality = 'SD'
		if url[quality] is None and 'AUTO' in url:
			quality = 'AUTO'
		if url[quality] is None:
			return			
		return url[quality]

	
	# M3U
	def MakeM3U(self, php):
		type = 'OKSUSU'
		str = ''
		list = self.GetChannelList()

		for item in list:
			url = BROAD_URL % (php, type, item['id'])
			tvgid = '%s|%s' % (type, item['id'])
			tvgname = '%s|%s' % (type, item['title'])
			if item['id'] == '85': radio = True
			if item['music_yn'] == 'Y':
				str += M3U_RADIO_FORMAT % (tvgid, tvgname, item['img'], '%s RADIO' % type, item['title'], url)
			else:
				str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], url)
		return str

	# EPG
	
	def MakeEPG(self, filename):
		#list = self.GetChannelList()
		import datetime
		startDate = datetime.datetime.now()
		startParam = startDate.strftime('%Y%m%d')
		endDate = startDate + datetime.timedelta(days=1)
		endParam = endDate.strftime('%Y%m%d')

		str = ''
		url = 'http://www.oksusu.com/api/live/channel?startTime=%s00&endTime=%s24' % (startParam, endParam)
		#url = 'http://www.oksusu.com/api/live/channel?startTime=%s00&endTime=%s06' % (startParam, startParam)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		data = json.load(response, encoding='utf8')

		for channel in data['channels']:
			str += '\t<channel id="OKSUSU|%s">\n' % channel['serviceId']
			str += '\t\t<display-name>OKSUSU|%s</display-name>\n' % channel['channelName']
			str += '\t</channel>\n'
			
			currentDate = startDate
			for epg in channel['programs']:
				startTime = datetime.datetime.fromtimestamp(float(epg['startTime'])/1000.).strftime('%Y%m%d%H%M%S')
				endTime = datetime.datetime.fromtimestamp(float(epg['endTime'])/1000.).strftime('%Y%m%d%H%M%S')

				str += '\t<programme start="%s +0900" stop="%s +0900" channel="OKSUSU|%s">\n' %  (startTime, endTime, channel['serviceId'])
				str += '\t\t<title lang="kr">%s</title>\n' % epg['programName'].replace('<',' ').replace('>',' ')
				
				age_str = '%s세 이상 관람가' % epg['ratingCd'] if epg['ratingCd'] != '0' and epg['ratingCd'] != '1' else '전체 관람가'
				str += '\t\t<rating system="KMRB"><value>%s</value></rating>\n' % age_str
				desc = '등급 : %s\n' % age_str

				if 'mainGenreName' in epg: 
					str += '\t\t<category lang="kr">%s</category>\n' % epg['mainGenreName']
					desc += '장르 : %s\n' % epg['mainGenreName']
				

				actorName = epg['actorName'].strip() if 'actorName' in epg and epg['actorName'] is not None else None
				directorName  = epg['directorName'].strip() if 'directorName' in epg and epg['directorName'] is not None else None
				if actorName is not None or directorName is not None: str += '\t\t<credits>\n'
			
				if actorName is not None:
					temp = actorName.split(',')
					for actor in temp: str += '\t\t\t<actor>%s</actor>\n' % actor.strip().replace('<',' ').replace('>',' ')
					desc += '출연 : %s\n' % actorName
				if directorName is not None:
					temp = directorName.split(',')
					for actor in temp: str += '\t\t\t<producer>%s</producer>\n' % actor.strip().replace('<',' ').replace('>',' ')
					desc += '연출 : %s\n' % directorName
				if actorName is not None or directorName is not None: str += '\t\t</credits>\n'
				
				str += '\t\t<desc lang="kr">%s</desc>\n' % desc.strip().replace('<',' ').replace('>',' ')
				str += '\t</programme>\n'
			
		str += self.MakeEPGRadio(filename)	
		return str
	

	
	def MakeEPGRadio(self, filename):
		list = self.GetChannelList()
		import datetime
		startDate = datetime.datetime.now()
		startParam = startDate.strftime('%Y%m%d')
		endDate = startDate + datetime.timedelta(days=2)
		endParam = endDate.strftime('%Y%m%d')

		str = ''
		for item in list:
			if item['music_yn'] == 'Y':
				str += '\t<channel id="OKSUSU|%s">\n' % item['id']
				str += '\t\t<display-name>OKSUSU|%s</display-name>\n' % item['title']
				str += '\t</channel>\n'
				url = 'http://www.oksusu.com/api/live/schedule?channelServiceId=%s&startTime=%s00&endTime=%s24&scheduleKey=key' % (item['id'], startParam, endParam)
				request = urllib2.Request(url)
				response = urllib2.urlopen(request)
				data = json.load(response, encoding='utf8')
				currentDate = startDate
				for epg in data['channel']['programs']:
					str += '\t<programme start="%s +0900" stop="%s +0900" channel="OKSUSU|%s">\n' %  (epg['startTimeYMDHIS'], epg['endTimeYMDHIS'], item['id'])
					str += '\t\t<title lang="kr">%s</title>\n' % epg['programName'].replace('<',' ').replace('>',' ')
					
					age_str = '%s세 이상 관람가' % epg['ratingCd'] if epg['ratingCd'] != '0' and epg['ratingCd'] != '1' else '전체 관람가'
					str += '\t\t<rating system="KMRB"><value>%s</value></rating>\n' % age_str
					desc = '등급 : %s\n' % age_str

					if 'mainGenreName' in epg: 
						str += '\t\t<category lang="kr">%s</category>\n' % epg['mainGenreName']
						desc += '장르 : %s\n' % epg['mainGenreName']
					

					actorName = epg['actorName'].strip() if 'actorName' in epg and epg['actorName'] is not None else None
					directorName  = epg['directorName'].strip() if 'directorName' in epg and epg['directorName'] is not None else None
					if actorName is not None or directorName is not None: str += '\t\t<credits>\n'
				
					if actorName is not None:
						temp = actorName.split(',')
						for actor in temp: str += '\t\t\t<actor>%s</actor>\n' % actor.strip().replace('<',' ').replace('>',' ')
						desc += '출연 : %s\n' % actorName
					if directorName is not None:
						temp = directorName.split(',')
						for actor in temp: str += '\t\t\t<producer>%s</producer>\n' % actor.strip().replace('<',' ').replace('>',' ')
						desc += '연출 : %s\n' % directorName
					if actorName is not None or directorName is not None: str += '\t\t</credits>\n'
					
					str += '\t\t<desc lang="kr">%s</desc>\n' % desc.strip().replace('<',' ').replace('>',' ')
					str += '\t</programme>\n'
		return str
	