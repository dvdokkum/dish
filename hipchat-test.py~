import urllib2

url = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=adfa81620ff9b4c9756302cfb7e17d&room_id=920103&from=DishBot&message=@here+clean+your+dishes&message_format=text&color=yellow&notify=1"
request = urllib2.Request(url)
response = urllib2.urlopen(request)

print response.read()