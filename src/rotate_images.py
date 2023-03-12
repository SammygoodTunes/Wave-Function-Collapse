
import glob
from PIL import Image


def main():

	image_files = glob.glob("*.png")
	num = int(image_files[len(image_files)-1].strip(".png"))
	for image in image_files:
		img = Image.open(image)
		for i in range(3):
			num += 1
			img = img.rotate(90)
			img.save(str(num)+".png", 'PNG')

if __name__ == '__main__':
	main()