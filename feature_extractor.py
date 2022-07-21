import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

class FeatureExtractor:
	def __init__(self, bins):
		self.bins = bins # store the number of bins for the 3D histogram

	def extract(self, image):
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert the image to the HSV
		features = [] # initialize the features
		
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5)) # center of the image

		# divide the image into 4 segments (top-left, top-right, bottom-right, bottom-left)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
			(0, cX, cY, h)]
		# construct an elliptical mask representing the center of the image
		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
		
		# loop over the segments
		for (startX, endX, startY, endY) in segments:
			# construct a mask for each corner of the image and subtract the elliptical center
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			# extract a color histogram from the corner and update the feature vector
			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		# extract a color histogram from the elliptical and update the feature vector
		hist = self.histogram(image, ellipMask)
		features.extend(hist)
		
		return features


	def histogram(self, image, mask):
		# extract a 3D color histogram from the masked region of the image
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])

		# normalize the histogram
		hist = cv2.normalize(hist, hist).flatten()
		
		return hist
