def get_new_state(state, sensor1_difference, sensor2_distance):
	if state == 0:
		if sensor1_difference > -3:
			return 0
		elif sensor1_difference > -45 and sensor2_distance < 20:
			return 2
		else:
			if sensor2_distance > 20:
				return 1
			else:
				return 3
	elif state == 1:
                if sensor2_distance >20 and sensor2_distance < 50:
                        return 1
                elif sensor2_distance < 20:
                        return 3
		elif sensor1_difference > 40:
                	return 0
                else:
		#else sensor1_difference > 8:
			return 2
	elif state == 2:
		if sensor2_distance > 50 and sensor1_difference>10:
                        return 0
                elif sensor2_distance > 20:
                        return 1
                elif sensor1_difference < -10:
                        return 3
                else:
                        return 2
	elif state == 3:
		if sensor1_difference > 50:
			return 0
		elif sensor1_difference > 18:
			return 2
		elif sensor1_difference > 8:
			return 1
		else:
			return 3
	else:
		#INVALID STATE INPUT
		return -1
