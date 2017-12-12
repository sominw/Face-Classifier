## Precog-Task

### Description

**Task:** Build a simple Web Application, which when given an image, is able to detect a face (show with a boundary box) and give a result saying whether Narendra Modi and/or Arvind Kejriwal are present in the image or not.

<p align="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/1.png?raw=true"/>
</p>

### Overview of the solution

**Brief description:**
1. Used 3 different classifiers to process the image - A *Haar Cascade* clf to detect and draw boundry around the face and *2 Convolutional Neural Networks* to further evaluate if it is Arvind Kejriwal and/or Narendra Modi.
2. Key Challenge - Sampling of images (positive and negative sets) to train CNNs. Segregation & and keeping negative samples of each kind in the cross-positive categories to build an effective classification system. In addition, keeping the **training** & **validation** datasets mutually exclusive. Also used `flow_generator` to overcome the limitation of limited data to create multiple variants of the same image.
<p align="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/6.png?raw=true"/>
</p>
3. Used flask to create a minimal web-app where you can upload the image. Deployed it on a DigitalOcean droplet.


**Particulars:**
- **Data Collection:** Used `Fatkun Batch Image` chrome extension to extract data from Google Images.
- **Train-Validation split**: Nearly `80:20` split. 80% data used to train, the rest is used to cross-validate.
- Training carried out on [FloydHub's](https://www.floydhub.com/) CPU instances.

<p float="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/namo.png?raw=true"/>
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/ak.png?raw=true"/>
</p>

<p float="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/namo_loss.png?raw=true"/>
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/ak_loss.png?raw=true"/>
</p>

>Given higher compute, the same/different architectures can be experimented with higher number of epochs

- **Deployment:** DigitalOcean droplet.

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

    sudo mongorestore --db data_for_task --collection fs.chunks /data_for_task/fs.chunks.bson
    sudo mongorestore --db data_for_task --collection fs.chunks /data_for_task/fs.files.bson

To extract all images for `Arvind Kejriwal`, with `positive` class label & as part of `validation` dataset -

    python3 extract_img_example.py -person "Arvind Kejriwal" -label "positive" -part "validation"

### Potential Limitations

The entirety of this minimal-webapp has a few limitations. Due to the nature of the training data (preserve covariance, reduce randomness in samples), the detection of whether the image is of AK or NaMo will only happen **if haar-cascade clf is able to detect a face**, if however even a single face is detected, CNNs might be able to correctly classify the image. Altering `scale_factor` param of haar_cascade might as well alter the results in cases where facial propotionals are unusally large as compared to the size of the image. -

<p align="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/2.png?raw=true"/>
</p>

Cases where this may happen:
- Face covered with some form of obstacle.
- Unusually large face proportions as compared to the size of the photo.
- Varying viewing angles.

*How to overcome this? RCNNs is an approach that can be tried out to resolve this sort of an issue.*

---
Some more samples
---

>The following samples were taken at the time of development, actual testing results may vary as the final model (weights) get updated periodically.

<p align="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/3.png?raw=true"/>
</p>

<p align="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/4.png?raw=true"/>
</p>

<p align="center">
  <img src="https://github.com/sominwadhwa/precog_task/blob/master/static/etc/5.png?raw=true"/>
</p>
