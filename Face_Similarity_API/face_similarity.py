# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:18:43 2019

@author: Internship010
"""

import face_similarity_api as FSA

CHOICE = int(input("Choose 1:Single Pair Checking\nChoose"
                   "2:Multiple Pair Checking From Folder\n"))
if CHOICE == 1:
    PERSON_NAME = input("Enter Path of Person Image : ")
    DOCUMENT_NAME = input("Enter Path of Document Image : ")
    N = int(input("Choices :\n1.Document Gender\n2.Person Gender\n"
                  "3.Both\n4.None\n"))
    FSA.compare(PERSON_NAME, DOCUMENT_NAME, N)
elif CHOICE == 2:
    FSA.start()
