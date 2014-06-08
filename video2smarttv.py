#!/usr/bin/python
# coding: utf-8

#
# Send mp4 streaming media URIs to Samsung Smart TV for immediate playback
#

import os, socket, argparse, logging, subprocess, cgi

#
# Defaults
#

port = 7676

#
# DIDL-Lite template
# Note that this is included in the Universal Plug and Play (UPnP) message in urlencoded form
#

didl_lite_template = """<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:sec="http://www.sec.co.kr/">
   <item id="f-0" parentID="0" restricted="0">
      <upnp:class>object.item.videoItem</upnp:class>
      <res protocolInfo="http-get:*:video/mp4:DLNA.ORG_OP=01;DLNA.ORG_CI=0;DLNA.ORG_FLAGS=01700000000000000000000000000000" sec:URIType="public">$$$URI$$$</res>
   </item>
</DIDL-Lite>"""

# Remove newlines and whitespace
didl_lite = ' '.join(cgi.escape(didl_lite_template.replace("\n","")).split())

#
# Universal Plug and Play (UPnP) message templates.
# Note that the request times out if there is a blank charater between the header lines and the message
# or if we do not use .replace("\n", "\r\n") to get "CRLF line terminators"
#

AVTransportTemplate = """POST /smp_22_ HTTP/1.1
Accept: application/json, text/plain, */*
Soapaction: "urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"
Content-Type: text/xml;charset="UTF-8"

<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
      <CurrentURI>$$$URI$$$</CurrentURI>
      <CurrentURIMetaData>$DIDL</CurrentURIMetaData>
    </u:SetAVTransportURI>
  </s:Body>
</s:Envelope>"""

PlayTemplate = """POST /smp_22_ HTTP/1.1
Accept: application/json, text/plain, */*
Soapaction: "urn:schemas-upnp-org:service:AVTransport:1#Play"
Content-Type: text/xml;charset="UTF-8"

<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
      <Speed>1</Speed>
    </u:Play>
  </s:Body>
</s:Envelope>"""

#
# Send message to the TV
#

def sendMessage(ip, port, message):
  s    = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  s.connect((ip, port))
  sent = s.send(message.replace("\n", "\r\n"))
  if (sent <= 0):
    print("Error sending message")
    s.close()
    return
  recv = s.recv(100000)
  s.close()
  logging.debug(recv)
  logging.debug("")

#
# Parse command line and send messages to the TV
#

def main():
  parser = argparse.ArgumentParser(description='Send mp4 video streams to a Samsung Smart TV', add_help = True)
  flags = parser.add_argument_group('Arguments')
  parser.add_argument("-v", "--verbose", help="Verbose output, print requests and responses", action="store_true")
  flags.add_argument('-i', '--ip', dest = 'ip', default = None, help = 'Required. IP Address of the TV', required = True)
  flags.add_argument('-p', '--port', dest = 'port', default = port, type = int, help = 'Optional. Port of the TV')
  flags.add_argument('uri', default = None, help = 'Required. URI to be sent to TV. If this does not start with http, it is sent to yt-downloader for processing.')

  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

  if not (args.uri.startswith("http")):
    myexec = "youtube-dl"
    try:
      FNULL = open(os.devnull, 'w')
      subprocess.call([myexec, '--version'], stdout=FNULL, stderr=FNULL)
    except OSError:
      print "%s is not installed." % myexec
      print "Install it in order to be able to search YouTube."
      exit(1)
    command = ["youtube-dl", "-g", "--default-search", "auto", args.uri]
    logging.debug(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = process.communicate()
    logging.debug(out)
    args.uri = out.strip()

  message = AVTransportTemplate.replace("$DIDL", didl_lite).replace("$$$URI$$$", args.uri)
  logging.debug(message)
  sendMessage(args.ip, args.port, message)

  message = PlayTemplate
  logging.debug(message)
  sendMessage(args.ip, args.port, message)
  
main()

