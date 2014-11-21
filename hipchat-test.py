import urllib2

# insert your auth token

url = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=XXXXXXXXXXXXXX&room_id=920103&from=DishBot&message=@here+clean+your+dishes&message_format=text&color=yellow&notify=1"
request = urllib2.Request(url)
response = urllib2.urlopen(request)

print response.read()
