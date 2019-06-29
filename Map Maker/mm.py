#Official Modules
import pygame
import time 
import sys
import pickle
import os
import glob
from threading import Thread, Lock
#Extra Files
import key_input
###GLOBALS###
tile_current = None
tile_counter = 0
clock = pygame.time.Clock()
screen_width = 1000
screen_height = 750


player = pygame.sprite.Group()
NPC = pygame.sprite.Group()
items = pygame.sprite.Group()
foreground = pygame.sprite.Group()
background = pygame.sprite.Group()
EVENT = pygame.sprite.Group()
layers = [background , foreground , items , NPC , player , EVENT]
layer_counter = 0
#layer_current = layers[layer_counter]

mouse_positions = []
mouse_difference = (0,0)
mouse_adjusted_x = 0
mouse_adjusted_y = 0

test_mode = False
mode_create = "CREATE"
global_timer = pygame.time.get_ticks()

#events = {"area_1": }
event_group = pygame.sprite.Group()


###FUNCTIONS###
def constant_input():
	global test_mode

	while True:
		term_input = input()

		if term_input == "/save":
			save_level()
		elif term_input == "/load":
			load_level()
		elif term_input == "/run":
			test_mode = not test_mode
def save_level():
	all_save_data = []
	for layer in layers:
		for tile in layer:
			all_save_data.append(tile.tile_save_data)
	
	name = input("Save level as:")
	with open('C:/Users/Dal/Desktop/cyborg/levels/' + name + '.pickle', "wb") as f:
		pickle.dump(all_save_data, f)
	print("Level Saved!")
def load_level():#will eventually need to impliment loading the original image. atm just defaults 
	global layers 

	name = input("Load level:")
	with open('C:/Users/Dal/Desktop/cyborg/levels/' + name + '.pickle', "rb") as f:
		data_list = pickle.load(f)
	#reconstruct level with loaded data 
	for layer in layers:
		layer.empty()#erase any current level 
	for tile_data in data_list:
		print(tile_data)
		it = clickable_square( tile_data[0] , tile_data[1] , tile_data[2] , tile_data[3] , tile_data[4] , tile_data[5])
		#REDO THIS TO ADD SPECIFIC TILES TO SPECIFIC LAYERS 
		layers[tile_data[5]].add(it)
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
			return respons
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
def dont_stack(test_x, test_y): 
	global layers
	global layer_counter

	#go through the current tiles list and see if a tile exists in it with the same coordinates 
	for sprite in layers[layer_counter]:
		if sprite.rect.x == test_x and sprite.rect.y == test_y :
			return "FAIL"
	return "PASS"
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

	tile_current = names[tile_counter]
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
	global mode_create
	global layers

	if "left_mouse" in key_input.inputs_per_frame and mode_create == "CREATE":
		x,y = pygame.mouse.get_pos() 
		if within_bounds( x , y ) == "PASS":#check whether the mouse was clicked within the editable area 
			x_pos, y_pos = calculate_placement( x , y )#check where to place clock w. grid movement
			if dont_stack( x_pos , y_pos ) == "PASS":#make sure no other block exists at location
				#find what layer we in fam 
				it = clickable_square( tile_current , x_pos , y_pos , mouse_adjusted_x , mouse_adjusted_y , layer_counter )
				layers[layer_counter].add(it)
def tile_destroy():
	global mode_create

	if "left_mouse" in key_input.inputs_per_frame and mode_create == "DESTROY":
		x,y = pygame.mouse.get_pos() 
		if within_bounds( x , y ) == "PASS":#check whether the mouse was clicked within the editable area 
			x_pos, y_pos = calculate_placement( x , y )#check where to place clock w. grid movement
			for layer in layers:
				for tile in layer:
					if tile.rect.x == x_pos and tile.rect.y == y_pos:
						layer.remove(tile)
def event_place():
	global event_group
	global mode_create

	if "left_mouse" in key_input.inputs_per_frame and mode_create == "EVENT":
		x,y = pygame.mouse.get_pos() 
		if within_bounds( x , y ) == "PASS":#check whether the mouse was clicked within the editable area 
			x_pos, y_pos = calculate_placement( x , y )#check where to place clock w. grid movement
			#decide what tile is selected and what to apply to it 




def switch_mode():
	global mode_create

	if "m_key" in key_input.inputs_per_frame:
		if mode_create == "CREATE":
			mode_create = "DESTROY"
		elif mode_create == "DESTROY":
			mode_create = "EVENT"
		elif mode_create == "EVENT":
			mode_create = "CREATE" 
def layer_select():
	global layer_counter
	global global_timer

	dynamic_timer = pygame.time.get_ticks()
	if  dynamic_timer > global_timer + 100:
		if "up_arrow_key" in key_input.inputs_per_frame:
			layer_counter += 1
		elif "down_arrow_key" in key_input.inputs_per_frame: 
			layer_counter -= 1
		if layer_counter < 0:
			layer_counter += 1
		elif layer_counter > len(layers) - 1:
			layer_counter -= 1
		global_timer = dynamic_timer
def render_order():
	global layers 

	screen.fill((0,191,255))
	pygame.draw.rect(screen, (200,200,200), ( 0 + mouse_adjusted_x , 0 + mouse_adjusted_y, TILE_SIZE * hori_size , TILE_SIZE * vert_size ),0)#draw the editable area underneath the border
	for layer in layers:
		for tile in layer:
			tile.click_pull_movement( mouse_adjusted_x , mouse_adjusted_y ) 
	#cycle through backgrounds and draw them 
	for layer in layers:
		layer.draw(screen)
	pygame.draw.rect(screen, (0,0,0), ( 0 + mouse_adjusted_x , 0 + mouse_adjusted_y , TILE_SIZE * hori_size , TILE_SIZE * vert_size ),5)#Draw map boundary. should overlap clickable tile 
	#Render text above everything
	text_creator("Calibri", 20, "Tile Selected: %s" % (tile_current), 10, 10)
	what_layer = ["background", "foreground", "items", "NPC", "player"]#this only exists to allow the proper layer to be said.. 
	text_creator("Calibri", 20, "Layer Selected: %s" % (what_layer[layer_counter]), 10, 30)
	#if mode_create == True:
	#	mode = "Create"
	#else:
	#	mode = "Destroy"
	text_creator("Calibri", 20, "Mode Selected: %s" % (mode_create), 10, 50)


	pygame.display.flip()
	clock.tick(30)
	#print(clock.get_fps())
def text_creator(font_style, font_size, text, x, y):
	myfont = pygame.font.SysFont(font_style , font_size)
	label = myfont.render(text, 1, (0,0,0))#just going to keep the default color of black
	screen.blit(label, (x, y))
class clickable_square(pygame.sprite.Sprite):  
	def __init__(self, image, on_x, on_y, x_ori_offset, y_ori_offset, layer_counter):
		super().__init__()
		self.image_file = image
		self.image_ref = 'C:/Users/Dal/Desktop/cyborg/tiles/' + image
		self.image = pygame.image.load(self.image_ref).convert()
		self.rect = self.image.get_rect()
		self.layer = layer_counter
		#original x/y of where it was placed on screen 
		self.rect.x = on_x 
		self.rect.y = on_y
		#vars to remember original coordinates when block was placed
		self.ori_x = self.rect.x
		self.ori_y = self.rect.y
		#vars to remember original offset when block was placed
		self.ori_x_off = x_ori_offset
		self.ori_y_off = y_ori_offset
		#data to reconstruct a tile
		self.tile_save_data = ( self.image_file , self.rect.x , self.rect.y , self.ori_x_off , self.ori_y_off , self.layer )

	def click_pull_movement(self, change_in_x_off , change_in_y_off):
		self.rect.x = self.ori_x - (self.ori_x_off - change_in_x_off)
		self.rect.y = self.ori_y - (self.ori_y_off - change_in_y_off)

	def movement(self, x, y):
		self.rect.x += x
		self.rect.y += y 

	def update(self, change_in_x_off , change_in_y_off):
		pass

def centre_camera():
	global layers
	
	#find MC's Sprite, centre on it 
	for tile in layers[4]:
		if tile.image_file == "MC.png":
			xdif = tile.rect.x - 1000 / 2# - 25
			ydif = tile.rect.y - 750 / 2 #- 50
			tile.rect.x = 1000 / 2 #- 25
			tile.rect.y = 750 / 2 #- 50
			for layer in layers[0:3]:
				for tile in layer:
					tile.rect.x = tile.rect.x - xdif
					tile.rect.y = tile.rect.y - ydif
			break
def test_render():
	global layers 

	screen.fill((0,191,255))
	#cycle through backgrounds and draw them 
	for layer in layers:
		layer.draw(screen)
	
	pygame.display.flip()
	clock.tick(30)
def rough_apply():
	#apply an effect to all layers
	pass
def character_movement():
	global layers

	if "up_arrow_key" in key_input.inputs_per_frame:
		for layer in layers[0:3]:#move everything except the player 
			for tile in layer:
				tile.movement(0,5)
	if "right_arrow_key" in key_input.inputs_per_frame:
		for layer in layers[0:3]:
			for tile in layer:
				tile.movement(-5,0)
	if "down_arrow_key" in key_input.inputs_per_frame:
		for layer in layers[0:3]:#move everything except the player 
			for tile in layer:
				tile.movement(0,-5)
	if "left_arrow_key" in key_input.inputs_per_frame:
		for layer in layers[0:3]:#move everything except the player 
			for tile in layer:
				tile.movement(5,0)



#Startup questions
new_or_old = reply("New Map(1) or Load Map(2)","switch")
if new_or_old == 1:
	pass
elif new_or_old == 2:
	load_level()#broken atm because i need to setup vvv before i load a level. ez fix

#Setup map specifics
#how many blocks(40pix tiles) wide and high 
hori_size = 25
vert_size = 25
TILE_SIZE = 40

#Placing the screen here initializes it after the start up questions have been answered
screen = pygame.display.set_mode((screen_width,screen_height))

#Start up constant-input threading
process = Thread(target = constant_input)
process.daemon = True
process.start()

while True:
	#EDITOR MODE
	if test_mode == False:
		key_input.player_input()
		tile_select()#mouse down and up
		layer_select()#up/down arrow keys 
		click_pull()#right-click to move map around
		tile_place()#left-click to place selected tile
		tile_destroy()#left-click to destroy selected tile 
		switch_mode()# M key to flip modes 

		###***RENDERING***###
		render_order()

	#PLAY-TEST MODE 
	elif test_mode == True:
		key_input.player_input()
		centre_camera()
		character_movement()
		###***RENDERING***###
		test_render()
