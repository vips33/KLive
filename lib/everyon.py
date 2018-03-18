# -*- coding: utf-8 -*-
import urllib, urllib2
import json
import re
from util import *

class EVERYON:
	EVERYON_LIST = ['전체채널|all', '종편/뉴스|20100', '경제/정보/해외|20300', '레저/스포츠/게임|20400', '드라마/보험|20500', '연예/오락|20600', '여성/어린이/교육|20700', '종교/지역/공공|20800','홈쇼핑|20200']

	# List
	def  GetChannelList(self):
		ret = []
		for cate in self.EVERYON_LIST:
			temp = cate.split('|')
			if temp[1] != 'all':
				pageNo = 1
				while True:
					hasMore, list = self.GetChannelListFromCate(temp[1], pageNo)
					for item in list:
						ret.append(item)
					if hasMore == 'N': break
					pageNo += 1
		return ret



	def GetChannelListFromCate(self, cate, pageNo='1'):
		url  = 'http://www.everyon.tv/main/proc/ajax_ch_list.php'
		params = { 'chNum' : '', 'cate':'', 'sCate':cate, 'chNum':'', 'chNm':'', 'page':pageNo, 'perPage':'20', 'srchTxt':''  }
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		request.add_header('Cookie', 'etv_api_key=88abc0e1c8e61c8c3109788ec8392c7fd86c16765fc0b80d5f2366c84c894203')
		response = urllib2.urlopen(request)
		data = response.read()
		#print(data)
		hasMore = 'Y' if int(data.split('|')[1]) > int(pageNo) * 20 else 'N'
		regax = 'thumb\"\stitle\=\"(.*?)\".*\s*.*selCh\(\'(.*?)\'.*\s*<img\ssrc\=\"(.*?)\"'
		regax2 = 'ch_name\"\stitle\=\"(.*?)\"'
		r = re.compile(regax)
		r2 = re.compile(regax2)
		m = r.findall(data)
		m2 = r2.findall(data)
		list = []
		#for item in m:
		for i in range(len(m)-1):
			info = {}
			info['title'] = m[i][0].replace(',', ' ')
			info['id'] = m[i][1]
			info['img'] = m[i][2]
			info['summary'] = m2[i]
			list.append(info)
		return hasMore, list

	
	# URL
	def GetURLFromSC(self, id):
		url  = 'http://www.everyon.tv/main/proc/get_ch_data.php'
		params = { 'chId' : id }
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		request.add_header('Cookie', 'etv_api_key=88abc0e1c8e61c8c3109788ec8392c7fd86c16765fc0b80d5f2366c84c894203')
		response = urllib2.urlopen(request)
		data = json.load(response, encoding='utf8')
		url2 = data['medias'][0]['url'] if len(data['medias']) > 0 else None	
		return url2
		

	# M3U	
	def MakeM3U(self, php):
		type = 'EVERYON'
		str = ''
		for item in self. GetChannelList():
			url = BROAD_URL % (php, type, item['id'])
			tvgid = '%s|%s' % (type, item['id'])
			tvgname = '%s|%s' % (type, item['title'])
			str += M3U_FORMAT % (tvgid, tvgname, item['img'], type, item['title'], url)
		return str

	def MakeEPG(self, filename):
		list = self. GetChannelList()
		import datetime
		startDate = datetime.datetime.now()
		startParam = startDate.strftime('%Y%m%d')
		endDate = startDate + datetime.timedelta(days=1)
		endParam = endDate.strftime('%Y%m%d')

		str = ''
		regax = '\<td\>(.*?)\<'
		p = re.compile(regax)

		for item in list:
			str += '\t<channel id="EVERYON|%s">\n' % item['id']
			str += '\t\t<display-name>EVERYON|%s</display-name>\n' % item['title']
			str += '\t</channel>\n'
			
			url_today = 'http://www.everyon.tv/main/schedule.etv?chNum=%s' % item['id']
			url_next = 'http://www.everyon.tv/main/schedule.etv?chNum=%s&schDt=%s&schFlag=n' % (item['id'], startParam)

			for url in [url_today, url_next]:
				current_date = startDate if url == url_today else endDate

				request = urllib2.Request(url)
				response = urllib2.urlopen(request)
				data = response.read()

				idx1 = data.find('<tbody>')
				idx2 = data.find('</tbody>')
				data = data[idx1+7:idx2]
				
				m = p.findall(data)
				for i in range(len(m)/3):
					time = m[i*3].replace(':', '')
					title = m[i*3+1]
					age = m[i*3+2]
					
					if time == '': continue

					temp = time.split('~')
					start_time = temp[0]
					end_time = temp[1]
					start_str = '%s%s' % (current_date.strftime('%Y%m%d'),start_time)
					if int(start_time) > int(end_time): current_date = current_date + datetime.timedelta(days=1)
					end_str = '%s%s' % (current_date.strftime('%Y%m%d'),end_time)

					str += '\t<programme start="%s00 +0900" stop="%s00 +0900" channel="EVERYON|%s">\n' %  (start_str, end_str, item['id'])
					str += '\t\t<title lang="kr">%s</title>\n' % title.replace('<',' ').replace('>',' ')
					
					age_str = '%s세 이상 관람가' % age if age != 'ALL' else '전체 관람가'
					str += '\t\t<rating system="KMRB"><value>%s</value></rating>\n' % age_str
					desc = '등급 : %s\n' % age_str

					str += '\t\t<desc lang="kr">%s</desc>\n' % desc.strip().replace('<',' ').replace('>',' ')
					str += '\t</programme>\n'
		return str
