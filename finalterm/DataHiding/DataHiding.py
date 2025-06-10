import cv2
import numpy as np

def embed_message(image_path, message, output_path):
    image = cv2.imread(image_path)
    message += '#####'
    binary_msg = ''.join(format(ord(i), '08b') for i in message)

    data_index = 0
    for row in image:
        for pixel in row:
            for i in range(3):
                if data_index < len(binary_msg):
                    pixel[i] = (pixel[i] & ~1) | int(binary_msg[data_index])
                    data_index += 1

    cv2.imwrite(output_path, image)
    print("Message embedded and saved as", output_path)

def extract_message(image_path):
    image = cv2.imread(image_path)
    binary_data = ""
    for row in image:
        for pixel in row:
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for c in chars:
        message += chr(int(c, 2))
        if message.endswith("#####"):
            break

    print("Extracted message:", message[:-5])

def main():
    embed_message("repo.png", "HELLO", "stego.png")
    extract_message("stego.png")

main()