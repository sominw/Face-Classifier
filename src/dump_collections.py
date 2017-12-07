import os
import pymongo
import gridfs

def dumpToDB(directory, lbl, prt):
	conn = pymongo.MongoClient()
	db = conn.AK_ImgData #Change DB Name accordingly
	fs = gridfs.GridFS(db)
	for file in os.listdir(directory):
		filename=os.fsdecode(file)
		with open(directory+"/"+filename,'rb') as img:
			b = fs.put(img, filename=filename, label=lbl, part=prt)
			print (filename, b)

#Alter the three params accordingly or pass them off as args
directory = '/Users/sominwadhwa/Desktop/temp/ak/train/positive'
lbl = 'positive'
part = 'train'

dumpToDB(directory,lbl,part)