# -*- coding: utf-8 -*-
"""
사용법
 - m3u 생성 
      python klive.py m3u [klive.php 주소]
  예) python klive.py m3u http://xxx.synology.me/klive/klive.php

 - epg 파일 생성
      python klive.py epg
""" 

# M3U 
# 지원목록 : KBS MBC SBS RADIO1 POOQ TVING OKSUSU OLLEH VIDEOPORTAL EVERYON TVING_VOD RADIO2
# '|' 로 구분
CONTENTS_LIST		= 'KBS|MBC|SBS|RADIO1|POOQ|TVING|OKSUSU|OLLEH|VIDEOPORTAL|EVERYON|TVING_VOD|RADIO2'


# M3U 파일 이름
FILENAME_M3U		= 'klive.m3u'


# EPG 저장될 파일
FILENAME_EPG 		= 'klive.xml'


# MBC
MBC_ID			= ''
MBC_PW			= ''


# 푹
POOQ_ID			= ''
POOQ_PW			= ''
POOQ_QUALITY		= '1000'		# 5000 2000 1000 500


# 티빙
TVING_ID		= ''
TVING_PW		= ''
TVING_QUALITY		= 'stream30'		# stream50 stream40 stream30
TVING_LOGIN_TYPE	= 'CJONE'		# CJONE TVING


# 옥수수
OKSUSU_ID		= ''
OKSUSU_PW		= ''
OKSUSU_QUALITY		= 'SD'			# FHD HD SD


# 올레 모바일 TV
OLLEH_ID		= ''
OLLEH_PW		= ''
OLLEH_QUALITY		= '1000'		# 4000 2000 1000


# RADIO2 xml 파일 경로
RADIO2_XML		= 'https://soju6jan.github.io/radio2'
