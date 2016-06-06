chair_height = 20
floor_height = 50 # (actually 68 )
distance_to_chair_away = 70
distance_to_occupied_away = 60
def get_new_state(state, sensor1_difference,sensor1_distance, sensor2_distance, sensor1_std_dev, startBool):
        if (startBool == True):
                if sensor2_distance < 50 and sensor2_distance>20:
                        return 1 
                elif sensor2_distance<20 and sensor1_distance<50:#60:
                        return 3
                elif sensor2_distance>50 and sensor1_distance>75:#0:
                        return 0
                else:
                        return 2
        else:
        	if state == 0:
                        if (sensor2_distance < 20 and sensor1_difference > -10):
                                return 2
        		elif sensor1_difference > -10:
        			return 0
        		elif sensor1_difference > -45 and (sensor2_distance < 20 or sensor2_distance > 50):
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
                        elif (sensor1_std_dev > 5) and sensor1_difference>40:
                                return 2
                        else:
                                return 0
        		#elif sensor1_difference > 40:
                        	#return 0
                       
        	elif state == 2:
                        if sensor1_difference < 10 and sensor1_difference > -10:
                                return 2
        		if sensor2_distance > 50 and sensor1_difference>10:
                                return 0
                        elif sensor2_distance > 20:
                                return 1
                        else:
                        #elif sensor1_difference < -10:
                                return 3
        	elif state == 3:
                        if sensor1_difference < 18 and sensor2_distance < 20:
                                return 3
                        elif sensor2_distance>20 and sensor1_difference<18:
                                return 1
                        elif sensor1_difference > 18 and sensor1_difference<50 and (sensor2_distance < 20 or sensor2_distance > 50):
        			return 2
                        else:
        			return 0
        		


        	else:
        		#INVALID STATE INPUT
        		return -1
