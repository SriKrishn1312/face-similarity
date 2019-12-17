# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:18:43 2019

@author: Internship010
"""

import Face_Similarity_API as FSA

Choice = int(input("Choose 1 : Single Pair Checking \nChoose 2 : Multiple Pair Checking From Folder\n"))
if Choice == 1:
    Person = input("Enter Path of Person Image : ")
    Document = input("Enter Path of Document Image : ")
    n=int(input("Choices :\n1.Document Gender\n2.Person Gender\n3.Both\n4.None\n"))    
    FSA.compare(Person,Document,n)
elif Choice == 2:    
    FSA.start()    