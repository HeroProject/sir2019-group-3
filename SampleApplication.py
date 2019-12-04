import AbstractApplication as Base
from threading import Semaphore
import QuestAns as QA


class SampleApplication(Base.AbstractApplication):
    def __init__(self):
        Base.AbstractApplication.__init__(self)
        self.name = None
        self.age = None
        self.scenario_choice = None

        self.entities = {"answer_name": "name",
                         "answer_age": "age",
                         "pick_scenario": "scenario_choice"}

    def main(self):
     # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()
 
        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('<keyfile>.json')
        self.setDialogflowAgent('<projectid>')
 
        # Make the robot ask the question, and wait until it is done speaking
        while QA.Questions.keys != "":
            
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
        """
        get the input of the user, get the attribute this input should
        be assigned to, set the attribute
        """
        if intentName in self.entities and len(args) > 0:
            user_input = args[0]
            attribute = self.entities["answer_name"]
            setattr(self, attribute, user_input)
            self.nameLock.release()


# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
