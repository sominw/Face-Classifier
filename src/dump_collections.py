import os, argparse
import pymongo
import gridfs

def dumpToDB(directory, lbl, prt, person):
	conn = pymongo.MongoClient()
	db = conn.data_for_task #Change DB Name accordingly
	fs = gridfs.GridFS(db)
	for file in os.listdir(directory):
		filename=os.fsdecode(file)
		with open(directory+"/"+filename,'rb') as img:
			b = fs.put(img, filename=filename, label=lbl, part=prt, person=person)
			print (filename, b)

#Alter the three params accordingly or pass them off as args

parser = argparse.ArgumentParser()
parser.add_argument('-person', type=str, default='Arvind Kejriwal')
parser.add_argument('-label', type=str, default='positive')
parser.add_argument('-part', type=str, default='train')
parser.add_argument('-path', type=str, default='/Users/sominwadhwa/Desktop/temp/ak/train/positive')
args = parser.parse_args()

dumpToDB(args.path, args.label, args.part, args.person)