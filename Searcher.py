import numpy as np
import csv
import cv2
from matplotlib import pyplot as plt

class Searcher:
	def __init__(self, indexPath):
		self.indexPath = indexPath

	def search(self, queryFeatures, limit = 10):
		results = {} # initialize results
		# open the index file for reading
		with open(self.indexPath) as f:
			reader = csv.reader(f)

		# 	# loop over the rows in the index
			for row in reader:
		# compute the chi-squared distance between the features in our index and query features
				features = [float(x) for x in row[1:]]
				d = self.mse(features, queryFeatures)

				# udpate the results (the key is the image ID in the index and the value is the distance)
				results[row[0]] = d

			f.close()
		# sort our results
		results = sorted([(v, k) for (k, v) in results.items()])

		return results[:limit]

	def mse(self,imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	
		rs= np.square(np.subtract(imageA,imageB)).mean()
	
		# return the MSE, the lower the error, the more "similar"
		return rs

