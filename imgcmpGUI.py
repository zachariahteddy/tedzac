#!/usr/bin/python

import tkMessageBox
import PIL.Image
import ImageChops, sys, os, re
from Tkinter import *
from math import sqrt
from urllib import urlretrieve

def check():
  try:
    link1=lk1.get()                                                                # Reading link for image1
    link2=lk2.get()                                                                # Reading link for image2
     
    
    file1 = 'image1'                                                               # Creating a temporary file named 'image1'
    file2 = 'image2'                                                               # Creating a temporary file named 'image2'                                                           

    urlretrieve(link1, file1)                                                      # Downloading and saving to file 'image1'
    urlretrieve(link2, file2)                                                      # Downloading and saving to file 'image2'

    diff_perc_seq = []

    image1 = PIL.Image.open(file1)                                                 # Opening the downloaded file
    image2 = PIL.Image.open(file2)
 
    
    image1, image2 = samesize(image1, image2)                                       # Making the sizes of images equal.

    difference_in_image = ImageChops.difference(image1, image2)                     # difference_in_image contains the pixel level difference as an RGB tuple.

    
    if difference_in_image.getbbox() is None:                                       # getbbox returns box containing the non-zero regions of the image. If its none, difference is none..!
        tkMessageBox.showinfo('Mirror Images..!',' The images are 100% similar. Similarity Scale value - 100')
       
    else:
        pixel_tuple_seq = difference_in_image.getdata()                             # pixel_tuple_seq contains the list of difference pixel tuples(R, G, B).


        pixel_rms_seq = map(rms, pixel_tuple_seq)                                   # pixel_rms_seq contains the rms list of difference pixel tuples.
                                                                                    # The percentage of difference is found out using formula, perc = (value/255) * 100
        for item in pixel_rms_seq:
            diff_perc_seq.append(item/255*100)
        avg_diff = sum(diff_perc_seq)/len(diff_perc_seq)                            # The total average difference is found out.
        similarity = 100 - avg_diff

        if avg_diff == 100:
	    tkMessageBox.showinfo('Images Dissimilar','The images are completely dissimilar. Similarity scale value - 0')
          
        else:
	    tkMessageBox.showinfo('Images Similar','The images are %.2f%% similar. Similarity scale value - %.2f ' %(similarity, similarity))
           
    os.system('rm ' + file1 + ' ' + file2)
  except ValueError:
    tkMessageBox.showwarning('Entry Missing!','Please fill up all entries')  
  mGui.destroy()
  return;

def samesize(image1, image2):                                                        # Checks for disparity in image sizes & makes it same.
    if image1.size > image2.size:
        image2 = image2.resize(image1.size, PIL.Image.BICUBIC)
    elif image2 > image1:
        image1 = image1.resize(image2.size, PIL.Image.BICUBIC)

    return image1, image2

def rms(list):                                                                       # Returns the Root Mean Square value of a set of numbers.'''
    sum = 0

    for item in list:
        sum += item * item

    mean = sum/len(list)
    return sqrt(mean)  




mGui = Tk()
mGui.geometry("500x100+525+300")                                                     # Creating a GUI
mGui.title("IMAGE COMPARISON")

Label(mGui,text="Please enter the Image Files of same type:", fg="red",font="Verdana 10 bold").grid(column=1)
Label(mGui,text="Link for first image: ").grid(row=1,column=0)
lk1=Entry(mGui)                                                                      # Entry field for link of image1
lk1.grid(row=1,column=1)

    
Label(mGui,text="Link for second image:").grid(row=2,column=0)
lk2=Entry(mGui)                                                                      # Entry field for link of image2
lk2.grid(row=2,column=1)

mButton=Button(mGui,text="SUBMIT",command=check).grid(row=4,column=1)
mGui.mainloop() 
 
   
    



