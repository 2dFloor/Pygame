import pygame
import time 
import sys
import pickle
import os
import glob
from threading import Thread, Lock

import map_maker_vars
import key_input

def active_render(unsorted_group): #decomisioned for now... 
	#this algorithem can easily be improved upon...
	map_maker_vars.render_group.empty()
	map_maker_vars.render_group = unsorted_group.copy()
	for it in unsorted_group:
		if it.rect.x >= -40 and it.rect.x <= map_maker_vars.screen_width +40 and it.rect.y >= -40 and it.rect.y <= map_maker_vars.screen_height:
			pass
		else:
			map_maker_vars.render_group.remove(it)

def constant_input():
	while True:
		term_input = input()
		print(term_input + " was typed!")

		if term_input == "/save":
			save_level()
		elif term_input == "/load":
			load_level()

def save_level():
	all_save_data = []
	for tile in map_maker_vars.background:
		all_save_data.append(tile.tile_save_data)
		print(tile.tile_save_data)
	
	name = input("Save level as:")
	with open('C:/Users/Dal/Desktop/cyborg/levels/' + name + '.pickle', "wb") as f:
		pickle.dump(all_save_data, f)
	print("Level Saved!")

def load_level():#will eventually need to impliment loading the original image. atm just defaults 
	name = input("Load level:")
	with open('C:/Users/Dal/Desktop/cyborg/levels/' + name + '.pickle', "rb") as f:
		data_list = pickle.load(f)
	#reconstruct level with loaded data 
	map_maker_vars.background.empty()#erase any current level 
	for tile_data in data_list:
		it = clickable_square( tile_data[1] , tile_data[2] , tile_data[3] , tile_data[4])
		map_maker_vars.background.add(it)
	print("Level Loaded!")

def reply(question, question_type):
	if question_type == "switch":
		while True:# switch question
			response = input(question)
			try: 
				response = int(response)
				if response in (1,2):
					return response
				else:
					print("Invalid Input")
			except ValueError:
				print("Invalid Input")

	elif question_type == "int":
		while True:# integer question
			response = input(question)
			if 0 < int(response) < 99999:
				return response
			else:
				print("Invalid Input")

	elif question_type == "str":
		while True:# string question
			response = input(question)
			return response

def within_bounds(x,y):
	if ( map_maker_vars.mouse_adjusted_x ) < x <= ((hori_size) * TILE_SIZE + map_maker_vars.mouse_adjusted_x) and ( map_maker_vars.mouse_adjusted_y ) < y <= ((vert_size) * TILE_SIZE + map_maker_vars.mouse_adjusted_y):
		return "PASS" 
	else: 
		return "FAIL"#was the click allowed and within boundaries

def calculate_placement(x_mouse, y_mouse):
	new_origin_x = map_maker_vars.mouse_adjusted_x
	new_origin_y = map_maker_vars.mouse_adjusted_y
	while new_origin_x < x_mouse:
		new_origin_x += 40
	while new_origin_y < y_mouse:
		new_origin_y += 40
	final_x = new_origin_x - 40
	final_y = new_origin_y - 40
	return final_x, final_y#finds where to put tiles, even with displacement having moved the graph

def dont_stack(test_x, test_y):#doesnt allow tiles to be stacked on one another 
	#go through the current tiles list and see if a tile exists in it with the same coordinates 
	for sprite in map_maker_vars.background:
		if sprite.rect.x == test_x and sprite.rect.y == test_y :
			return "FAIL"
	return "PASS"

def select_tile(value):
	tile_bank = []

class clickable_square(pygame.sprite.Sprite):  
	def __init__(self, on_x, on_y, x_ori_offset, y_ori_offset):
		super().__init__()

		self.image_ref = 'C:/Users/Dal/Desktop/project FIRST/v2/click_base.png'
		self.image = pygame.image.load(self.image_ref).convert()
		self.rect = self.image.get_rect()
		#original x/y of where it was placed on screen 
		self.rect.x = on_x 
		self.rect.y = on_y
		#vars to remember original coordinates when block was placed
		self.ori_x = self.rect.x
		self.ori_y = self.rect.y
		#vars to remember original offset when block was placed
		self.ori_x_off = x_ori_offset
		self.ori_y_off = y_ori_offset

		self.tile_save_data = ( self.image_ref , self.rect.x , self.rect.y , self.ori_x_off , self.ori_y_off )

	def update(self, change_in_x_off , change_in_y_off):
		self.rect.x = self.ori_x - (self.ori_x_off - change_in_x_off)
		self.rect.y = self.ori_y - (self.ori_y_off - change_in_y_off)




new_or_old = reply("New Map(1) or Load Map(2)","switch")

#Setup map specifics
#how many blocks(40pix tiles) wide and high 
hori_size = 25
vert_size = 25
TILE_SIZE = 40 #constant

#initialize screen and have it pop up
screen = pygame.display.set_mode((map_maker_vars.screen_width,map_maker_vars.screen_height))
clock = pygame.time.Clock()

if new_or_old == 1:
	#NEW - blank settings are loaded
	pass

elif new_or_old == 2:
	map_name = reply("Name of Map: ","string")
	#PREVIOUS - settings preloaded and checked for relaibility 
	#if loading then the "map specifics" vars will be altered

#Start up constant-input threading
process = Thread(target = constant_input)
process.daemon = True
process.start()

while True:
	#Get any key input
	key_input.player_input()

	#pan map according to mouse-click drag
	if "right_mouse" in key_input.player_inputs:
		map_maker_vars.mouse_positions.append(pygame.mouse.get_pos())
		if len(map_maker_vars.mouse_positions) == 2:	
			#find the difference from starting location to ending of the right mouse being held 
			x1, y1 = map_maker_vars.mouse_positions[0]
			x2, y2 = map_maker_vars.mouse_positions[1]
			x_difference = x2 - x1
			y_difference = y2 - y1
			map_maker_vars.mouse_difference = (x_difference,y_difference)
			#Unpack the differenetial x/y values so they can be assigned
			x, y = map_maker_vars.mouse_difference
			map_maker_vars.mouse_adjusted_x += x
			map_maker_vars.mouse_adjusted_y += y

			del map_maker_vars.mouse_positions[0]
	else:
		map_maker_vars.mouse_positions[:] = []
		map_maker_vars.mouse_difference = (0,0)

	#place tile on right-click
	elif "left_mouse" in key_input.player_inputs:
		x,y = pygame.mouse.get_pos() 
		if within_bounds( x , y ) == "PASS":#check whether the mouse was clicked within the editable area 
			x_pos, y_pos = calculate_placement( x , y )#check where to place clock w. grid movement
			if dont_stack( x_pos , y_pos ) == "PASS":#make sure no other block exists at location
				it = clickable_square( x_pos , y_pos , map_maker_vars.mouse_adjusted_x , map_maker_vars.mouse_adjusted_y )
				map_maker_vars.background.add(it)

	#scroll through tiles 
	elif "mouse_up" in key_input.player_input:

	elif "mouse_down"in key_input.player_input:

	###***RENDERING***###
	screen.fill((0,191,255))#background, uneditable area 
	pygame.draw.rect(screen, (200,200,200), ( 0 + map_maker_vars.mouse_adjusted_x , 0 + map_maker_vars.mouse_adjusted_y, TILE_SIZE * hori_size , TILE_SIZE * vert_size ),0)#draw the editable area underneath the border
	map_maker_vars.background.update( map_maker_vars.mouse_adjusted_x , map_maker_vars.mouse_adjusted_y ) 
	map_maker_vars.background.draw(screen)
	pygame.draw.rect(screen, (0,0,0), ( 0 + map_maker_vars.mouse_adjusted_x , 0 + map_maker_vars.mouse_adjusted_y , TILE_SIZE * hori_size , TILE_SIZE * vert_size ),5)#Draw map boundary. should overlap clickable tile 
	

	pygame.display.flip()
	clock.tick(30)
	
print("Exited loop")