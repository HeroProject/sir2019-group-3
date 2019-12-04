import AbstractApplication as Base
from threading import Semaphore
import random


class SampleApplication(Base.AbstractApplication):
    def main(self):
        
        
        print(self.Questions.keys())
        self.name = None
        self.age = None
        self.scenario_choice = None

        self.entities = {"answer_name": "name",
                         "answer_age": "age",
                         "pick_scenario": "scenario_choice"}
        
        context = {1:["name"],
           2:["age"],
           3:["today"],
           4:["situations"]}

        
        self.robot_name = ''
        self.placating_responses = ["It's okay! Take your time", "Don't worry! Take your time.", "Don't worry, you can take your time", "No worries, take as long as you need", "Don't worry, take as long as you need", "Don't worry, you're doing great", "No worries, you're doing great", "I understand you might be feeling anxious, that's okay, take your time"]


        self.Questions = {1:["Hi, my name is" + self.robot_name + "what is your name?", "Hello,  I'm" + self.robot_name + "How can I call you?"],
             2:["How old are you?", "What age are you?"],
             3:["How are you doing today?","How are things going?","How are you feeling?"],
             4: "These are the situations we can practice: 1: checking out at a supermarket, 2: meeting new people, 3: ordering food at a restaurant, 4: having a job interview, 5: expressing opinions, 6: inviting others to do something together. Which number would you like to practice?"}

        self.Answers = {1:["Nice name!" , self.name + "I like that!"],
           2:["I'm 24", "I'm 24 years old"],
           3:["My day was okay so far. A customer at the grocery shop I work at was being difficult and wanted to speak to the manager, but I managed to solve the problem after all!", "My day was okay so far. I had a presentation for a course of mine. I was really nervous, but people said it went really well! I’m relieved."],
           4:["Nice! So scenario" + self.scenario_choice + "We will practice that next session", "Great! So scenario" + self.scenario_choice + "I look forward to practicing that next time", "Sounds good! So scenario" + self.scenariochoice + "I can’t wait to practice it with you", "Alright! We will practice scenario" + scenariochoice + "the next session then. I bet you’ll do great"]}
        
        
        
        
        
        
        
        
        
     # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()
 
        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('Keyfile.json')
        self.setDialogflowAgent('socially-intelligent-robotics')
 
        # Make the robot ask the question, and wait until it is done speaking
        while self.Questions.keys != "":
            
            self.speechLock = Semaphore(0)
            self.sayAnimated('Hello, what is your name?')
            self.speechLock.acquire()
 
            # Listen for an answer for at most 5 seconds
            self.name = None
            self.nameLock = Semaphore(0)
            self.setAudioContext('answer_name')
            self.startListening()
            self.nameLock.acquire(timeout=5)
            self.stopListening()
            if not self.name:  # wait one more second after stopListening (if needed)
                self.nameLock.acquire(timeout=1)
 
            # Respond and wait for that to finish
            if self.name:
                self.sayAnimated('Nice to meet you ' + self.name + '!')
            else:
                self.sayAnimated('Sorry, I didn\'t catch your name.')
            self.speechLock.acquire()
 
            # Display a gesture (replace <gestureID> with your gestureID)
            self.gestureLock = Semaphore(0)
            self.doGesture('<gestureID>/behavior_1')
            self.gestureLock.acquire()
 
    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()
 
    def onAudioIntent(self, *args, intentName):
        if intentName == 'answer_name' and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()


    def recognise_gender(self):
        self.gestureLock = Semaphore(0)
        gender_client, confidence = self.doGesture('recog_gender')
        self.gestureLock.acquire()

        if gender_client == 1 or gender_client == "Male": #not quite sure how it returns things yet
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


# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
