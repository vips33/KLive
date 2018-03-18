# -*- coding: utf-8 -*-
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.join( os.getcwd(), 'lib' ))

from setting import *
from pooq import *
from tving import *
from oksusu import *
from everyon import *
from sbs import *
from kbs import *
from mbc import *
from util import *
from radio import *
from olleh import *
from videoportal import *

def MakeM3U(php):
	temp = CONTENTS_LIST.split('|')
	str = '#EXTM3U\n'
	for item in temp:
		if item == 'KBS': str += KBS().MakeM3U(php)
		if item == 'MBC': str += MBC().MakeM3U(php)
		if item == 'SBS': str += SBS().MakeM3U(php)
		if item == 'RADIO1': str += RADIO1().MakeM3U(php)
		if item == 'RADIO2': str += RADIO2(RADIO2_XML).MakeM3U(php)
		if item == 'POOQ': str += POOQ().MakeM3U(php)
		if item == 'TVING': str += TVING().MakeM3U(php)
		if item == 'OKSUSU': str += OKSUSU().MakeM3U(php)
		if item == 'EVERYON': str += EVERYON().MakeM3U(php)
		if item == 'OLLEH': str += OLLEH().MakeM3U(php)
		if item == 'TVING_VOD': str += TVING().MakeM3U(php, list_type=1)
		if item == 'VIDEOPORTAL': str += VIDEOPORTAL().MakeM3U(php)
	str = ChangeM3UForEPG(str)
	if FILENAME_M3U != '':
		WriteFile(FILENAME_M3U, str)
	return str

def ChangeM3UForEPG(str):
	list = [
		['\"KBS|KBS 1TV\"',		'\"POOQ|KBS 1TV\"'],
		['\"KBS|KBS 2TV\"',		'\"POOQ|KBS 2TV\"'],
		['\"KBS|KBSN Drama\"',		'\"POOQ|KBS DRAMA\"'],
		['\"KBS|KBSN Joy\"',		'\"POOQ|KBS JOY\"'],
		['\"KBS|KBSN W\"',		'\"POOQ|KBS W\"'],
		['\"KBS|KBSN Life\"',		'\"POOQ|KBSN Life\"'],
		['\"KBS|KBS 1Radio\"',		'\"POOQ|KBS1RADIO\"'],
		['\"KBS|KBS 2FM Cool FM\"',	'\"POOQ|KBSCOOLFM\"'],
		['\"KBS|KBS 2FM Cool FM 보라\"',	'\"POOQ|KBSCOOLFM\"'],
		['\"MBC|MBC\"',			'\"POOQ|MBC\"'],
		['\"MBC|MBC 표준FM\"',		'\"POOQ|MBC 표준 FM\"'],
		['\"MBC|MBC FM4U\"',		'\"POOQ|MBC FM4U\"'],
		['\"MBC|MBC 무한도전24\"',	'\"POOQ|MBC 무한도전\"'],
		['\"POOQ|CCTV4\"',		'\"EVERYON|CH.28 CCTV-4\"'],
		['\"POOQ|ANIMAX\"',		'\"OKSUSU|Animax\"'],
		]
	for item in list:
		str = str.replace(item[0], item[1])
	return str


def MakeEPG():
	temp = CONTENTS_LIST.split('|')
	str = ''
	str += '<?xml version="1.0" encoding="UTF-8"?>\n'
	str += '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
	str += '<tv generator-info-name="sc">\n'
	file = None
	for item in temp:
		#if item == 'KBS': str += MakeEPG_KBS(file)
		#if item == 'MBC': str += MakeEPG_MBC(file)
		#if item == 'SBS': str += MakeEPG_SBS(file)
		if item == 'POOQ': str += POOQ().MakeEPG(file)
		if item == 'TVING': str += TVING().MakeEPG(file)
		if item == 'OKSUSU': str += OKSUSU().MakeEPG(file)
		if item == 'EVERYON': str += EVERYON().MakeEPG(file)
		if item == 'OLLEH': str += OLLEH().MakeEPG(file)
		if item == 'TVING_VOD': str += TVING().MakeEPG(file, list_type=1)
		if item == 'VIDEOPORTAL': str += VIDEOPORTAL().MakeEPG(file)
	str += '</tv>\n'
	str = str.replace('&amp;', '·')
	str = str.replace('&', '·')
	if FILENAME_EPG != '':
		WriteFile(FILENAME_EPG, str)
	return str


def GetURL(type, id):
	if type == 'SBS': 
		SBS().DoLoginFromSC(SBS_ID, SBS_PW)
		ret = SBS().GetURL(id)
	elif type == 'EVERYON': 
		ret = EVERYON().GetURLFromSC(id)
	elif type == 'POOQ': 
		POOQ().DoLoginFromSC(POOQ_ID, POOQ_PW)
		ret = POOQ().GetURL(id, POOQ_QUALITY)
	elif type == 'TVING':
		TVING().DoLoginFromSC(TVING_ID, TVING_PW, TVING_LOGIN_TYPE)
		ret = TVING().GetURL(id, TVING_QUALITY)
	elif type == 'OKSUSU':
		OKSUSU().DoLoginFromSC(OKSUSU_ID, OKSUSU_PW)
		ret = OKSUSU().GetURLFromSC(id, OKSUSU_QUALITY)
	elif type == 'OLLEH':
		OLLEH().DoLoginFromSC(OLLEH_ID, OLLEH_PW)
		ret = OLLEH().GetURLFromSC(id, OLLEH_QUALITY)
	elif type == 'KBS':
		ret = KBS().GetURLWithLocalID(id)
	elif type == 'MBC':
		MBC().DoLoginFromSC(MBC_ID, MBC_PW)
		ret = MBC().GetURLWithLocalID(id)
	elif type == 'VIDEOPORTAL':
		ret = VIDEOPORTAL().GetURL(id)
	return ret

def main():
	mode = 'm3u'
	argLen = len(sys.argv)
	if len(sys.argv) > 1:
		mode = sys.argv[1]
	if mode == 'm3u':
		php = sys.argv[2] if argLen > 2 else 'http://localhost/klive/klive.php'
		ret = MakeM3U(php)
	elif mode == 'url':
		type = sys.argv[2]
		id = sys.argv[3]
		ret = GetURL(type, id)
	elif mode == 'epg':
		ret = MakeEPG()
	if ret is not None:
		print(ret)

main()