import AbstractApplication as Base
from threading import Semaphore
import random


class SampleApplication(Base.AbstractApplication):
    # def __init__(self):
    #     Base.AbstractApplication.__init__(self)
    #     self.name = None
    #     self.age = None
    #     self.scenario_choice = None
    #
    #     self.entities = {"answer_name": "name",
    #                      "answer_age": "age",
    #                      "pick_scenario": "scenario_choice"}

    def main(self):

        #
        # print(self.Questions.keys())
        self.name = ""
        self.age = ""
        self.scenario_choice = ""
        self.answer_joke = ""
        self.confirm_scenario = ""

        self.entities = {"answer_name": "name", "answer_age": "age", "pick_scenario": "scenario_choice", "answer_joke": "answer_joke", "scenario_confirmation": "confirm scenario"}

        self.context = {1: "answer_name", 2: "answer_age", 3: "answer_joke", 4: "story_about_day", 5: "choose_scenario", 6: "pick_scenario"}

        self.robot_name = ""
        self.placating_responses = ["It's okay! Take your time", "Don't worry! Take your time.", "Don't worry, you can take your time", "No worries, take as long as you need", "Don't worry, take as long as you need", "Don't worry, you're doing great", "No worries, you're doing great", "I understand you might be feeling anxious, that's okay, take your time"]

        self.Questions = {1: ["Hi, my name is" + self.robot_name + ". What is your name?", "Hello, I'm " + self.robot_name + ". How can I call you?"], 2: ["How old are you?", "What age are you?"], 3: ["How are you doing today?", "How are things going?", "How are you feeling?"], 4: ["Would you like to hear a joke?"], 5: ["These are the situations we can practice: 1: checking out at a supermarket, 2: meeting new people, 3: ordering food at a restaurant, 4: having a job interview, 5: expressing opinions, 6: inviting others to do something together. Which number would you like to practice?"], 6: ["So scenario" + self.scenario_choice + "is that correct? Or was it another number?"]}

        self.Answers = {1: ["Oh, {self.name} + Nice name!", self.name + ". I like that!"], 2: ["I'm 24", "I'm 24 years old"], 3: ["Thanks for sharing. My day was okay so far. A customer at the grocery shop I work at was being difficult and wanted to speak to the manager, but I managed to solve the problem after all!", "Thanks for sharing. My day was okay so far. I had a presentation for a course of mine. I was really nervous, but people said it went really well! I’m relieved."], 4: ["I forgot to feed my robot dog, but then remembered it doesn’t eat", "Why did the robot get angry so often? People kept pushing its buttons", "What did the robot have for lunch? … A byte!", "A robot walks into a bar and takes a seat. The bartender says: We don’t serve robots. The robot replies: Someday, you will"], 5: ["Okay", "Alright", "Got it"], 6: ["Alright! We will practice that next session. I bet you’ll do great. See you then!", "Okay! I am looking forward to practicing that with you next time. I bet you’ll do great. See you then! ", "Sounds good! I can’t wait to practice it with you. I bet you’ll do great. See you then!", "Alright! We will practice it next session then. I bet you’ll do great. See you then! "]}

        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('Keyfile.json')
        self.setDialogflowAgent('socially-intelligent-robotics')

        # Make the robot ask the question, and wait until it is done speaking
        question_number = 1
        # self.recognise_gender()
        for index in range(len(self.Questions)):
            print("start of loop")
            self.speechLock = Semaphore(0)

            # get list of question phrases
            question_phrases = self.Questions[question_number]
            question = random.choice(question_phrases)
            self.sayAnimated(question)
            self.speechLock.acquire()

            # Listen for an answer for at most 5 seconds
            self.nameLock = Semaphore(0)
            self.setAudioContext(self.context[question_number])
            self.startListening()
            self.nameLock.acquire(timeout=10)
            self.stopListening()
            if not self.name:  # wait one more second after stopListening (if needed)
                self.nameLock.acquire(timeout=3)

            # when you expect an answer
            if question_number == 1:
                # Respond and wait for that to finish

                if not self.name:
                    self.sayAnimated('Sorry, I didn\'t catch your name.')
                    self.speechLock.acquire(timeout=8)

            if question_number == 4:
                self.speechLock.acquire(timeout=7)
                if not self.scenario_choice:
                        self.sayAnimated('Sorry, what scenario did you want to practice?')
                        self.speechLock.acquire(timeout=7)

            # say answers
            answer_options = self.Answers[question_number]
            answer = random.choice(answer_options)
            self.sayAnimated(answer)

            # # Display a gesture (replace <gestureID> with your gestureID)
            # self.gestureLock = Semaphore(0)
            # self.doGesture('<gestureID>/behavior_1')
            # self.gestureLock.acquire()

            # next question
            question_number += 1
            print("end of loop", question_number)

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
            attribute = self.entities[intentName]
            setattr(self, attribute, user_input)
            self.nameLock.release()
            print(user_input)

    def recognise_gender(self):
        self.gestureLock = Semaphore(0)
        gender_client, confidence = self.doGesture('Recognition_gestures2/NAO_choregraphe_new/recog_sex')
        print(gender_client)
        self.gestureLock.acquire()

        if gender_client == 1 or gender_client == "Male":  # not quite sure how it returns things yet
            self.robot_name = "Michael"
        else:
            self.robot_name = "Michelle"

        return self.robot_name

    # associated data is an array containing the detection score of the following five expressions: [neutral, happy, surprised, angry or sad].
    # Each score ranges from 0 and 1 and represents the probability that the person expresses the corresponding expression. As such, the sum of all five properties is equal to 1, except if the detection failed (in that case all five values are set to zero).

    def recognise_dispair(self):
        self.gestureLock = Semaphore(0)
        emotion, confidence = self.doGesture('Recognition_gestures2/NAO_choregraphe_new/recog_emo')
        self.gestureLock.acquire()

        if emotion == "Sad" or emotion == "Angry" or emotion == "Surprised":  # might have to change if it uses the detection criteria
            return random.choice(self.placating_responses)


# Run the application
sample = SampleApplication()
sample.main()
sample.stop()