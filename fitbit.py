# pybit
#
# Copyright (c) 2013, Iain R. Learmonth <irl@sdf.org>
# All rights reserved.
#
# For redistribution and use terms, see the LICENSE file.
#

import http.cookiejar
import urllib.request as urllib2
from urllib.parse import urlencode
from xml.dom.minidom import parseString
import re

AUTH_URL = 'https://www.fitbit.com/login'
GRAPH_URL = 'http://www.fitbit.com/graph/getGraphData'

class Fitbit:

    def __init__(self, email, password):
        """
        Perform a login to the Fitbit website in order to get a cookie for later
        use. Email address and password should be nicely escaped before calling
        this function.
        """

        self.cookiej = http.cookiejar.CookieJar()
        cookie_processor = urllib2.HTTPCookieProcessor(self.cookiej)
        self.opener = urllib2.build_opener(cookie_processor)

        payload = {
            'login': 'Log In',
            'includeWorkflow': '',
            'loginRedirect': 'redirect',
            'email': email,
            'password': password
        }
        encoded_data = urlencode(payload)
        request_object = urllib2.Request(AUTH_URL, encoded_data.encode('utf-8'))

        #Request the url with our posted login. We now have session cookies
        response = self.opener.open(request_object)

    def fetchFromFitbit(self, url):
        """
        Perform a GET request for a resource on the Fitbit website using the
        cookie containing the authentication data.
        """

        request = urllib2.Request(url)
        response = self.opener.open(request)

        return response

    def getStepsForDay(self, date):
        """
        Given a date, returns an array of data points of steps data with 5
        minute resolution.
        """

        urlParts = [
            GRAPH_URL,
            "?type=intradaySteps",
            "&version=amchart",
            "&dateFrom=%s" % (date.strftime('%Y-%m-%d'),),
            "&dateTo=%s" % (date.strftime('%Y-%m-%d'),),
            "&chart_type=column2d",
        ]

        url = ''.join(urlParts)

        xml = self.fetchFromFitbit(url).read().strip() # The strip() is
                                                       # NECESSARY!!
        return self.__stepsXMLToPython(xml)

    def __stepsXMLToPython(self, xml):
        """
        This code is horrific just because the input XML is horrific. If
        Fitbit change their website, this will be the first thing to break.
        """

        stepsData = []

        dom = parseString(xml.strip())
        dataPoints = dom.getElementsByTagName('data')[0] \
            .getElementsByTagName('graph')[0]            \
            .getElementsByTagName('value')
        for point in dataPoints:
            if point.attributes['xid'].value != '288':
                times = re.findall(r'[1-2]?[0-9]:[0-9][0-9]',
                    point.attributes['description'].value)
                stepsData.append({
                    'start': times[0],
                    'end': times[1],
                    'steps': self.__getTextFromNode(point.childNodes)
                    })

        return stepsData

    def getSleepForDay(self, date):
        """
        Currently returns XML, need to find a way of matching values to times.
        """

        urlParts = [
            GRAPH_URL,
            "?type=intradaySleep",
            "&period=1m",
            "&dateTo=%s" (date.strftime('%Y-%m-%d'),),
        ]

        url = ''.join(urlParts)

        xml = self.fetchFromFitbit(url)

        return xml

    def __getTextFromNode(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

