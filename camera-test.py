import cv
capture = cv.CaptureFromCAM(-1)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 960)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
im = cv.QueryFrame(capture)
cv.SaveImage("/home/pi/camera-test.jpg", im)
