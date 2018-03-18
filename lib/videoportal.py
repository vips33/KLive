# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import os
import json
import pickle
import time
import xml.etree.ElementTree as ET
from util import *

class VIDEOPORTAL:
	COOKIE_FILENAME = 'videoportal.txt'

	# Login

	# List
	def GetChannelList(self):
		try:
			import datetime
			stamp = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
			url = 'http://123.140.104.150/api/epg/v1/channel/virtual?access_key=C4A0697007C3548D389B&cp_id=S_LGU_HYUK0920&system_id=HDTV&SA_ID=500053434041&STB_MAC=v000.5343.4041&NSC_TYPE=LTE&BASE_GB=Y&BASE_CD=W172.017&YOUTH_YN=N&ORDER_GB=N&POOQ_YN=N&HDTV_VIEW_GB=R&SID=001010005638&CLIENT_IP=172.17.100.15&OS_INFO=android_4.4.2&NW_INFO=WIFI&APP_TYPE=ROSA&DEV_MODEL=SM-N935F&CARRIER_TYPE=E&UI_VER=04.38.04&NOW_PAGE=25&PRE_PAGE=&MENU_NM=&CONTS_GB=&TERM_BINVER=3.8.118.0106'
			result = []
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			tree = ET.parse(response)
			root = tree.getroot()
			for item in root.findall('list'):
				info = {}
				info['id'] = item.findtext('service_id')
				info['title'] = item.findtext('service_name')
				info['img'] = item.findtext('img_url') + item.findtext('img_file_name')
				info['summary'] = item.findtext('description')
				url = item.findtext('live_server1') + item.findtext('live_file_name1')
				info['url']  = '%s?VOD_RequestID=v2M2-0101-1010-7272-5050-0000%s;LTE;480p;WIFI&APPNAME=hdtv&ALBUM_ID=%s&ma=D0:17:C2:CE:D7:A1' % (url, stamp, info['id'])
				if item.findtext('live_file_name1') != '' and item.findtext('genre_name') != u'성인':
					result.append(info)
		except Exception as e:
			print(e)
			result = []
		return result

	# URL
	def GetURL(self, code):
		import datetime
		try:
			live_server1 = 'http://1.214.67.74:80/'
			live_file_name = '%sHN.m3u8' % code
			stamp = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
			url = '%s%s?VOD_RequestID=v2M2-0101-1010-7272-5050-0000%s;LTE;720p;WIFI&APPNAME=hdtv&ALBUM_ID=%s&ma=D0:17:C2:CE:D7:A1' % (live_server1, live_file_name, stamp, code)
			return url
		except Exception as e:
			print(e)
		return
	
	# M3U
	def MakeM3U(self, php):
		type = 'VIDEOPORTAL'
		str = ''
		list = self.GetChannelList()

		for item in list:
			url = BROAD_URL % (php, type, item['id'])
			tvgid = '%s|%s' % (type, item['id'])
			tvgname = '%s|%s' % (type, item['title'])
			str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], url)
			#str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], item['url'])
		return str

	# EPG
	#
	def MakeEPG(self, filename):
		str = ''
		list = self.GetChannelList()
		for item in list:
			str += '\t<channel id="VIDEOPORTAL|%s">\n' % item['id']
			str += '\t\t<display-name>VIDEOPORTAL|%s</display-name>\n' % item['title']
			str += '\t</channel>\n'


		url = 'http://123.140.104.150/api/epg/v1/schedule/virtual?access_key=CE45020A8BC704127A6C&cp_id=S_LGU_HYUK0920&system_id=HDTV&SA_ID=M20110725000&STB_MAC=v201.1072.5000&NSC_TYPE=LTE&TC_IN=-1&TC_OUT=3&YOUTH_YN=N&POOQ_YN=N&HDTV_VIEW_GB=R&SERVICE_ID=&EPG_SDATE=&EPG_EDATE=&SID=001010005638&CLIENT_IP=192.168.0.1&OS_INFO=android_4.4.2&NW_INFO=WIFI&APP_TYPE=ROSA&DEV_MODEL=SM-N935F&CARRIER_TYPE=E&UI_VER=04.38.04&NOW_PAGE=25&PRE_PAGE=&MENU_NM=&CONTS_GB=&TERM_BINVER=3.8.118.0106'
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		tree = ET.parse(response)
		root = tree.getroot()
		for item in root.findall('list'):
			str += '\t<programme start="%s +0900" stop="%s +0900" channel="VIDEOPORTAL|%s">\n' %  (item.findtext('start_time'), item.findtext('end_time'), item.findtext('service_id'))
			str += '\t\t<title lang="kr">%s</title>\n' % item.findtext('program_title').replace('<',' ').replace('>',' ')

			#age_str = '%s세 이상 관람가' % epg['ratingCd'] if epg['ratingCd'] != '0' and epg['ratingCd'] != '1' else '전체 관람가'
			#str += '\t\t<rating system="KMRB"><value>%s</value></rating>\n' % age_str
			#desc = '등급 : %s\n' % age_str
			desc = ''

			actorName = item.findtext('act').strip()				
			actorName = actorName if actorName != '' else None
			if actorName is not None: 
				str += '\t\t<credits>\n'
				temp = actorName.split(',')
				for actor in temp: str += '\t\t\t<actor>%s</actor>\n' % actor.strip().replace('<',' ').replace('>',' ')
				desc += '출연 : %s\n' % actorName
				str += '\t\t</credits>\n'
			if item.findtext('sid').strip() != '': desc += '%s\n' % item.findtext('sid').strip()
			desc += '%s' % item.findtext('program_synopsis')
			str += '\t\t<desc lang="kr">%s</desc>\n' % desc.strip().replace('<',' ').replace('>',' ')
			str += '\t</programme>\n'
		return str
	

	
	

"""
#ret = VIDEOPORTAL().GetChannelList()
ret = VIDEOPORTAL().MakeM3U('')
print(ret)


&f9ETX@"C5P#PGET /747HN.m3u8?VOD_RequestID=v050-0000-5353-4343-4040-414120180308120056;LTE;480p;WIFI&APPNAME=hdtv&ALBUM_ID=747&ma=D0:17:C2:CE:D7:A1 HTTP/1.1
Host: 1.214.67.12
User-Agent: Android 1.0 


http://1.214.67.74/747HN.m3u8?VOD_RequestID=v2M2-0101-1010-7272-5050-000020180308115412;LTE;720p;WIFI&APPNAME=hdtv&ALBUM_ID=747&ma=D0:17:C2:CE:D7:A1
http://1.214.67.74/747HN.m3u8?VOD_RequestID=v2M2-0101-1010-7272-5050-000020180308115412;LTE;1080p;WIFI&APPNAME=hdtv&ALBUM_ID=747&ma=D0:17:C2:CE:D7:A1

http://123.140.104.150/api/epg/v1/channel/virtual?access_key=C4A0697007C3548D389B&cp_id=S_LGU_HYUK0920&system_id=HDTV&SA_ID=500053434041&STB_MAC=v000.5343.4041&NSC_TYPE=LTE&BASE_GB=Y&BASE_CD=W172.017&YOUTH_YN=N&ORDER_GB=N&POOQ_YN=N&HDTV_VIEW_GB=R&SID=001010005638&CLIENT_IP=172.17.100.15&OS_INFO=android_4.4.2&NW_INFO=WIFI&APP_TYPE=ROSA&DEV_MODEL=SM-N935F&CARRIER_TYPE=E&UI_VER=04.38.04&NOW_PAGE=25&PRE_PAGE=&MENU_NM=&CONTS_GB=&TERM_BINVER=3.8.118.0106

&f9ETX@"C5P#PGET http://1.209.146.140:80/747H.m3u8?VOD_RequestID=v050-0000-5353-4343-4040-414120180308120056;LTE;480p;WIFI&APPNAME=hdtv&ALBUM_ID=747&ma=D0:17:C2:CE:D7:A1 HTTP/1.1
Host: 1.214.67.12
User-Agent: Android 1.0 




<service_id>747</service_id>
<service_name>JTBC</service_name>
<service_eng_name>JTBC</service_eng_name>
<live_server1>http://1.214.67.74:80/</live_server1>
<live_file_name1>747HN.m3u8</live_file_name1>
<live_server2>http://1.209.146.140:80/</live_server2>
<live_file_name2>747H.m3u8</live_file_name2>
<live_server3>http://1.209.146.20:80/</live_server3>
<live_file_name3>747H.m3u8</live_file_name3>
<live_low_server1>http://1.214.67.74:80/</live_low_server1>
<live_low_file_name1>747LN.m3u8</live_low_file_name1>
<live_low_server2>http://1.209.146.140:80/</live_low_server2>
<live_low_file_name2>747L.m3u8</live_low_file_name2>
<live_low_server3>http://1.209.146.20:80/</live_low_server3>
<live_low_file_name3>747L.m3u8</live_low_file_name3>
<img_url>http://210.182.60.11/image/</img_url>
<img_file_name>JTBC_H161012.png</img_file_name>

http://1.214.67.74:80/vod/747HN.m3u8

&f9ETX@"C5P#PGET 
http://1.214.67.74:80/747HN.m3u8?VOD_RequestID=v050-0000-5353-4343-4040-414120180308120056;LTE;480p;WIFI&APPNAME=hdtv&ALBUM_ID=747&ma=D0:17:C2:CE:D7:A1 HTTP/1.1
Host: 1.214.67.12
User-Agent: Android 1.0 




&f9E@?{h8P;@jPGET /api/epg/v1/channel/virtual?access_key=C4A0697007C3548D389B&cp_id=S_LGU_HYUK0920&system_id=HDTV&SA_ID=M20110725000&STB_MAC=v201.1072.5000&NSC_TYPE=LTE&BASE_GB=Y&BASE_CD=W172.017&YOUTH_YN=N&ORDER_GB=N&POOQ_YN=N&HDTV_VIEW_GB=R&SID=001010005638&CLIENT_IP=172.17.100.15&OS_INFO=android_4.4.2&NW_INFO=WIFI&APP_TYPE=ROSA&DEV_MODEL=SM-N935F&CARRIER_TYPE=E&UI_VER=04.38.04&NOW_PAGE=25&PRE_PAGE=&MENU_NM=&CONTS_GB=&TERM_BINVER=3.8.118.0106 HTTP/1.1
Accept: application/xml
Content-Type: application/xml
Host: 123.140.104.150
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.8.0
&f9E@?{h8P5f!P1GET 123.140.104.150/api/epg/v1/schedule/virtual?access_key=CE45020A8BC704127A6C&cp_id=S_LGU_HYUK0920&system_id=HDTV&SA_ID=M20110725000&STB_MAC=v201.1072.5000&NSC_TYPE=LTE&TC_IN=-1&TC_OUT=3&YOUTH_YN=N&POOQ_YN=N&HDTV_VIEW_GB=R&SERVICE_ID=&EPG_SDATE=&EPG_EDATE=&SID=001010005638&CLIENT_IP=172.17.100.15&OS_INFO=android_4.4.2&NW_INFO=WIFI&APP_TYPE=ROSA&DEV_MODEL=SM-N935F&CARRIER_TYPE=E&UI_VER=04.38.04&NOW_PAGE=25&PRE_PAGE=&MENU_NM=&CONTS_GB=&TERM_BINVER=3.8.118.0106 HTTP/1.1
Accept: application/xml
Content-Type: application/xml
Host: 123.140.104.150
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.8.0


http://1.214.67.74/747HN.m3u8?VOD_RequestID=v2M2-0101-1010-7272-5050-000020180308135532;LTE;480p;WIFI&APPNAME=hdtv&ALBUM_ID=747&ma=D0:17:C2:CE:D7:A1

http://1.214.67.12/750HN.m3u8?VOD_RequestID=v2M2-0101-1010-7272-5050-000020180308135532;LTE;480p;WIFI&APPNAME=hdtv&ALBUM_ID=750&ma=D0:17:C2:CE:D7:A1

http://1.214.67.12/750HN.m3u8?VOD_RequestID=v2M2-0101-1010-7272-5050-000020180308135532

;LTE;720p;WIFI&APPNAME=hdtv&ALBUM_ID=750&ma=D0:17:C2:CE:D7:A1





"""