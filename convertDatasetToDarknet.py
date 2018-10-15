#!/usr/bin/python3

from shutil import copyfile
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join
from shutil import copyfile
import os
import numpy as np

# labelsFolders = ['labels/Luigi_Yoshi_Dreamland/' , 'labels/Luigi_Yoshi_DK_Jungle/' , 'labels/Luigi_Yoshi_DK_Island/', 'labels/Luigi_Kirby_Jiggly_Samus_Dreamland/', 'labels/DK_Ness_Kirby_Falcon_Dreamland_Castle/', 'labels/DK_Fox_Pika_Starfox/']


# imageFolders = ['trainingImages/Luigi_Yoshi_Dreamland/' , 'trainingImages/Luigi_Yoshi_DK_Jungle/' , 'trainingImages/Luigi_Yoshi_DK_Island/', 'trainingImages/Luigi_Kirby_Jiggly_Samus_Dreamland/', 'trainingImages/DK_Ness_Kirby_Falcon_Dreamland_Castle/', 'labels/DK_Fox_Pika_Starfox/']
# labelsFolders = [ 'DK_Fox_Pika_Starfox/']

createDarknetLabels = True

labelsFolders = listdir('labels')
imageFolders = listdir('labels')


#Create a file to store the locations of images
imageListFile = open('darknet/trainImages.list', 'w')

#Some Global Variables
imageNumber = int(0)
cwd = os.getcwd()

numLabelsPerChar = np.zeros(12)

for folder in labelsFolders:
	
	onlyfiles = [f for f in listdir('labels/' + folder) if isfile(join('labels/' + folder, f))]
	for xmlFile in onlyfiles:
		num_boxes = 0
		difficulty = False
		bndbox = []
		bndboxDarkNet = []
		label = []
		bndboxString = []
		bndboxStringDarkNet = []


		#Parse the XML file to create labels
		tree = ET.parse('labels/' + folder + '/' + xmlFile)
		
		root = tree.getroot()
		for child in root:
		# print (child.tag)
			if(child.tag == "filename"):
				filename = child.text
			if(child.tag == "path"):
				path = child.text
			if (child.tag == "object"):
				for child2 in child:
					if(child2.tag == "difficult"):
						if(child2.text is '1'):
							difficulty = True
					if(child2.tag == "name"):
					# print(child2.text)
						if(child2.text == "luigi"):
							label.append(0)
							num_boxes += 1
							numLabelsPerChar[0] += 1
						elif (child2.text == "yoshi"):
							label.append(1)
							num_boxes += 1
							numLabelsPerChar[1] += 1
						elif (child2.text == "DK"):
							label.append(2)
							num_boxes += 1
							numLabelsPerChar[2] += 1
						elif (child2.text == "ness"):
							label.append(3)
							num_boxes += 1
							numLabelsPerChar[3] += 1
						elif (child2.text == "mario"):
							label.append(4)
							num_boxes += 1
							numLabelsPerChar[4] += 1
						elif (child2.text == "link"):
							label.append(5)
							num_boxes += 1
							numLabelsPerChar[5] += 1
						elif (child2.text == "falcon"):
							label.append(6)
							num_boxes += 1
							numLabelsPerChar[6] += 1
						elif (child2.text == "samus"):
							label.append(7)
							num_boxes += 1
							numLabelsPerChar[7] += 1
						elif (child2.text == "kirby"):
							label.append(8)
							num_boxes += 1
							numLabelsPerChar[8] += 1
						elif (child2.text == "pikachu"):
							label.append(9)
							num_boxes += 1
							numLabelsPerChar[9] += 1
						elif (child2.text == "jigglypuff"):
							label.append(10)
							num_boxes += 1
							numLabelsPerChar[10] += 1
						elif (child2.text == "fox"):
							label.append(11)
							num_boxes += 1
							numLabelsPerChar[11] += 1
					if(child2.tag == "bndbox"):

						numVals = 0
						for child3 in child2:
							if (child3.tag == 'xmin'):
								xmin = float(child3.text)
								numVals += 1
							if (child3.tag == 'xmax'):
								xmax = float(child3.text)
								numVals += 1
							if (child3.tag == 'ymin'):
								ymin = float(child3.text)
								numVals += 1
							if (child3.tag == 'ymax'):
								ymax = float(child3.text)
								numVals += 1


						X = (xmin + xmax) / 2 / 720
						Y = (ymin + ymax) / 2 / 480
						dX = (xmax - xmin) / 720
						dY = (ymax - ymin) / 480
						
						#If we didn't get 4 values from this file, disregard the image using difficulty flag
						if (numVals is not 4):
							difficulty = True

						bndboxDarkNet.append([X, Y, dX, dY])

						if (dX < 0 or dY < 0):
							print("Error less than 0!!!")
							quit()

		if (not difficulty and num_boxes is not 0):
			imageNumber += 1
			# Copy the image from its original directory to the new one
			srcImage = 'trainingImages/' + folder + '/' + xmlFile[0:-4] + '.jpg'
			dstImage = 'darknet/trainImages/' + str(imageNumber).zfill(6) + '.jpg'
			copyfile(srcImage, dstImage)
			
			#Write the name of the created image to our image list
			imageListFile.write(cwd + '/' + dstImage + '\n')

			outputLabelsDarknet = open('darknet/trainImages/' + str(imageNumber).zfill(6) + '.txt', 'w')
			# outputLabelsDarknet = open('darknet/labels/' + str(imageNumber).zfill(6) + '.txt', 'w')
			
			for i in range(num_boxes):
					
				bndboxStringDarkNet.append(str(bndboxDarkNet[i][0]) + " " + str(bndboxDarkNet[i][1]) + " " + str(bndboxDarkNet[i][2]) + " " + str(bndboxDarkNet[i][3]))

			for i in range(num_boxes):
				if i is not 0:
					outputLabelsDarknet.write('\n')
				outputLabelsDarknet.write(str(label[i]) + " " + str(bndboxStringDarkNet[i]) )

			outputLabelsDarknet.close()



print("Number  of chars")
print(numLabelsPerChar)