# import please
import random

# add to self
self.robot_name = ''
self.placating_responses = ["It's okay! Take your time", "Don't worry! Take your time.", "Don't worry, you can take your time", "No worries, take as long as you need", "Don't worry, take as long as you need", "Don't worry, you're doing great", "No worries, you're doing great", "I understand you might be feeling anxious, that's okay, take your time"]

# first recognise gender & change robot name accordingly
# Gender estimation of a person in the form [gender, confidence]. Gender is either 0 for female or 1 for male and the confidence is in [0, 1].
def recognise_gender(self):
    self.gestureLock = Semaphore(0)
    gender_client, confidence = self.doGesture('recog_gender')
    self.gestureLock.acquire()

    if gender_client == 0 or gender_client == "Male": #not quite sure how it returns things yet
        self.robot_name = "Michael"
    else:
        self.robot_name = "Michelle"

    return self.robot_name

#associated data is an array containing the detection score of the following five expressions: [neutral, happy, surprised, angry or sad].
#Each score ranges from 0 and 1 and represents the probability that the person expresses the corresponding expression. As such, the sum of all five properties is equal to 1, except if the detection failed (in that case all five values are set to zero).

def recognise_dispair(self):
    self.gestureLock = Semaphore(0)
    emotion, confidence = self.doGesture('recog_emo')
    self.gestureLock.acquire()

    if emotion == "Sad" or emotion == "Angry" or emotion == "Surprised":    #might have to change if it uses the detection criteria
        return random.choice(self.placating_responses)
