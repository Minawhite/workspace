from PIL import Image
import random

def generate_shares(image_path):
    img = Image.open(image_path).convert('1')
    width, height = img.size
    share1 = Image.new('1', (width * 2, height * 2))
    share2 = Image.new('1', (width * 2, height * 2))

    patterns = {
        0: [(0, 255), (255, 0), (255, 0), (0, 255)],
        1: [(0, 255), (255, 0), (0, 255), (255, 0)]
    }

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            r = random.randint(0, 1)
            p1 = patterns[r]
            p2 = p1 if pixel == 0 else [(255 - a, 255 - b) for a, b in p1]

            for dy in range(2):
                for dx in range(2):
                    share1.putpixel((x * 2 + dx, y * 2 + dy), p1[dy * 2 + dx][0])
                    share2.putpixel((x * 2 + dx, y * 2 + dy), p2[dy * 2 + dx][1])

    share1.save("share1.png")
    share2.save("share2.png")
    print("Shares saved as share1.png and share2.png")

def overlay_shares(share1_path, share2_path):
    s1 = Image.open(share1_path).convert("1")
    s2 = Image.open(share2_path).convert("1")
    result = Image.new("1", s1.size)

    for y in range(s1.size[1]):
        for x in range(s1.size[0]):
            pixel = s1.getpixel((x, y)) & s2.getpixel((x, y))
            result.putpixel((x, y), pixel)

    result.save("reconstructed.png")
    print("Overlay saved as reconstructed.png")

def main():
    generate_shares("repo.png")
    overlay_shares("share1.png", "share2.png")

main()