import cv
import urllib2
import time
import math

#grab an image from the camera and save it
capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
im = cv.QueryFrame(capture)
cv.SaveImage("/home/pi/dish/capture/sink-latest.jpg", im)

#convert the image to grayscale
edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(im, edges, cv.CV_BGR2GRAY)

#edge detect it, then smooth the edges
thresh = 120
cv.Canny(edges, edges, thresh, thresh / 2, 3)
cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 3, 3) 
cv.SaveImage("/home/pi/dish/capture/sink-latest-edges.jpg", edges)

#find the circles
storage = cv.CreateMat(640, 1, cv.CV_32FC3)
cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, edges.width / 10, thresh, 160, 0, 0)

#read where the drains are
dirty = False
f = open("/home/pi/dish/sink-empty.txt", "r")
drains = []
for line in f:
    val = line.split(",")
    drains.append((int(val[0]), int(val[1]), int(val[2])))

#match circles with drains
tolerance = 12
for i in range(storage.rows):
    val = storage[i, 0]
    centerX = int(val[0])
    centerY = int(val[1])
    radius = int(val[2])
    isdrain = False
    for j in range(len(drains)):
        if abs(centerX - drains[j][0]) < tolerance:
            if abs(centerY - drains[j][1]) < tolerance:
                if abs(radius - drains[j][2]) < tolerance:
                        if drains[j][2] != 0:
                            isdrain = True
                            drains[j] = (drains[j][0], drains[j][1], 0)
    if isdrain:
        cv.Circle(im, (centerX, centerY), radius, (0, 255, 0), thickness=2) 
    else:
        dirty = True
        print "circular feature at: " + str(centerX) + "," + str(centerY) + " size: " + str(radius)
        cv.Circle(im, (centerX, centerY), radius, (0, 0, 255), thickness=3)

#test for drains not seen
for j in range(len(drains)):
    if drains[j][2] != 0:
        #dirty = True
        print "drain not found at: " + str(drains[j][0]) + "," + str(drains[j][1])
        cv.Circle(im, (drains[j][0], drains[j][1]), 10, (255, 0, 0), thickness=3) 

#save an image for debug
cv.SaveImage("/home/pi/dish/capture/sink-latest-circles.jpg", im)

#load last status
import os.path
status = "/home/pi/dish/status.txt"
if os.path.isfile(status):
    f = open(status, "r")
    wasDirty = f.readline() == "dirty"
    print "wasDirty: " + str(wasDirty)
    f.close()
else:
    wasDirty = False
    
#save new status
print "dirty: " + str(dirty)
f = open(status, "w")
if dirty:
    f.write("dirty")
else:
    f.write("clean")
f.close()

#send hipchat notification
time = math.ceil(time.time())
dirtyurl = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=adfa81620ff9b4c9756302cfb7e17d&room_id=920103&from=DishBot&message=Someone+here+left+their+dishes+in+the+sink!+http://raspbeat01.local/sink-latest.jpg?%(time)s&message_format=text&color=yellow&notify=1" % locals()
cleanurl = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=adfa81620ff9b4c9756302cfb7e17d&room_id=920103&from=DishBot&message=Yo!+The+sink+is+clean+now.+Let's+keep+it+that+way!+http://raspbeat01.local/sink-latest.jpg?%(time)s&message_format=text&color=green&notify=1" % locals()
#post the image directly to hipchat
#imageurl = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=adfa81620ff9b4c9756302cfb7e17d&room_id=920103&from=DishBot&message=http://raspbeat01.local/sink-latest.jpg&message_format=text&color=gray&notify=1"

if dirty and not wasDirty:
    request = urllib2.Request(dirtyurl)
    response = urllib2.urlopen(request)
    print "The sink just became DIRTY. Sent a message!"
    print response.read()
    request = urllib2.Request(imageurl)
    response = urllib2.urlopen(request)
    print response.read()
elif not dirty and wasDirty:
    request = urllib2.Request(cleanurl)
    response = urllib2.urlopen(request)
    print "The sink just became CLEAN. Sent a message!"
    print response.read()
    request = urllib2.Request(imageurl)
    response = urllib2.urlopen(request)
    print response.read()