## Precog-Task

### Description

**Task:** Build a simple Web Application, which when given an image, is able to detect a face (show with a boundary box) and give a result saying whether Narendra Modi and/or Arvind Kejriwal are present in the image or not.

#### Overview of the solution

**Brief description:**
1. Used 3 different classifier to process the image - A *Haar Cascade* clf to detect and draw boundry around the face and 2 *Convolutional Neural Networks* to further evaluate if it is Arvind Kejriwal and/or Narendra Modi.
2. Key Challenge - Sampling of images (positive and negative sets) to train CNNs. Segregation & and keeping negative samples of each kind in the cross-positive categories to build an effective classification system. In addition, keeping the **training** & **validation** datasets mutually exclusive.
3. Use flask to create a minimal web-app where you can upload the image. Deployed it on a DigitalOcean droplet.

**Directory Structure:**

    .
    .
    ├── collections                     # MongoDB exports of data in GridFS specification
    ├── src                             # source Files
    │   ├── train.py                    # training script
    │   ├── dump_collections.py         # script used to dump data into GridFS specs.
    │   ├── extract_img_example.py      # to extract data from gridFS specs
    ├── models                          # saved models               
    ├── static
    ├── templates
    ├── precog_task.py                  # execution script  
    ├── utils.py
    └── wsgi.py
    .
    .

**Structure of collection:**

The data is stored in GridFS specs in MongoDB. `dump_collections.py` was used to export data to MongoDB. To pass off all the data into the db, the script can be executed as - `python3 src/dump_collections.py -label "negative" -part "train" -path "/Users/sominwadhwa/Desktop/temp/nm/train/negative" `. Entries stored are of the form:

    {img_file_1, 'label':'positive', 'part':'train', 'person':'Arvind Kejriwal'}

Since the entire data is stored in GridFS specs, to extract it you can use the `extract_img_example.py` by first adding the collections to a temporary database -

    sudo mongorestore --db data_for_task --collection fs.chunks --out /data_for_task/fs.chunks.bson
    sudo mongorestore --db data_for_task --collection fs.chunks --out /data_for_task/fs.files.bson

To extract all images for `Arvind Kejriwal`, with `positive` class label & as part of `validation` dataset -

    python3 extract_img_example.py -person "Arvind Kejriwal" -label "positive" -part "validation"
