'''
Created on Wed Dec 11 16:54:06 2019

@author: Internship010

'''

import json

import re

import os

import sys

import face_recognition.api as face_recognition

from PIL import Image

import numpy as np

from numpy import array

from keras.preprocessing.image import img_to_array

from keras.models import load_model

import cv2


def scan(img1, img2):
    """
    Read, Encode Person Image,document for comaprison and
    gender classification.
    """
    pil_img = Image.open(img1).convert('RGB')
    cv_img = array(pil_img)
    image1 = cv_img[:, :, ::-1].copy()
    encoding1 = face_recognition.face_encodings(image1)
    pil_img = Image.open(img2).convert('RGB')
    cv_img = array(pil_img)
    image2 = cv_img[:, :, ::-1].copy()
    encoding2 = face_recognition.face_encodings(image2)
    gimage1 = image1
    gimage1 = cv2.resize(gimage1, (96, 96))
    gimage1 = gimage1.astype("float") / 255.0
    gimage1 = img_to_array(gimage1)
    gimage1 = np.expand_dims(gimage1, axis=0)
    gimage2 = image2
    gimage2 = cv2.resize(gimage2, (96, 96))
    gimage2 = gimage2.astype("float") / 255.0
    gimage2 = img_to_array(gimage2)
    gimage2 = np.expand_dims(gimage2, axis=0)
    return encoding1, gimage1, encoding2, gimage2


def test(encoding1, encoding2):
    """
    Compare document with Person Image Encodings.
    """
    if len(encoding1) < 1 or len(encoding2) < 1:
        print("No Face Identified")
        sys.exit(0)
    for encodings2 in encoding2:
        distance = face_recognition.face_distance(encoding1, encodings2)
    similarity = distance_to_similarity(distance[0])
    similarity = float("{0:.2f}".format(similarity))
    return similarity



def distance_to_similarity(distance):
    """
    To Calculate Similarity From Distance.
    """
    similarity = 100 - 50*distance
    return similarity


def gender(image):
    """
    To Find Gender of Person.
    """
    model = load_model("gender_classification.model")
    confidence = model.predict(image)[0]
    if confidence[0] > confidence[1]:
        return "man"
    return "woman"



def image_files_in_folder(folder):
    """
    To get paths of image files in a folder.
    """
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match
            (r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def json_create(similarity, boolean, genp=None, gend=None):
    """
    To generate json output.
    """
    json_dict = {}
    json_dict["Similarity"] = similarity
    json_dict["Matched"] = boolean
    if genp is not None:
        json_dict["Gender_Person"] = genp
    if gend is not None:
        json_dict["Gender_document"] = gend
    with open('Face_Similarity_Output.json', 'w') as json_file:
        json.dump(json_dict, json_file)



def compare(img1, img2, choose_option, json_val=0):
    """
    Function to call single pair of Image & document is compared
    Gender is checked
    1 for document gender
    2 for person image gender
    3 for both
    4 for no gender output.
    """
    genp = None
    gend = None
    encoding1, gimage1, encoding2, gimage2 = scan(img1, img2)
    similarity = test(encoding1, encoding2)
    if choose_option == 3:
        genp = gender(gimage1)
        gend = gender(gimage2)
    elif choose_option == 1:
        gend = gender(gimage2)
    elif choose_option == 2:
        genp = gender(gimage1)
    boolean = similarity >= 70.0
    if json_val == 0:
        json_create(similarity, boolean, genp, gend)
    return(similarity, boolean, genp)


def start():
    """
    Function to call when Images and documents belonging to folder Input.
    """
    ul_dict = {}
    val_dict = {}
    people = image_files_in_folder("Input/image")
    doc = image_files_in_folder("Input/doc")
    for img1 in people:
        for img2 in doc:
            sim, pred, genp = compare(img1, img2, 2, json_val=1)
            val_dict.update({img2: (sim, pred)})
        ul_dict.update({img1: {genp: val_dict}})
        val_dict = {}
    with open('Output/output.json', 'w') as json_file:
        json.dump(ul_dict, json_file, indent=2, sort_keys=False)
