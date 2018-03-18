from logic import *
NAME = 'KLive'
PREFIX = '/video/klive'
ICON = 'icon-default.jpg'
ART = 'art-default.jpg'

####################################################################################################
def Start():
    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)
    HTTP.CacheTime = 0

####################################################################################################
@handler(PREFIX, NAME, thumb = ICON, art = ART)
def MainMenu():
	oc = ObjectContainer()
	try:
		for menu in TOP_MENU_LIST:
			tmp = menu.split('|')
			oc.add(
			    DirectoryObject(
				key = 
				    Callback(
					ChannelList,
					title = unicode(tmp[1]),
					type = tmp[0]
				    ),
				title = unicode(tmp[1]),
				#thumb = R("%s.png" % tmp[1])
			    )
			)
	except Exception as e:
		LOG('<<<Exception>>> MainMenu: %s' % e)
	return oc

####################################################################################################
@route(PREFIX + '/ChannelList')
def ChannelList(title, type):
	oc = ObjectContainer(title2 = unicode(title))
	try:
		list = GetChannelList(type)
		for item in list:
			param = item['id']
			isUrl = 'N'
			if 'url' in item:
				param = item['url']
				isUrl = 'Y'
			
			isTv = 'Y'
			if 'isTv' in item: isTv = item['isTv']
			if 'isRadio' in item and item['isRadio'] == 'Y': isTv = 'N'
			if Client.Product == 'Plex for iOS': isTv = 'Y'

			if isTv == 'Y':
				oc.add(
					CreateVideoClipObject(
						url = param, title = unicode(item['title']), thumb = item['img'], art = ART,
						summary = unicode(item['summary']), type=type, id = item['id'], isUrl=isUrl,
						include_container = False
					)
				)
			else:
				oc.add(
					CreateTrackObject(
						url = param, title = unicode(item['title']), thumb = item['img'], art = ART,
						summary = unicode(item['summary']), type=type, id = item['id'], isUrl=isUrl,
						include_container = False
					)
				)
	except Exception as e:
		LOG('<<<Exception>>> ChannelList: %s' % e)
	return oc

####################################################################################################
@route(PREFIX + '/CreateVideoClipObject', include_container = bool)
def CreateVideoClipObject(url, title, thumb, art, summary, type, id,  isUrl,
                          optimized_for_streaming = True,
                          include_container = False, *args, **kwargs):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject,
		url = url, title = title, thumb = thumb, art = art, summary = summary,
		type=type, id = id, isUrl = isUrl,
		optimized_for_streaming = optimized_for_streaming,
		include_container = True),
        rating_key = url,
        title = title,
        thumb = thumb,
        art = art,
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(Callback(PlayVideo, url = url, type=type, id = id, isUrl=isUrl))
                    )
                ],
                optimized_for_streaming = optimized_for_streaming,
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects = [vco])
    else:
        return vco

####################################################################################################
@route(PREFIX + '/createtrackobject', include_container = bool)
def CreateTrackObject(url, title, thumb, art, summary, type, id,  isUrl, include_container=False, *args, **kwargs):
	container = Container.MP4
	audio_codec = AudioCodec.AAC
	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, title=title, thumb=thumb, art=art, summary=summary, type=type, id=id,   isUrl = isUrl, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		items = [
			MediaObject(
				parts = [
					PartObject(
						#key=url
						key = Callback(PlayAudio, url=url, type=type, id=id, isUrl=isUrl,)
					)
				],
				container = container,
				audio_codec = audio_codec,
				audio_channels = 2
			)
		], 
		thumb = Resource.ContentsOfURLWithFallback(thumb)
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object

####################################################################################################
@indirect
@route(PREFIX + '/PlayVideo.m3u8')
def PlayVideo(url, type, id,  isUrl):
	if isUrl == 'N': url = GetURL(type, id)
	LOG('PLAYVIDEO %s' % url)
	return IndirectResponse(VideoClipObject, key = url)

####################################################################################################
@indirect
@route(PREFIX + '/PlayAudio.m3u8')
def PlayAudio(url, type, id,  isUrl):
	if isUrl == 'N': url = GetURL(type, id)
	LOG('PlayAudio %s' % url)
	return IndirectResponse(TrackObject, key=url)

####################################################################################################
@route(PREFIX + '/label')
def Label(message):
	oc = ObjectContainer(title2 = unicode(message))
	oc.add(DirectoryObject(key = Callback(Label, message=message),title = unicode(message)))
	return oc
