######
#Authors: Valerie, Sanne, Robin, Emiel,Sander, Srinivas
#Course : Socially Intelligent Robotics 
#Version : 1.0.0
#Date : December 6th 2019
#Group: SIR-Project-Group3
######


import AbstractApplication as Base
from threading import Semaphore
import random


#Sample Application Class Declaration and Implementation
class SampleApplication(Base.AbstractApplication):

    def main(self):
        
        
        
        #Declaration of User Defined Variables
        self.name = ""
        self.age = ""
        self.scenario_choice = ""
        self.answer_joke = ""
        self.confirm_scenario = ""
        self.entities = {"answer_name": "name", "answer_age": "age", "pick_answer": "scenario_choice", "answer_joke": "answer_joke", "scenario_confirmation": "confirm scenario"}
        self.context = {1: "answer_name", 2: "answer_age", 3: "answer_joke", 4: "story_about_day", 5: "choose_scenario", 6: "pick_scenario"}
        self.robot_name = "Michelle"
        self.placating_responses = ["It's okay! Take your time", "Don't worry! Take your time.", "Don't worry, you can take your time", "No worries, take as long as you need", "Don't worry, take as long as you need", "Don't worry, you're doing great", "No worries, you're doing great", "I understand you might be feeling anxious, that's okay, take your time"]
        self.Questions = {1: ["Hi, my name is " + self.robot_name + " What is your name?", "Hello, I'm " + self.robot_name + " What can I call you?"], 2: ["How old are you?", "What age are you?"], 3: ["How are you doing today?", "How are things going?", "How are you feeling?"], 4: ["Would you like to hear a joke?"], 5: ["These are the situations we can practice: 1: checking out at a supermarket, 2: meeting new people, 3: ordering food at a restaurant, 4: having a job interview. Which number would you like to practice?"]}
        self.Answers = {1: [f"Oh, I like that!"], 2: ["I'm 24 years old"], 3: ["Thanks for sharing. My day was okay so far. A customer at the grocery shop I work at was being difficult and wanted to speak to the manager, but I managed to solve the problem after all!"], 4: ["A robot walks into a bar and takes a seat. The bartender says: We don’t serve robots. The robot replies: Someday, you will"], 5: ["Alright! We will practice that next session. I bet you’ll do great. See you then!", "Okay! I am looking forward to practicing that with you next time. I bet you’ll do great. See you then! ", "Sounds good! I can’t wait to practice it with you. I bet you’ll do great. See you then!", "Alright! We will practice it next session then. I bet you’ll do great. See you then! "]}
        self.listening_time_outs = {1: 8, 2: 10, 3: 20, 4: 8, 5: 20}
        self.speak_time_outs = {1: 10, 2: 15, 3: 15, 4: 10, 5: 70}
        #End of User Defined Variables
        
        
        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()
        
        
        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('Keyfile.json')
        self.setDialogflowAgent('socially-intelligent-robotics')

        # Make the robot ask the question, and wait until it is done speaking
        question_number = 1
        
        

        for index in range(len(self.Questions)):
            print("start of loop")
            self.speechLock = Semaphore(0)

            # ask question
            self.ask_question(question_number)

            # Listen for an answer for at most 5 seconds
            self.listen_answer(question_number)

            # when you expect an answer
            if question_number == 1 and not self.name:
                    self.sayAnimated('Sorry, I didn\'t catch your name.')
                    self.speechLock.acquire(timeout=10)
                    self.listen_answer(question_number)
                    
            # say answers
            if question_number == 1:
                self.sayAnimated('Nice to meet you ' + self.name + '!')
            else:
                answer_options = self.Answers[question_number]
                answer = random.choice(answer_options)
                self.sayAnimated(answer)

            # next question
            question_number += 1
            print("end of loop", question_number)
    #End of Main Method
    
    
    
    
    
    
    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()
    #end of onRobotEvent method
    
    
    
    
    
    def onAudioIntent(self, *args, intentName):
        """
        get the input of the user, get the attribute this input should
        be assigned to, set the attribute
        """
        if intentName in self.entities and len(args) > 0:
            user_input = args[0]
            attribute = self.entities[intentName]
            setattr(self, attribute, user_input)
            self.nameLock.release()
            print(user_input)
            print("name: ", self.name)
            print("age: ", self.age)
            print("scenario ", self.scenario_choice)
    #end of onAudioIntent method


    def recognise_gender(self):
        self.gestureLock = Semaphore(0)
        gender_client = self.doGesture('nao_choregraphe_new/recog_sex')
        print(gender_client)
        self.gestureLock.acquire()

        if gender_client == 1 or gender_client == "Male":  
            self.robot_name = "Michael"
        else:
            self.robot_name = "Michelle"

        return self.robot_name
    #end of recognise_gender  method
    
    
     
    
    
    
    
    def recognise_dispair(self):
        
        # associated data is an array containing the detection score of the following five expressions: [neutral, happy, surprised, angry or sad].
        # Each score ranges from 0 and 1 and represents the probability that the person expresses the corresponding expression. As such, the sum of all five properties is equal to 1, except if the detection failed (in that case all five values are set to zero).

        
        self.gestureLock = Semaphore(0)
        emotion, confidence = self.doGesture("recog_sex/recog_sex")
        self.gestureLock.acquire()

        if emotion == "Sad" or emotion == "Angry" or emotion == "Surprised": 
            return random.choice(self.placating_responses)

    #end of recognise_dispair method
    
    
    
    def ask_question(self, question_number):
        
        # get list of question phrases
        question_phrases = self.Questions[question_number]
        question = random.choice(question_phrases)
        self.sayAnimated(question)
        
        # might need to be longer for the
        timout = self.speak_time_outs[question_number]
        self.speechLock.acquire(timeout=timout)
    #end of ask_question method
    
    
        
    def listen_answer(self, question_number):
        self.nameLock = Semaphore(0)
        self.setAudioContext(self.context[question_number])
        self.startListening()
        # timeout for listening
        time_out = self.listening_time_outs[question_number]
        self.nameLock.acquire(timeout=time_out)
        self.stopListening()

    #end of listen_answer method
    
    
    
    def gesture_only(self):
        self.doGesture("happy/Enthusiastic_4")
    #end of gesture_only method
    
    
#end of SampleApplication class

    
# Run the application
sample = SampleApplication()
sample.main()
sample.stop()









































#context = {1:["name"],
           #2:["age"],
           #3:["today"],
           #4:["situations"]}
           
           