# Plugin constants
__plugin__ = 'Roskilde Festival videos'
__author__ = 'Jeppe Toustrup'
__url__ = 'https://github.com/Tenzer/plugin.video.roskilde'
__version__ = '0.0.0'
__sourceurl__ = 'http://vms.api.qbrick.com/rest/v3/getplayer/34DC795A397AC7F3'


import sys
import time
import urllib
import urllib2
import urlparse
import xml.dom.minidom

import xbmc
import xbmcgui
import xbmcplugin

plugin = sys.argv[0]
handle = int(sys.argv[1])
params = urlparse.parse_qs(sys.argv[2][1:])  # Skip '?'

if params:
    # Get stream URL
    req = urllib2.Request(params['streamurl'][0])
    res = urllib2.urlopen(req)
    rawRes = res.read()
    res.close()

    # Parse XML file
    xml = xml.dom.minidom.parseString(rawRes)
    base = xml.getElementsByTagName('meta')[0].getAttribute('base')
    stream = xml.getElementsByTagName('video')[-1].getAttribute('src')

    xbmc.log('Found base: %s, and stream: %s' % (base, stream), xbmc.LOGNOTICE)

    listitem = xbmcgui.ListItem(params['title'][0])
    listitem.setProperty('PlayPath', stream)
    xbmc.Player().play(base, listitem)
else:
    # Get XML file
    req = urllib2.Request(__sourceurl__)
    res = urllib2.urlopen(req)
    rawRes = res.read()
    res.close()

    # Parse XML file
    xml = xml.dom.minidom.parseString(rawRes)
    items = xml.getElementsByTagName('item')

    # Set metadata
    xbmcplugin.setContent(handle, 'musicvideos')
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_DATE)

    # Print list of videos
    total = len(items)
    for item in items:
        title = item.getElementsByTagName('title')[0].firstChild.data
        thumbnail = item.getElementsByTagName('image')[0].firstChild.data
        streamurl = item.getElementsByTagName('substream')[0].firstChild.data

        date_obj = time.strptime(item.getElementsByTagName('publishdate')[0].firstChild.data, '%Y-%m-%d %H:%M:%S')
        date = time.strftime('%d.%m.%Y', date_obj)

        params = urllib.urlencode({
            #'id': id,
            'title': title.encode('utf-8'),
            'thumbnail': thumbnail,
            'streamurl': streamurl,
            'date': date
        })
        url = plugin + '?' + params

        listitem = xbmcgui.ListItem()
        listitem.setLabel(title)
        listitem.setLabel2(date)
        listitem.setThumbnailImage(thumbnail)
        listitem.setInfo('video', {'date': date, 'title': title})
        xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=total)

    xbmcplugin.endOfDirectory(handle)
