import os
import pymongo
import gridfs

def dumpToDB(directory, lbl, prt):
	conn = pymongo.MongoClient()
	db = conn.NM_ImgData #Change DB Name accordingly
	fs = gridfs.GridFS(db)
	for file in os.listdir(directory):
		filename=os.fsdecode(file)
		with open(directory+"/"+filename,'rb') as img:
			b = fs.put(img, filename=filename, label=lbl, part=prt)
			print (filename, b)

directory = '/Users/sominwadhwa/Desktop/temp/nm/train/positive'
lbl = 'positive'
part = 'train'

dumpToDB(directory,lbl,part)