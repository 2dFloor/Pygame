import pygame
import sys

pygame.init()

inputs_per_frame = []

def player_input():
	global inputs_per_frame

	#flush the global var list of keys pressed that call 
	inputs_per_frame[:] = []
	#temp list to accumulate and add to glob list at end
	temp_list = []

	pressed = pygame.key.get_pressed()
	mouse_input = pygame.mouse.get_pressed()
	for event in pygame.event.get():
		#mouse up/down
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			temp_list.append("mouse_up")
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			temp_list.append("mouse_down")
		#quit game
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	if mouse_input == (1,0,0):
		temp_list.append("left_mouse")
	if mouse_input == (0,1,0):
		temp_list.append("middle_mouse")
	if mouse_input == (0,0,1):
		temp_list.append("right_mouse")
	if pressed[pygame.K_q]:
		temp_list.append("q_key")
	if pressed[pygame.K_w]:
		temp_list.append("w_key")
	if pressed[pygame.K_a]:
		temp_list.append("a_key")
	if pressed[pygame.K_s]:
		temp_list.append("s_key")
	if pressed[pygame.K_e]:
		temp_list.append("e_key")
	if pressed[pygame.K_d]:
		temp_list.append("d_key")
	if pressed[pygame.K_m]:
		temp_list.append("m_key")
	if pressed[pygame.K_l]:
		temp_list.append("l_key")
	if pressed[pygame.K_UP]:
		temp_list.append("up_arrow_key")
	if pressed[pygame.K_DOWN]:
		temp_list.append("down_arrow_key")
	if pressed[pygame.K_RIGHT]:
		temp_list.append("right_arrow_key")
	if pressed[pygame.K_LEFT]:
		temp_list.append("left_arrow_key")
	if pressed[pygame.K_SPACE]:
		temp_list.append("space_bar")

	
	#flush the temp list into the global list 
	for temp in temp_list:
		inputs_per_frame.append(temp)