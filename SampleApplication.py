import AbstractApplication as Base
from threading import Semaphore
import random
import time


class Question(object):

    def __init__(self, context, entity, question, answer, listen_timeout=5, needs_answer=True):
        """ 
        Parameters : 
            self.context (str) : context of the conversation
            self.entity (str) : entity for the intents
            self._question (str) : questions of the robot to be asked.
            self._answer (str) : answers which are responded to the patient/human
            self._listen_timeout (int) : time counter for listening by the robot.
            self.needs_answer (bool) : a boolean variable which is set to true or false depending on whether an answer is needed for a particular question
            self.gestures_dict (dict) =  a dictionary with keys listening and speaking with corresponsing gestures as values.
          
        """
        
        self.context = context
        self.entity = entity
        self._question = question
        self._answer = answer
        self.listen_timeout = listen_timeout
        self.needs_answer = needs_answer
        self.gestures_dict = {"listening": ["animations/Stand/BodyTalk/Listening/Listening_2",
                                          "animations/Stand/BodyTalk/Listening/ListeningLeft_1",
                                          "animations/Stand/BodyTalk/Listening/ListeningLeft_3",
                                          "animations/Stand/BodyTalk/Listening/ListeningRight_1",
                                          "animations/Stand/BodyTalk/Listening/ListeningRight_3"],
                              "speaking": ["animations/Stand/BodyTalk/Speaking/BodyTalk_1",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_2",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_3",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_4",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_5",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_6",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_7",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_8",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_9",
                                         "animations/Stand/BodyTalk/Speaking/BodyTalk_10"]
}

    def question(self):
        
        """
            The Question method - Returns the random question based on the context of the conversation.   
        """
        
        if isinstance(self._question, list):
            return random.choice(self._question)
        return self._question

    def answer(self):
        """
        The Answer Method - Returns a random answer based on the context of the conversation.
        
        """
        if isinstance(self._answer, list):
            return random.choice(self._answer)
        return self._answer


class DialogFlowSampleApplication(Base.AbstractApplication):
    
    def __init__(self):
        
        """
        self.state (dict): Keys are the general information or data by the patient/user, values are set according
        to the user input.
        self.questions (List) : List of questions. listen_timeout and needs_answer are other two values that is required for the robot to understand the user input corresponding to the question.
        self.locks (dict) : Sets the language, speech and input as keys to values as Semaphores(0) 
        """
        
        super().__init__()

        self.state = {
            'name': None,
            'age': None,
            'scenario_choice': '',
            'Confirmation': None,
            'confirm_scenario': '',
    
        }
        self.questions = [
            Question("answer_name", "name",
                     [
                         "Hi my name is Michelle. What is your name?",
                         "Hello, I'm Michelle. What can I call you?",
                     ],
                     "Oh, I like that! Hi {}!",
                     listen_timeout=5
                     ),
            Question("answer_age", "age",
                     ["How old are you?", "What age are you?"],
                     "I'm 24 years old.",
                     listen_timeout=5, needs_answer=False,
                     ),
            Question("story_about_day", None,
                     ["How are you doing today?", "How are things going?", "How are you feeling?"],
                     "Thanks for sharing. My day was okay so far. A customer at the grocery shop I work at was being difficult and wanted to speak to the manager, but I managed to solve the problem after all!",
                     listen_timeout=5, needs_answer=False,
                     ),
            Question("answer_joke", "Confirmation",
                     ["Would you like to hear a joke?"],
                     ["A robot walks into a bar and takes a seat. The bartender says: We don’t serve robots. The robot replies: Someday, you will.",
                      "I forgot to feed my robot dog, but then remembered it doesn’t eat",
                      "Why did the robot get angry so often? People kept pushing its buttons.",
                      "What did the robot have for lunch? A byte",
                      "What is a robot’s favourite music? Heavy metal"],
                     listen_timeout=5, needs_answer=True,
                     ),
            Question("choose_scenario", "scenario_choice",
                     ["These are the situations we can practice: 1: checking out at a supermarket, 2: meeting new people, 3: ordering food at a restaurant, 4: having a job interview. Which number would you like to practice?"],
                     ["Alright! We will practice that next session. I bet you’ll do great. See you then!", "Okay! I am looking forward to practicing that with you next time. I bet you’ll do great. See you then! ", "Sounds good! I can’t wait to practice it with you. I bet you’ll do great. See you then!", "Alright! We will practice it next session then. I bet you’ll do great. See you then! "],
                     listen_timeout=5, needs_answer=True,
                     )
        ]

        self.locks = {
            'lang': Semaphore(0),
            'speech': Semaphore(0),
            'input': Semaphore(0),
        }

    def main(self):
        
        """
         main method - The method implements the language setting.It also initializes the Keyfile(json) for the 
         Dialogflow and also the project id for the dialogflow. The method focuses on the implementation of the 
         questions and it's flow of questions and answers in a loop. The gestures implementation is 
         also appended separately for listening and speaking as well after the question is picked.
         Incase of no inputs or answers, an exception case is defined in the else case of the method
        """
        
        #implements the language setting
        print("[+] setting language")
        self.setLanguage('en-US')
        self.locks['lang'].acquire()
        print("[+] language set")

       
        #initializes the Keyfile(json) for the Dialogflow and also the project id for the dialogflow
        self.setDialogflowKey('Keyfile.json')
        self.setDialogflowAgent('socially-intelligent-robotics')

        #implementation of the questions and it's flow of questions and answers in a loop
        for i, question in enumerate(self.questions):
            print(f"[+] begin question {i+1}")
            time.sleep(0.5)
            
            #the for loop implements the choice of questions,gestures and inputs(by the user).
            for attempt in range(2):
                print(f"  [-] asking question (attempt {attempt+1})")

                gesture = random.choice(question.gestures_dict['speaking'])
                self.doGesture(gesture)
                print(f"  [-] doing gesture {gesture}")
                self._speak(question.question())
                self.setAudioContext(question.context)

                gesture = random.choice(question.gestures_dict['listening'])
                self.doGesture(gesture)
                print(f"  [-] doing gesture {gesture}")

                self.startListening()
                self.locks['input'].acquire(timeout=question.listen_timeout)
                self.stopListening()

                #checks the condition if the question entity is null or not and acquires the input by the user
                if question.entity is not None and self.state[question.entity] is None:
                    self.locks['input'].acquire(timeout=1)
                
                #checks the conditon if the answer is needed for the question or question is not null, then returns if True or breaks if False
                if not question.needs_answer or self.state[question.entity] is not None:
                    print("  [-] question answer accepted")
                    break

                print("  [-] question answer rejected")
                self._speak('Sorry I didn\'t quite catch that')
                
            #checks the conditon if the question needs an answer or question entity is not null, then returns the answer, else alternative answer is obtained in the else case.  
            if not question.needs_answer or self.state[question.entity] is not None:
                data = ''
                if question.entity is not None:
                    data = self.state[question.entity]
                    print(f"  [-] answer was '{data}'")
                self._speak(question.answer().format(data))
            else:
                print("[-] this question is one of life's biggest mysteries")
                self._speak('Im a sad robot i didnt hear any answers')


    def _speak(self, text):
        
        """
        _speak method returns implementation of the robot to speak the required information
        """
        self.sayAnimated(text)
        self.locks['speech'].acquire()

    def onRobotEvent(self, event):
        """
        onRobotEvent implements the event parameter based on the selection of the event and triggers 
        which event to be locked accordingly.
    
        """
        
        if event == 'LanguageChanged':
            self.locks['lang'].release()
        elif event == 'TextDone':
            self.locks['speech'].release()

    def onAudioIntent(self, *args, intentName):
        
        """
        get the input of the user, get the attribute this input should
        be assigned to, set the attribute
        """
        
        print(f"[+] Got intent {intentName}: {args}")
        for q in self.questions:
            if intentName == q.context and len(args) > 0:
                if q.entity is not None:
                    self.state[q.entity] = args[0]
                self.locks['input'].release()
                break




sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
