from cProfile import label
import imghdr
from importlib.resources import path
from tkinter import *
from tkinter.font import BOLD
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from Searcher import Searcher
import argparse
import os
import cv2
import numpy as np
import crop_image
import search

root = Tk()
root.geometry("1080x720")

refPt = []
cropping = False
img = None
filepath = None
#final_result = None

def open_img():
    global filepath 
    global img
    filepath = filedialog.askopenfilename(title ='"pen')
    img = Image.open(filepath)
    basewidth = 160
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.image = img
    panel.grid(row = 2)
    img = cv2.imread(filepath)

def crop():
    global filepath
    global img
    img = crop_image.crop_img(img)

def submit():
    global img
    global final_result
    final_result = search.search_func(img)
    #search.search_func(img)
    col=0
    row=6
    for f in final_result:
        img=Image.open(f) # read the image file
        basewidth = 140
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img=ImageTk.PhotoImage(img)
        e1 =Label(root)
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection 
        if(col==4): # start new line after third column
            row=row+1# start wtih next row
            col=0    # start with first column
        else:       # within the same row 
            col=col+1 # increase to next column     


root.title("Super Vippro Image Search Engine")

root.resizable(width = True, height = True)
 
btn_openImg = Button(root, text ='Open image', command = open_img).grid(row = 1, columnspan = 4)

btn_crop = Button(root, text='Crop', command = crop).grid(row = 3, columnspan = 4)

btn_submit = Button(root, text='Submit', command=submit).grid(row = 5, columnspan = 4)

root.mainloop()