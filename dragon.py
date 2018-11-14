import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections  as mc
from matplotlib.widgets import Slider, Button

dragon_order = 0
koch_order = 0
mirror = False

if mirror:
	sin_60 = np.sin(np.radians(-60))
	cos_60 = np.cos(np.radians(-60))
else:
	sin_60 = np.sin(np.radians(60))
	cos_60 = np.cos(np.radians(60))

rotate_60 = np.array([[cos_60,sin_60],[-sin_60,cos_60]])
rotate_90 = np.array([(0.0,1.0), (-1.0,0.0)])

start_line = np.array([[[0.0,0.0],[1.0,0.0]]])


def koch(line, order):
	if order == 0:
		return line

	res = np.zeros((4,2,2))
	unit = (line[0][1] - line[0][0]) / 3
	point1 = line[0][0]
	point2 = line[0][0] + unit
	point3 = point2 + np.dot(unit, rotate_60)
	point4 = line[0][0] + 2 * unit
	point5 = line[0][1]
	
	res0 = koch(np.array([[point4,point5]]), order-1)
	res1 = koch(np.array([[point2,point3]]), order-1)
	res2 = koch(np.array([[point3,point4]]), order-1)
	res3 = koch(np.array([[point1,point2]]), order-1)
	return np.concatenate((res0, res1, res2, res3))


def mirror_koch(lines, dragon_iterations):
	
	if mirror and koch_order > 0:
		for d in range(2**dragon_iterations):
			base_line = lines[d*4**koch_order]
			for k in range(d*4**koch_order + 1, (d+1)*4**koch_order):
				line = lines[k]
				if base_line[0,0] == base_line[1,0]: # a.x equals b.x so its a vertical line
					line[0,0] = 2 * base_line[0,0] - line[0,0]
					line[1,0] = 2 * base_line[1,0] - line[1,0]
				elif base_line[0,1] == base_line[1,1]: # a.y equals b.y so its a horizontal line
					line[0,1] = 2 * base_line[0,1] - line[0,1]
					line[1,1] = 2 * base_line[1,1] - line[1,1]
					

def dragon(lines):
	origin = [0.0,0.0]
	for i in range(dragon_order):
		rotated_lines = np.dot(lines-origin, rotate_90) + origin
		mirror_koch(rotated_lines, i)
		origin = rotated_lines[0,1]
		lines = np.vstack([lines, rotated_lines])
	return lines



fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.15)

lc = mc.LineCollection(start_line)
ax.add_collection(lc)

margin = 0.1
ax.autoscale()
ax.set_aspect('equal')
plt.axis('off')
plt.tight_layout()

def on_change(val):
	global koch_order, dragon_order
	k_order = int(np.round(koch_slider.val))
	d_order = int(np.round(dragon_slider.val))
	if k_order != koch_order or d_order != dragon_order:
		koch_order = k_order
		dragon_order = d_order
		draw()

def draw():
	global koch_order, dragon_order
	lines = dragon(koch(start_line, koch_order))
	ax.set_xlim((np.amin(lines[:,:,0])-margin, np.amax(lines[:,:,0])+margin))
	ax.set_ylim((np.amin(lines[:,:,1])-margin, np.amax(lines[:,:,1])+margin))
	
	lc = mc.LineCollection(lines)
	del ax.collections[0]
	ax.add_collection(lc)
	plt.subplots_adjust(bottom=0.15)
	fig.canvas.draw_idle()


koch_slider_axes  = fig.add_axes([0.25, 0.1, 0.65, 0.03])
koch_slider = Slider(koch_slider_axes, 'Koch', 0, 6, valinit=0, valfmt='%0.0f')
koch_slider.on_changed(on_change)

dragon_slider_axes = fig.add_axes([0.25, 0.05, 0.65, 0.03])
dragon_slider = Slider(dragon_slider_axes, 'Dragon', 0, 14, valinit=0, valfmt='%0.0f')
dragon_slider.on_changed(on_change)

draw()

plt.show()