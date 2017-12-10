import os
import pymongo
import gridfs

conn = pymongo.MongoClient()
db = conn.AK_ImgData #Change DB Name accordingly
fs = gridfs.GridFS(db)

for grid_out in fs.find({'label':'positive', 'part':'validation'}):
    b = grid_out.read()
    outfilename = grid_out.filename
    output= open(outfilename,"wb")
    output.write(b)
    output.close()
    print (outfilename)