import numpy as np
from PIL import Image
import sys
from getpass4 import getpass

username= "estudiante"
password= "1234"



def Encode(src, message, dest):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4  
    total_pixels = array.size//n

    width, height = img.size
    message += "$end$"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")
        
        
def Decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4    
         
    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$end$":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$end$" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")
        
        
def main():
    user= input("hi, please enter your username: ")
    if user != username:
        print("Try again")
    else:
        pswd= getpass("Enter your password: ")
        if pswd == password:
            print("Hello, please enter the option that you want: ")
            print("h: Encode")
            print("u: Decode")
        else:
            print("Incorrect Password")
        

    func = input()

    if func == 'h':
        print("Enter Source Image Path")
        src = input()
        print("Enter Message to Hide")
        message = input()
        print("Enter Destination Image Path")
        dest = input()
        print("Encoding...")
        Encode(src, message, dest)

    elif func == 'u':
    
        print("Enter Source Image Path")
        src = input()
        print("Decoding...")
        Decode(src)

    else:
        print("ERROR: Invalid option chosen")
        
if __name__ == '__main__':
    main()