import pygame
import time 
import sys
import pickle
import os
import glob
from threading import Thread, Lock

import key_input

screen_width = 1000
screen_height = 1000
clock = pygame.time.Clock()

layers = {}
layer_order = []

mouse_positions = []
mouse_difference = (0,0)
mouse_adjusted_x = 0
mouse_adjusted_y = 0

layer_key = None
current_mode = "CREATE"
#only change these for a new level, not existing
hori_size = 25
vert_size = 25
TILE_SIZE = 40

tile_current = None
tile_counter = 0


def layer_select():
	global layer_key
	layer_show()
	desired = input("What layer? ")
	layer_key = desired
def constant_input():

	while True:
		term_input = input()
		if term_input == "/save":
			pass
		elif term_input == "/load":
			pass
		elif term_input == "/layeradd":
			layer_add()
		elif term_input == "/layershow":
			layer_show()
		elif term_input == "/layerre":
			layer_rearrange()
		elif term_input == "/layerdelete":
			layer_del()
		elif term_input == "/res":
			change_res()
		elif term_input == "/layer":
			layer_select()
def within_bounds(x,y):
	if ( mouse_adjusted_x ) < x <= ((hori_size) * TILE_SIZE + mouse_adjusted_x) and ( mouse_adjusted_y ) < y <= ((vert_size) * TILE_SIZE + mouse_adjusted_y):
		return "PASS" 
	else: 
		return "FAIL"#was the click allowed and within boundarie
def calculate_placement(x_mouse, y_mouse):
	new_origin_x = mouse_adjusted_x
	new_origin_y = mouse_adjusted_y
	while new_origin_x < x_mouse:
		new_origin_x += 40
	while new_origin_y < y_mouse:
		new_origin_y += 40
	final_x = new_origin_x - 40
	final_y = new_origin_y - 40
	return final_x, final_y
def tile_select():
	global tile_current
	global tile_counter

	#get tiles in folder, real time
	names = [os.path.basename(x) for x in glob.glob('C:/Users/Dal/Desktop/cyborg/tiles/*.png')]

	#checks if any input to change tile and checks if tile value is valid 
	if "mouse_up" in key_input.inputs_per_frame:
		tile_counter += 1
	if "mouse_down" in key_input.inputs_per_frame:
		tile_counter -= 1
	if tile_counter > len(names) - 1:
		tile_counter -= 1
	elif tile_counter < 0:
		tile_counter += 1

def change_res():
	global screen_width
	global screen_height
	global screen
	x = int(input("Width: "))
	y = int(input("Height: "))
	screen_width = x
	screen_height = y
	#reinitilize screen 
	screen = pygame.display.set_mode((screen_width,screen_height)) 
def layer_del():
	global layers
	global layer_order
	target_pos = int(input("Delete what layer? "))
	target_name = layer_order[target_pos]
	del layer_order[target_pos]
	print("Removed from list.")
		
	if target_name in layers:
		del layers[target_name]
		print("Removed from dictionary.")
def layer_add():
	global layers
	global layer_order
	key = input("New Layer Name: ") 
	value = pygame.sprite.Group()
	layers[key] = value
	layer_order.append(key)
def layer_show():
	global layer_order
	counter = 0
	print("Ordered Layers:")
	for layer in layer_order:
		print("%s. %s" % (counter,layer))
		counter += 1
	print("Dictionary:")
	for i in layers:
		print(i, layers[i])
def layer_rearrange():
	global layers
	global layer_order
	print("Current Order: %s" % layer_order)
	new_list = []
	for i in layer_order:
		chosen = int(input("Type Index of Layer: "))
		new_list.append(layer_order[chosen])
	layer_order = new_list[:]
	print("New Order: %s" % layer_order)
def edit_render():
	screen.fill((0,191,255))
	pygame.draw.rect(screen, (200,200,200), ( 0 + mouse_adjusted_x , 0 + mouse_adjusted_y, TILE_SIZE * hori_size , TILE_SIZE * vert_size ),0)#draw the editable area underneath the border
	

	pygame.draw.rect(screen, (0,0,0), ( 0 + mouse_adjusted_x , 0 + mouse_adjusted_y , TILE_SIZE * hori_size , TILE_SIZE * vert_size ),5)#Draw map boundary. should overlap clickable tile 
	
	pygame.display.flip()
	clock.tick(30)
def click_pull():
	if "right_mouse" in key_input.inputs_per_frame:
		global mouse_positions
		global mouse_difference
		global mouse_adjusted_x
		global mouse_adjusted_y

		mouse_positions.append(pygame.mouse.get_pos())
		if len(mouse_positions) == 2:	
			#find the difference from starting location to ending of the right mouse being held 
			x1, y1 = mouse_positions[0]
			x2, y2 = mouse_positions[1]
			x_difference = x2 - x1
			y_difference = y2 - y1
			mouse_difference = (x_difference,y_difference)
			#Unpack the differenetial x/y values so they can be assigned
			x, y = mouse_difference
			mouse_adjusted_x += x
			mouse_adjusted_y += y

			del mouse_positions[0]
	else:
		mouse_positions[:] = []
		mouse_difference = (0,0)	
def tile_place():
	global layers

	if current_mode == "CREATE":
		tile_select()

	if "left_mouse" in key_input.inputs_per_frame and current_mode == "CREATE":
		x,y = pygame.mouse.get_pos() 
		if within_bounds( x , y ) == "PASS":#check whether the mouse was clicked within the editable area 
			x_pos, y_pos = calculate_placement( x , y )#check where to place clock w. grid movement
			if dont_stack( x_pos , y_pos ) == "PASS":#make sure no other block exists at location
				#find what layer we in fam 
				it = clickable_square( tile_current , x_pos , y_pos , mouse_adjusted_x , mouse_adjusted_y , layer_counter )
				layers[layer_counter].add(it)
def dont_stack(test_x, test_y): 
	global layers
	global layer_key

	#go through the current tiles list and see if a tile exists in it with the same coordinates 
	for sprite in layers[layer_key]:
		if sprite.rect.x == test_x and sprite.rect.y == test_y :
			return "FAIL"
	return "PASS"

#Placing the screen here initializes it after the start up questions have been answered
screen = pygame.display.set_mode((screen_width,screen_height))
#Start up constant-input threading
process = Thread(target = constant_input)
process.daemon = True
process.start()

while True:
	key_input.player_input()
	edit_render()
	click_pull()
	tile_place()