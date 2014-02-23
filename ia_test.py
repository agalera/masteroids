import time
import math
import random

pasive = True
hp = 100
position = [0,0]
pasive_position = [0,0]
enemy = [10,10]
def calculate_move(delta, position_info, radians, actual_speed):

	position_info[0] += actual_speed * delta * math.sin(radians)
	position_info[1] += actual_speed * delta * math.cos(radians)
	return position_info

while True:
	if (pasive == False):
		radians = (math.atan2(enemy[0]-position[0], enemy[1]-position[1]))
		position = calculate_move(20.0, position, radians, 0.020)
		print(position, math.degrees(radians))
	else:
		if (hp < 100):
			pasive = False
			print ("change to agressive mode!")
		else:
			if (pasive_position[0] == int(position[0])):
				print ("entra")
				pasive_position = [int(position[0]) + random.randint(-5, 5),int(position[1]) + random.randint(-5, 5)]
			radians = (math.atan2(pasive_position[0]-position[0], pasive_position[1]-position[1]))
			position = calculate_move(20.0, position, radians, 0.020)
			print ("position: ", position)
			print ("focus: ", pasive_position)
			hp = 99

	time.sleep(1)