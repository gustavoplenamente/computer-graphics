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


if __name__ == '__main__':
	image = Image.open("images/nutella.jpg")
	scene = Image.open("images/art-museum.jpg")

	width, height = image.size

	target_pixels = ((54, 161), (154, 172), (53, 310), (152, 299))
	source_pixels = ((0, 0), (width-1, 0), (0, height-1), (width-1, height-1))

	inv_h = get_inv_h(source_pixels, target_pixels)

	scene_width, scene_height = scene.size
	scene_pixels = scene.load()

	for x in range(scene_width):
		for y in range(scene_height):
			pixel = (x, y)

			if should_replace(pixel, target_pixels):
				texture = get_texture(pixel, inv_h, image)
				scene.putpixel(pixel, texture)

	scene.show()
