# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:54:06 2019

@author: Internship010
"""
import face_recognition.api as face_recognition

import cv2

from PIL import Image

import numpy as np

from numpy import array

from keras.preprocessing.image import img_to_array

from keras.models import load_model

import json

import re

import os

#Read and Encode Person Image, Document for both comaprision and gender classification
def scan(img1,img2):
    pil_img = Image.open(img1).convert('RGB')
    cv_img = array(pil_img)
    image1 = cv_img[:,:,::-1].copy()
    encoding1 = face_recognition.face_encodings(image1)
    
    pil_img = Image.open(img2).convert('RGB')
    cv_img = array(pil_img)
    image2 = cv_img[:,:,::-1].copy()   
    encoding2 = face_recognition.face_encodings(image2)
    
    gimage1 = image1
    gimage1 = cv2.resize(gimage1, (96,96))

    gimage1 = gimage1.astype("float") / 255.0

    gimage1 = img_to_array(gimage1)

    gimage1 = np.expand_dims(gimage1, axis=0)
    
    gimage2 = image2
    gimage2 = cv2.resize(gimage2, (96,96))

    gimage2 = gimage2.astype("float") / 255.0

    gimage2 = img_to_array(gimage2)

    gimage2 = np.expand_dims(gimage2, axis=0)

    
    return image1,encoding1,gimage1,image2,encoding2,gimage2

#Compare Document with Person Image Encodings
def test(image1,encoding1,image2,encoding2):
    
    for encodings2 in encoding2:
        distance = face_recognition.face_distance(encoding1,encodings2)
        
    similarity = distance_to_similarity(distance[0])
    similarity = float("{0:.2f}".format(similarity))               
    return similarity 

#To Calculate Similarity From Distance
def distance_to_similarity(distance):
    similarity = 100 - 50*distance
    return similarity

#To Find Gender of Person
def gender(image):
    model = load_model("gender_classification.model") 
    confidence = model.predict(image)[0]
    if(confidence[0] > confidence[1]):
        return("man")
    else:
        return("woman")

#To get paths of image files in a folder
def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

#To generate json output
def JSON(similarity,Bool,genp=None,gend=None):
    Json_Dict = {}
    Json_Dict["Similarity"]=similarity
    Json_Dict["Matched"]=Bool
    if genp != None:
        Json_Dict["Gender_Person"]=genp
    if gend != None:
        Json_Dict["Gender_Document"]=gend
    with open('Face_Similarity_Output.json','w') as Json_File:
        json.dump(Json_Dict,Json_File)

#Function to call when single pair of Image and Document is compared and checked for gender
# 4 for no gender output
# 2 for person image gender
# 1 for document gender
# 3 for both        
def compare(img1,img2,Choice,Json = 0):
    genp = None
    gend = None
    
    image1,encoding1,gimage1,image2,encoding2,gimage2 = scan(img1,img2)
    similarity = test(image1,encoding1,image2,encoding2)
    
    if Choice == 3:
        genp = gender(gimage1)
        gend = gender(gimage2)
    elif Choice == 1:
        gend = gender(gimage2)
    elif Choice == 2:
        genp = gender(gimage1)
        
    if similarity >= 70.0:
            Bool=True
    else:
            Bool=False
    
    if Json == 0:
        JSON(similarity,Bool,genp,gend)           
    else:
        return(similarity,Bool,genp,gend)

#Function to call when Images and Documents belonging to folder Input are to be checked        
def start():
    ul_dict={}
    val_dict={}
    
    People = image_files_in_folder("Input/image")
    Doc = image_files_in_folder("Input/doc")
    for img1 in People:
        for img2 in Doc:
            sim,pred,genp,gend=compare(img1,img2,2,Json = 1)
            val_dict.update({img2:sim})
        ul_dict.update({img1:{genp:val_dict}})
        val_dict={}
    with open('Output/output.json','w') as Json_File:
        json.dump(ul_dict,Json_File,indent=2,sort_keys=False)