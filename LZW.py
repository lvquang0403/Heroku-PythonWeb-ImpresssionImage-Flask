import numpy as np
from PIL import Image
import os
def createCompressionDict():
    dictionary = {}
    for i in range(256):
        dictionary[str(i)] = i
    dictionary[','] = 256
    return dictionary,257
def compressColor(colorList):
    compressedColor = []
    compressed_size_channel=0
    i = 0
    compressionDictionary, compressionIndex = createCompressionDict()

    for currentRow in colorList:
        currentString = str(currentRow[0])
        compressedRow = ""
        i+=1
        #compressionDictionary, compressionIndex = createCompressionDict()
        for charIndex in range(1, len(currentRow)):
            currentChar = str(currentRow[charIndex])
            if currentString+currentChar in compressionDictionary:
                currentString = currentString+currentChar
            else:
                compressedRow = compressedRow + str(compressionDictionary[currentString]) + ","
                compressionDictionary[currentString+currentChar] = compressionIndex
                compressionIndex += 1
                compressed_size_channel+=1
                currentString = currentChar
            currentChar = ""
        compressedRow = compressedRow + str(compressionDictionary[currentString])
        compressed_size_channel+=1
        compressedColor.append(compressedRow)
    print("lenght dictionary : ", len(compressionDictionary))
    return len(compressionDictionary),compressed_size_channel,compressedColor
    
def compress(img_path):
  string=""
  bgr = cv2.imread(img_path, 1)
  b, g, r = bgr[:, :, 0], bgr[:, :, 1], bgr[:, :, 2]
  compressedcColors = []
  size_dic_r,size_r,compress_r = compressColor(r)
  size_dic_g,size_g,compress_g = compressColor(g)
  size_dic_b,size_b,compress_b = compressColor(b)
  compressedcColors.append(compress_r)
  compressedcColors.append(compress_g)
  compressedcColors.append(compress_b)
  print("size Dictionary each channel : ")
  string +="size Dictionary each channel : <br>"
  print("size Dictionary red channel : ",size_dic_r)
  string= string + "size Dictionary red channel : " +str(size_dic_r)+"<br>"
  print("size Dictionary green channel : ",size_dic_g)
  string= string + "size Dictionary green channel : " +str(size_dic_g)+"<br>"
  print("size Dictionary blue channel : ",size_dic_b)
  string= string + "size Dictionary blue channel : " +str(size_dic_b)+"<br>"
  print("original size : ",len(b.ravel())*3)
  string = string + "original size : " + str(len(b.ravel())*3)+ "<br>"
  print("compressed size : ",size_r+size_g+size_b)
  string = string + "compressed size : " + str(size_r+size_g+size_b)+ "<br>"
  if not os.path.isdir("./compressed"):
    os.mkdir("./compressed")
  output_path = "./compressed" + '/Compressed_LZW.lzw'
  output = open(output_path, 'w+')

  for color in compressedcColors:
    for row in color:
      output.write(row)
      output.write("\n")
    output.write("\n")
    
  print('Done!')
  return string,"Compressed_LZW.lzw"
