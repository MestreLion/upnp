import urllib2

ctrl_url = "http://10.10.10.1:1990/107fc877-460c-4b0d-91c2-48ff4e333181/control?WFAWLANConfig"

soap_encoding = "http://schemas.xmlsoap.org/soap/encoding/"
soap_env = "http://schemas.xmlsoap.org/soap/envelope"
service_ns = "urn:schemas-wifialliance-org:service:WFAWLANConfig:1"
soap_body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body>
<u:GetDeviceInfo xmlns:u="urn:schemas-upnp-org:control-1-0">
</u:GetDeviceInfo>
</s:Body>
</s:Envelope>
"""

soap_action = "urn:schemas-wifialliance-org:service:WFAWLANConfig#GetDeviceInfo"
headers = {
    'SOAPAction': u'"%s"' % (soap_action),
    'Host': u'192.168.0.1:1990',
    'Content-Type': 'text/xml',
    'Content-Length': len(soap_body),
}

request = urllib2.Request(ctrl_url, soap_body, headers)
response = urllib2.urlopen(request)

print response.read()
