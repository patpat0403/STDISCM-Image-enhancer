from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir
import matplotlib.pyplot as plt


def enhancer(img, brightness, sharpness, contrast):
    #change brightness first
    currImage= ImageEnhance.Brightness(img)
    newImage= currImage.enhance(brightness)

    currImage= ImageEnhance.Sharpness(newImage)
    newImage = currImage.enhance(sharpness)

    currImage=ImageEnhance.Contrast(newImage)
    newImage= currImage.enhance(contrast)

    return newImage


    





def main():
    ctr=1

    #location of reference images
    Ref_Loc = "C:\Dlsu stuff\STDISCM\STDISCM-Image-enhancer\Reference images"
    #location of enhanced images
    Enh_Loc=  "C:\Dlsu stuff\STDISCM\STDISCM-Image-enhancer\Enhanced images"
    #Enhancing time in units
    time = int(input("input time: "))
    #Brightness
    brightness= float(input("input brightness: "))
    #sharpness
    sharpness= float (input("input sharpness: "))
    #contrast
    contrast = float(input("input contrast: "))

    for img in listdir(Ref_Loc):
          curr = Image.open(Ref_Loc + '/' + img)
          curr.show()
          new_image = enhancer(curr, brightness, sharpness, contrast)
          new_image.show()
         
          
          
if __name__ == "__main__":
    main() 




