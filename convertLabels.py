#!/usr/bin/python3

import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join
from shutil import copyfile


# labelsFolders = ['labels/Luigi_Yoshi_Dreamland/' , 'labels/Luigi_Yoshi_DK_Jungle/' , 'labels/Luigi_Yoshi_DK_Island/', 'labels/Luigi_Kirby_Jiggly_Samus_Dreamland/', 'labels/DK_Ness_Kirby_Falcon_Dreamland_Castle/', 'labels/DK_Fox_Pika_Starfox/']
# labelsFolders = [ 'DK_Fox_Pika_Starfox/']

createDarknetLabels = False

labelsFolders = listdir('labels')


# print(onlyfiles)
outputFile = open('annotation/train_annotation/trainAnnotations.csv', 'w')

if(createDarknetLabels):
	outputNamesDarknet = open('annotation/train_annotation/darknetTrainNames.txt', 'w')
	outputLabelsDarknet = open('annotation/train_annotation/darknetTrainLabels.txt', 'w')

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
						elif (child2.text == "yoshi"):
							label.append(1)
							num_boxes += 1
						elif (child2.text == "DK"):
							label.append(2)
							num_boxes += 1
						elif (child2.text == "ness"):
							label.append(3)
							num_boxes += 1
						elif (child2.text == "mario"):
							label.append(4)
							num_boxes += 1
						elif (child2.text == "link"):
							label.append(5)
							num_boxes += 1
						elif (child2.text == "falcon"):
							label.append(6)
							num_boxes += 1
						elif (child2.text == "samus"):
							label.append(7)
							num_boxes += 1
						elif (child2.text == "kirby"):
							label.append(8)
							num_boxes += 1
						elif (child2.text == "pikachu"):
							label.append(9)
							num_boxes += 1
						elif (child2.text == "jigglypuff"):
							label.append(10)
							num_boxes += 1
						elif (child2.text == "fox"):
							label.append(11)
							num_boxes += 1
					if(child2.tag == "bndbox"):

						numVals = 0
						for child3 in child2:
							if (child3.tag == 'xmin'):
								xmin = child3.text
								numVals += 1
							if (child3.tag == 'xmax'):
								xmax = child3.text
								numVals += 1
							if (child3.tag == 'ymin'):
								ymin = child3.text
								numVals += 1
							if (child3.tag == 'ymax'):
								ymax = child3.text
								numVals += 1
						if (numVals == 4):
							bndbox.append([xmin, ymin, xmax, ymax])


		if (not difficulty and num_boxes is not 0):
			for i in range(num_boxes):
				bndboxString.append(','.join(map(str, bndbox[i])))

			outputFile.write(str(path))

			for i in range(num_boxes):
				outputFile.write(" " + str(bndboxString[i]) + "," +  str(label[i]))
			
			outputFile.write('\n')


outputFile.close()
# print(ET.tostring(root[6]))

# for child in root[6][4]:
#     print (child.tag, child.text)

	# for key in root[i].attrib:
	#     print ("key: %s , value: %s" % (key, mydictionary[key]))

# for child in root[1]:
