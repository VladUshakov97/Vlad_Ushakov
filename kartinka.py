from PIL import Image

image = Image.open('monro.jpg')

red, green, blue = image.split()

red = red.crop((50, 0, red.width, red.height))
green = green.crop((25, 0, green.width - 25, green.height))
blue = blue.crop((0, 0, blue.width - 50, blue.height))



new_image = Image.merge('RGB', (red, green, blue))

new_image.thumbnail((80, 80))

new_image.save('monro1.jpg')