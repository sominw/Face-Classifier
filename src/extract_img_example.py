import os
import pymongo
import gridfs

parser = argparse.ArgumentParser()
parser.add_argument('-person', type=str, default='Arvind Kejriwal')
parser.add_argument('-label', type=str, default='positive')
parser.add_argument('-part', type=str, default='train')

args = parser.parse_args()

conn = pymongo.MongoClient()
db = conn.data_for_task #Change DB Name accordingly
fs = gridfs.GridFS(db)

for grid_out in fs.find({'label':args.label, 'part':args.part, 'person':args.person}):
    b = grid_out.read()
    outfilename = grid_out.filename
    output= open(outfilename,"wb")
    output.write(b)
    output.close()
    print (outfilename)