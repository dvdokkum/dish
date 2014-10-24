import cv
capture = cv.CaptureFromCAM(-1)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 960)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
im = cv.QueryFrame(capture)
cv.SaveImage("/home/pi/dish/capture/camera-test.jpg", im)
 
edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(im, edges, cv.CV_BGR2GRAY)
thresh = 100
cv.Canny(edges, edges, thresh, thresh / 2, 3)
cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 3, 3)
storage = cv.CreateMat(640, 1, cv.CV_32FC3)
cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, edges.width / 10, thresh, 350, 0, 0)
# f = open("/home/pi/dish/sink-empty.txt", "w")
# for i in range(storage.rows):
#     val = storage[i, 0]
#     radius = int(val[2])
#     center = (int(val[0]), int(val[1]))
#     f.write(str(center[0]) + "," + str(center[1]) + "," + str(radius) + "\n")
#     cv.Circle(im, center, radius, (0, 255, 0), thickness=2)
# cv.SaveImage("/home/pi/dish/capture/sink-empty.jpg", im)
 
dirty = False
f = open("/home/pi/dish/sink-empty.txt", "r")
drains = []
for line in f:
    val = line.split(",")
    drains.append((int(val[0]), int(val[1]), int(val[2])))
tolerance = 10
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
for j in range(len(drains)):
    if drains[j][2] != 0:
        dirty = True
        print "drain not found at: " + str(drains[j][0]) + "," + str(drains[j][1])
        cv.Circle(im, (drains[j][0], drains[j][1]), 10, (255, 0, 0), thickness=3) 
cv.SaveImage("/home/pi/dish/capture/sink-latest.jpg", im)
