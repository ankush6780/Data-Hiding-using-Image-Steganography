from tkinter import *

from PIL import Image
import numpy as np
from cv2 import cv2
import os

d_path = ""
s_path = ""
dec_path = ""


def img_ConvToPNG():
    global s_path, d_path
    s_path = str(l.get())
    d_path = str(m.get() + c.get())
    print(s_path)
    print(d_path)

    im = Image.open(s_path)
    im.save(d_path)

def imgData():  
   
    a = d_path
    global dataSize, data_1d
    image = Image.open(a)
    image = np.array(image)
    
    print("Original list of pixels", image)
    dataSize = image.shape
    
    data_1d = image.ravel()
    print("\nPixels in Input image:",data_1d)


def message():  
    inp = inputtxt.get("1.0", "end-1c")
    mytext = inp
    global binarytxt
    
    length = str(bin(len(mytext)))
    print("Messasge length=",length)
    
    length = length[2:].zfill(10)  
    print("\n10 bit message length=",length)

    binarytxt = str(bin(int.from_bytes(mytext.encode(), 'big')))
    print("\nBinary coversion of message from ascii =",binarytxt)
    
    binarytxt = length + binarytxt[2:]
    print("\nConactenation 10bit msg + Ascii's Binary=",binarytxt)
    
    binarytxt = [int(x) for x in list(binarytxt)]
    print(binarytxt)

#odd pixel number into even
def evenConvt(value):
    value = value + 1
    return max(0, min(254, value))

#even pixel to odd
def oddConvt(value):  
    value = value + 1
    return max(0, min(255, value))


def encode():  

    for i in range(
            len(binarytxt)):  
        val = data_1d[i] % 2
        if binarytxt[i] == 1:
            if val == 1:
                pass
            else:
                data_1d[i] = oddConvt(data_1d[i])
        else:
            if val == 0:
                pass
            else:
                data_1d[i] = evenConvt(data_1d[i])

    global stegoimg
    stegoimg = data_1d.reshape(dataSize)
    print("\n3d array of Msg+ Pixels",stegoimg)



def decode():
    global dec_path
    dec_path = str(ds.get())
    image = Image.open(dec_path)
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
   
    length = int(length, 2)
    print("\nDecimal value of binary 10 bit length:",length)
    
    length_1 = length * 8 + 9
    print ("\nTotal pixel length used(Msg bits+ reserved msg length bits):", length_1)

    for i in range(10, length_1):
        val = data_1d[i] % 2
        strData += str(val)
    print("\nBinary of Ascii msg bits:",strData) 
    
    strData = '0b' + strData
    print("\nBinary identifier **0b**:", strData)
    
    global asciiData

    n = int(strData, 2)
    print("\nDecimal conversion of entire message bits: ", n)
    
    asciiData = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    print("\n****So the Hidden message in photo is**** :", asciiData)
    
    global Decoded_message
    Decoded_message = str(asciiData)
    head_tail = os.path.split(dec_path)
    nice = head_tail[0] + "/DecMessage.txt"
    f11 = open(nice, "w")
    f11.write(str(asciiData))
    f11.close()


def save():
    sa = cv2.cvtColor(stegoimg, cv2.COLOR_BGR2RGB)
    cv2.imwrite(d_path, sa)

def p1():
    img_ConvToPNG()
    imgData()
    message()
    encode()
    save()


def p2():
    decode()
    decMessage()


def encWin():
    root = Toplevel(parent)
    root.grab_set()  
    root.geometry("800x500")
    root['bg']='black'
 
    global q, l, si_path, di_path, c, m, inp

    label1 = Label(root, text="File Format:",bg='red', fg='white', font=("Times", 18)).pack()
    q = IntVar()
    Radiobutton(root, text="Image",bg='light green',fg='red', variable=q, value=1, indicatoron=0).pack()
   

    label2 = Label(root, text="Enter the Source Path:", bg='red', fg='white', font=("Times", 18)).pack()
    l = StringVar()
    si_path = Entry(root, width=80, justify="center", textvariable=l,bg='grey',fg='white').pack()

    label3 = Label(root, text="Enter the Destination folder path", bg='red', fg='white', font=("Times", 18)).pack()
    m = StringVar()
    di_path = Entry(root, width=80, justify="center", textvariable=m,bg='grey',fg='white').pack()

    label4 = Label(root, text="Enter File name of result:",bg='red', fg='white', font=("Times", 18)).pack()
    c = StringVar()
    name = Entry(root, width=80, justify="center", textvariable=c,bg='grey',fg='white').pack()

    label5 = Label(root, text="Enter the Secret Message:",bg='red', fg='white', font=("Times", 18)).pack()
    global inputtxt
    inputtxt = Text(root, height=10, width=50,bg='grey',fg='white')
    inputtxt.pack()

    inp = (inputtxt.get(1.0, "end-1c"))

    Fin_button = Button(root, text="Run", bg='Light Pink',font=("Times", 14), width=10, command=p1).place(relx=0.75, rely=0.9)
    

    root.mainloop()


def decWin():
    root2 = Toplevel(parent)
    root2.grab_set()  
    root2.geometry("800x500")
    root2['bg']='black'

    global dec_path, ds

    label6 = Label(root2, text="Enter file image path",bg='red', fg='white' ,font=(None, 18)).pack()
    ds = StringVar()
    dec_source = Entry(root2, width=80, justify="center", textvariable=ds).pack()

    label7 = Label(root2,
                   text="The decoded message will be opened in next window and is also saved in same directory as source",bg='yellow', fg='green' ,font=(None, 12)).pack()
    """ outputtxt =Text(root2,height= 10,width=50).insert(END,asciiData) """

    Fin_button2 = Button(root2, text="Run", bg='Light Pink',font=(None, 14),width=10, command=p2).place(relx=0.75, rely=0.9)



def decMessage():
    root3 = Toplevel(parent)
    root3.grab_set()
    root3.geometry("600x500")
    label8 = Label(root3, text="The message", fg='red').pack()
    label9 = Label(root3, text=Decoded_message).pack()


parent = Tk()
parent.geometry("500x700")
parent.title("IMAGE STEGANOGRAPHY")
parent['bg']='black'

enc_button = Button(parent, text="ENCODER", bg='red', fg='white' ,font=(None, 18),width=18, command=encWin).place(relx=0.5, rely=0.25, anchor=CENTER)
dec_button = Button(parent, text="DECODER", bg='red', fg='white',font=(None, 18),width=18, command=decWin).place(relx=0.5, rely=0.75, anchor=CENTER)

parent.mainloop()
