#Major project Mid term without GUI

from PIL import Image
import numpy as np
import cv2

#from tkinter import *
 
def imgData(image):
  
                                  
    image = Image.open(image)
    image = np.array(image)
    print("Original list of pixels", image)
    dataSize = image.shape
    print("Pixels Size:",dataSize)
    
    data_1d = image.ravel() 
    print("\nPixels in Input image:",data_1d)
    
    return dataSize, data_1d

def message(textFile):                      

    f = open(textFile, 'r')
    mytext = f.read()
    
    length = str(bin(len(mytext)))
    print("Messasge length=",length)
    
    length = length[2:].zfill(10)               
    print("\n10 bit message length=",length)                                                         
    
    binarytxt = str(bin(int.from_bytes(mytext.encode(), 'big')))    
    print("\nBinary coversion of message from ascii =",binarytxt)
    
    binarytxt = length + binarytxt[2:]
    print("\nConactenation 10bit msg + Ascii's Binary=",binarytxt)
    
    binarytxt = [int(x) for x in list(binarytxt)]
    print("\nList of concatenation(Message Data)",binarytxt)
    return binarytxt

#odd pixel number into even 
def evenConvt(value):                            

    value = value + 1
    return max(0, min(254, value))

#even pixel to odd
def oddConvt(value):                            

    value = value + 1
    return max(0, min(255, value))


def encode(imgData , messageData, shape):

    for i in range(len(messageData)):    
        val = imgData[i] % 2
        if messageData[i] == 1:
            if val == 1: 
                pass
            else: imgData[i] = oddConvt(imgData[i])
        else:
            if val == 0: 
                pass
            else: imgData[i] = evenConvt(imgData[i])
   
    stegoimg = imgData.reshape(shape)
    print("\n3d array of Msg+ Pixels",stegoimg)
   
    return stegoimg



def decode(imgData):

    image = Image.open(imgData)
    image = np.array(image)

    data_1d = image.ravel()
    print("\n1d array of stego 3d list:",data_1d)
   
    strData = ""
    length = ""
    for i in range(10):                                       
        val = data_1d[i] % 2
        length += str(val)
    print("\n10 bit stego msg length:",length)
    
    length = '0b' + length
    print("\nBinary 10 bit: ",length)
    
    length = int(length,2) 
    print("\nDecimal value of binary 10 bit length:",length)
    
    length_1 = length * 8 + 9
    print ("\nTotal pixel length used(Msg bits+ reserved msg length bits):", length_1)
    
    for i in range(10, length_1):                      
        val = data_1d[i] % 2
        strData += str(val)
    print("\nBinary of Ascii msg bits:",strData) 
    
    strData = '0b' + strData
    print("\nBinary identifier **0b**:", strData)
    
    n = int(strData, 2)
    print("\nDecimal conversion of entire message bits: ", n)
    
    #decimal to indivual binary and binary to ascii
    asciiData = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode() #total binary number msglength
    #ceil(a/b)=(a+b-1)/b  a=23,b=8

    #print( (n.bit_length() + 7) // 8)

    print("\n****So the Hidden message in photo is**** :", asciiData)



if __name__ == '__main__':                              
#encoding image  
    data_Length ,img_Data = imgData('sunflower.png')
    message_Data = message('message.txt')
    img_age = encode(img_Data, message_Data, data_Length)
    img_age = cv2.cvtColor(img_age, cv2.COLOR_BGR2RGB)
    cv2.imwrite('result.png', img_age)
  
#decode the image     
                                  
 
decode('result.png')

#from tkinter import *