import AbstractApplication as Base
from threading import Semaphore
import random
import time


class Question(object):

    def __init__(self, context, entity, question, answer, listen_timeout=5, needs_answer=True):
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
        if isinstance(self._question, list):
            return random.choice(self._question)
        return self._question

    def answer(self):
        if isinstance(self._answer, list):
            return random.choice(self._answer)
        return self._answer


class DialogFlowSampleApplication(Base.AbstractApplication):
    def __init__(self):
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
        # Set the correct language (and wait for it to be changed)
        print("[+] setting language")
        self.setLanguage('en-US')
        self.locks['lang'].acquire()
        print("[+] language set")

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('Keyfile.json')
        self.setDialogflowAgent('socially-intelligent-robotics')

        for i, question in enumerate(self.questions):
            print(f"[+] begin question {i+1}")
            time.sleep(0.5)

            # 2: The amount of attempts to get an answer...
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

                if question.entity is not None and self.state[question.entity] is None:
                    self.locks['input'].acquire(timeout=1)

                if not question.needs_answer or self.state[question.entity] is not None:
                    print("  [-] question answer accepted")
                    break

                print("  [-] question answer rejected")
                # At this point, we didnt hear things... lets retry
                self._speak('Sorry I didn\'t quite catch that')

            if not question.needs_answer or self.state[question.entity] is not None:
                data = ''
                if question.entity is not None:
                    data = self.state[question.entity]
                    print(f"  [-] answer was '{data}'")
                self._speak(question.answer().format(data))
            else:
                print("[-] this question is one of life's biggest mysteries")
                self._speak('Im a sad robot i didnt hear any answers')

        # Display a gesture (replace <gestureID> with your gestureID)
        # self.gestureLock = Semaphore(0)
        # self.doGesture('<gestureID>/behavior_1')
        # self.gestureLock.acquire()

    def _speak(self, text):
        self.sayAnimated(text)
        self.locks['speech'].acquire()

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.locks['lang'].release()
        elif event == 'TextDone':
            self.locks['speech'].release()
        # elif event == 'GestureDone':
        #     self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        print(f"[+] Got intent {intentName}: {args}")
        for q in self.questions:
            if intentName == q.context and len(args) > 0:
                if q.entity is not None:
                    self.state[q.entity] = args[0]
                self.locks['input'].release()
                break


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
