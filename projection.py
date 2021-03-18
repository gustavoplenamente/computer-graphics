import sys

import numpy as np
from PIL import Image


def get_inv_h(source_pixels, target_pixels):
	px = [pixel[0] for pixel in target_pixels]
	py = [pixel[1] for pixel in target_pixels]

	qx = [pixel[0] for pixel in source_pixels]
	qy = [pixel[1] for pixel in source_pixels]


	a = np.array([
				 [ px[0]  ,  py[0]  ,    1    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  -qx[0] ,    0    ,    0    ,    0    ],
				 [   0    ,    0    ,    0    ,  px[0]  ,  py[0]  ,    1    ,    0    ,    0    ,    0    ,  -qy[0] ,    0    ,    0    ,    0    ],
				 [   0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  px[0]  ,  py[0]  ,    1    ,   -1    ,    0    ,    0    ,    0    ],
				 [ px[1]  ,  py[1]  ,    1    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  -qx[1] ,    0    ,    0    ],
				 [   0    ,    0    ,    0    ,  px[1]  ,  py[1]  ,    1    ,    0    ,    0    ,    0    ,    0    ,  -qy[1] ,    0    ,    0    ],
				 [   0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  px[1]  ,  py[1]  ,    1    ,    0    ,   -1    ,    0    ,    0    ],
				 [ px[2]  ,  py[2]  ,    1    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  -qx[2] ,    0    ],
				 [   0    ,    0    ,    0    ,  px[2]  ,  py[2]  ,    1    ,    0    ,    0    ,    0    ,    0    ,    0    ,  -qy[2] ,    0    ],
				 [   0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  px[2]  ,  py[2]  ,    1    ,    0    ,    0    ,   -1    ,    0    ],
				 [ px[3]  ,  py[3]  ,    1    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  -qx[3] ],
				 [   0    ,    0    ,    0    ,  px[3]  ,  py[3]  ,    1    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  -qy[3] ],
				 [   0    ,    0    ,    0    ,    0    ,    0    ,    0    ,  px[3]  ,  py[3]  ,    1    ,    0    ,    0    ,    0    ,   -1    ],
				 [   0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    1    ]
				 ])

	b = np.array([   0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    0    ,    1    ])

	t = np.linalg.solve(a, b)

	h = np.array([
				 [  t[0]  ,  t[1]  ,  t[2]  ],
				 [  t[3]  ,  t[4]  ,  t[5]  ],
				 [  t[6]  ,  t[7]  ,  t[8]  ]
				 ])

	return h


def get_borders(pixel, target_pixels):
	x, y = pixel

	tx = [pixel[0] for pixel in target_pixels]
	ty = [pixel[1] for pixel in target_pixels]

	borders = []

	# 1st condition
	m = (ty[1] - ty[0]) / (tx[1] - tx[0])
	border = ty[0] + m * (x - tx[0])

	borders.append(border)

	# 2nd condition
	m = (tx[2] - tx[0]) / (ty[2] - ty[0])
	border = tx[0] + m * (y - ty[0])

	borders.append(border)

	# 3rd condition
	m = (ty[3] - ty[2]) / (tx[3] - tx[2])
	border = ty[2] + m * (x - tx[2])

	borders.append(border)

	# 4th condition
	m = (tx[3] - tx[1]) / (ty[3] - ty[1])
	border = tx[1] + m * (y - ty[1])

	borders.append(border)

	return borders


def should_replace(pixel, target_pixels):
	x, y = pixel

	borders = get_borders(pixel, target_pixels)

	return all([
			y >= borders[0],
			x >= borders[1],
			y <= borders[2],
			x <= borders[3]
		])


def get_texture(pixel, inv_h, image):
	vec = np.array([pixel[0], pixel[1], 1])
	mapped_pixel = np.dot(inv_h, vec)

	x, y, _ = mapped_pixel / mapped_pixel[2]

	x = round(x)
	y = round(y)

	pixels = image.load()
	return pixels[x, y]


def print_px(x, y):
	print(f"x: {x},   y: {y}")


def handle_input():
	if len(sys.argv) != 3:
		print("Usage: projection.py <texture_path> <scene_path>")
		exit()

	texture_path = sys.argv[1]
	scene_path = sys.argv[2]

	texture = Image.open(texture_path)
	scene = Image.open(scene_path)

	texture_width, texture_height = texture.size
	texture_pixels = []
	scene_pixels = []

	while True:
		print("Do you want to project the whole texture onto the scene? (y/n)")
		answer = input()

		if answer == 'y':
			texture_pixels = [
				(0, 0), 
				(texture_width-1, 0), 
				(0, texture_height-1), 
				(texture_width-1, texture_height-1)
			]

			break
		elif answer == 'n':
			print("Enter the coordinates of the texture quadrilateral vertices.")
			set_pixels(texture_pixels)

			break
		else:
			print("Answer must be 'y' or 'n'.")


	print("Enter the coordinates of the scene quadrilateral vertices.")
	set_pixels(scene_pixels)

	return texture, texture_pixels, scene, scene_pixels


def set_pixels(pixels):
	set_pixel_input(pixels, "Upper left vertex")
	set_pixel_input(pixels, "Upper right vertex")
	set_pixel_input(pixels, "Bottom left vertex")
	set_pixel_input(pixels, "Bottom right vertex")


def set_pixel_input(pixels, pixel_name):
	print(pixel_name)
	pixel = (int(input("X: ")), int(input("Y: ")))
	pixels.append(pixel)


if __name__ == '__main__':
	texture, texture_pixels, scene, target_pixels = handle_input()

	width, height = texture.size
	scene_width, scene_height = scene.size

	inv_h = get_inv_h(texture_pixels, target_pixels)

	scene_pixels = scene.load()

	for x in range(scene_width):
		for y in range(scene_height):
			pixel = (x, y)

			if should_replace(pixel, target_pixels):
				texture_color = get_texture(pixel, inv_h, texture)
				scene.putpixel(pixel, texture_color)

	scene.show()
	scene.save('images/result.jpg')
