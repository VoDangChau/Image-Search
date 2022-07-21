from email.mime import image
from feature_extractor import FeatureExtractor
from Searcher import Searcher
import argparse
import cv2
import crop_image

def search_func(image):
	fe = FeatureExtractor((8, 12, 3)) # initialize the image extractor

	# load the query image and extract it
	query = image
	features = fe.extract(query)

	# perform the search
	searcher = Searcher('index.csv')
	results = searcher.search(features)

	# resize and display the query
	scale_percent = 100
	width = int(query.shape[1] * scale_percent / 165)
	height = int(query.shape[0] * scale_percent / 165)
	dim = (width, height)
	query = cv2.resize(query, dim, interpolation = cv2.INTER_AREA)

	cv2.imshow("Query", query)
	final_result = []

	for (score, resultID) in results:
		result = cv2.imread(resultID)

		# resize and display results
		scale_percent = 100
		width = int(result.shape[1] * scale_percent / 165)
		height = int(result.shape[0] * scale_percent / 165)
		dim = (width, height)
		result = cv2.resize(result, dim, interpolation = cv2.INTER_AREA)
		print(resultID)
		cv2.imshow("Result", result)
		final_result.append(resultID)
		cv2.waitKey(0)
	return final_result