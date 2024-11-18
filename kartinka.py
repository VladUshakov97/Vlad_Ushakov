from PIL import Image

image = Image.open('monro.jpg')
red, green, blue = image.split()

red_cropped_one = red.crop((50, 0, red.width, red.height))
red_cropped_two = red_cropped_one.crop((25, 0, red.width - 25, red.height))

blended_red = Image.blend(red_cropped_one, red_cropped_two, 0.3)

green = green.crop((25, 0, green.width - 25, green.height))

blue_cropped_one = blue.crop((0, 0, blue.width - 50, blue.height))
blue_cropped_two = blue_cropped_one.crop((25, 0, blue.width - 25, blue.height))

blended_blue = Image.blend(blue_cropped_one, blue_cropped_two, 0.3)

new_image = Image.merge('RGB', (blended_red, green, blended_blue))

new_image.thumbnail((80, 80)) 
new_image.save('monro1.jpg')
