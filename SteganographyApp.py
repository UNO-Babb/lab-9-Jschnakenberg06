#Jonas Schnakenberg Lab 9

from PIL import Image
import os

def encode(img, msg):
  pixels = img.load()
  width, height = img.size
  letterSpot = 0
  pixel = 0
  letterBinary = ""
  msgLength = len(msg)
  red, green, blue = pixels[0, 0]
  pixels[0,0] = (msgLength, green, blue)

  for i in range(msgLength * 3):
    x = i % width
    y = i // width
    red, green, blue = pixels[x, y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = numberToBinary(ord(msg[letterSpot]))
      greenBinary = greenBinary[:7] + letterBinary[0]
      blueBinary = blueBinary[:7] + letterBinary[1]
    elif pixel % 3 == 1:
      redBinary = redBinary[:7] + letterBinary[2]
      greenBinary = greenBinary[:7] + letterBinary[3]
      blueBinary = blueBinary[:7] + letterBinary[4]
    else:
      redBinary = redBinary[:7] + letterBinary[5]
      greenBinary = greenBinary[:7] + letterBinary[6]
      blueBinary = blueBinary[:7] + letterBinary[7]
      letterSpot += 1

    red = binaryToNumber(redBinary)
    green = binaryToNumber(greenBinary)
    blue = binaryToNumber(blueBinary)
    pixels[x, y] = (red, green, blue)
    pixel += 1

  img.save("secretImg.png")

def decode(img):
  msg = ""
  pixels = img.load()
  red, green, blue = pixels[0, 0]
  msgLength = red
  width, height = img.size
  pixel = 0
  letterBinary = ""

  while len(msg) < msgLength:
    x = pixel % width
    y = pixel // width
    red, green, blue = pixels[x, y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = greenBinary[7] + blueBinary[7]
    elif pixel % 3 == 1:
      letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
    else:
      letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
      msg += chr(binaryToNumber(letterBinary))

    pixel += 1

  return msg

def numberToBinary(num):
  return format(num, '08b')

def binaryToNumber(bin):
  return int(bin, 2)

def main():
  print("Steganography App")
  mode = input("Encode or decode? (e/d): ")
  path = input("Image path: ")
  if not os.path.exists(path):
    print("File not found.")
    return
  img = Image.open(path)

  if mode == 'e':
    msg = input("Message to hide: ")
    encode(img, msg)
    print("Saved as secretImg.png")
  elif mode == 'd':
    print("Message:", decode(img))
  else:
    print("Choose 'e' or 'd'.")

if __name__ == '__main__':
  main()
