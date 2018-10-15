#!/usr/bin/python3


import xml.etree.cElementTree as ET
from xml.dom import minidom
from os.path import basename
from pathlib import Path


def createXML(inputFilepath, outputFilepath, classes, boundingBoxes):

	annotation = ET.Element("annotation")


	folder = ET.SubElement(annotation, "folder")
	folder.text = basename(str(Path(inputFilepath).parent))

	filename = ET.SubElement(annotation, "filename")
	filename.text = basename(inputFilepath)

	path = ET.SubElement(annotation, "path")
	path.text = inputFilepath
	# path.text = '/home/msardonini/mnt/superSmashCnn/imagesFromNet/' + basename(inputFilepath)

	source = ET.SubElement(annotation, "source")
	ET.SubElement(source, "database").text = "Unknown"

	size = ET.SubElement(annotation, "size")
	ET.SubElement(size, "width").text = "720"
	ET.SubElement(size, "height").text = "480"
	ET.SubElement(size, "depth").text = "3"

	segmented = ET.SubElement(annotation, "segmented")
	segmented.text = "0"

	for i in range(len(classes)):
		objectE= ET.SubElement(annotation, "object")

		if (classes[i] == 0):
			ET.SubElement(objectE, "name").text = "luigi"
		elif(classes[i] == 1):
			ET.SubElement(objectE, "name").text = "yoshi"
		elif(classes[i] == 2):
			ET.SubElement(objectE, "name").text = "DK"
		elif(classes[i] == 3):
			ET.SubElement(objectE, "name").text = "ness"
		elif(classes[i] == 4):
			ET.SubElement(objectE, "name").text = "mario"
		elif(classes[i] == 5):
			ET.SubElement(objectE, "name").text = "link"
		elif(classes[i] == 6):
			ET.SubElement(objectE, "name").text = "falcon"
		elif(classes[i] == 7):
			ET.SubElement(objectE, "name").text = "samus"
		elif(classes[i] == 8):
			ET.SubElement(objectE, "name").text = "kirby"
		elif(classes[i] == 9):
			ET.SubElement(objectE, "name").text = "pikachu"
		elif(classes[i] == 10):
			ET.SubElement(objectE, "name").text = "jigglypuff"
		elif(classes[i] == 11):
			ET.SubElement(objectE, "name").text = "fox"

		ET.SubElement(objectE, "pose").text = "Unspecified"
		ET.SubElement(objectE, "truncated").text = "0"
		ET.SubElement(objectE, "difficult").text = "0"
		bndBox = ET.SubElement(objectE, "bndbox")
		ET.SubElement(bndBox, "xmin").text = str(int(boundingBoxes[i][1]))
		ET.SubElement(bndBox, "xmax").text = str(int(boundingBoxes[i][3]))
		ET.SubElement(bndBox, "ymin").text = str(int(boundingBoxes[i][0]))
		ET.SubElement(bndBox, "ymax").text = str(int(boundingBoxes[i][2]))

	rough_string = ET.tostring(annotation)
	reparsed = minidom.parseString(rough_string)


	myStr = (reparsed.toprettyxml(indent="\t"))

	outputFile = open(outputFilepath, 'w+')
	outputFile.write(myStr)



if(__name__ is "__main__"):
	createXML('/home/msardonini/superSmashCnn/trainingImages/Luigi_Yoshi_DK_Jungle/rawImage00359.jpg', 'here.avi' , [0, 1], [[5, 10, 15, 20], [25, 30, 35, 40]])