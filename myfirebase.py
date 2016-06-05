from firebase1 import Firebase
import time 
class FirebaseClass(object):

    def __init__(self):
        self.userid = raw_input('Enter your user id')
        self.myurl = 'https://seat-occupancy.firebaseio.com/seat_'+str(self.userid)
        self.fb = Firebase(self.myurl)
        self.start = time.time()

    def add_state(self,state,intervalOrTransition):
        if (intervalOrTransition==True):
            childFb = self.fb.child('/intervals')
        else:
            childFb = self.fb.child('/transitions')
        elapsed_time = time.time() - self.start 
        childFb.push({'timestamp': elapsed_time, 'state': state})
