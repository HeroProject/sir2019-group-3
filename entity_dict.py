"""
contains:
- the user variables
- a dictionary that links the retrieved dialogflow parameters
- a loop for retrieving the entities from the API and linking them to
the user variables in python
"""
import AbstractApplication as Base


class DialogFlowSampleApplication(Base.AbstractApplication):
    def __init__(self):
        """idk how inheritance works"""
        Base.AbstractApplication.__init__(self)
        self.name = None
        self.age = None
        self.scenario_choice = None
        self.robot_name =

        self.entities = {"answer_name": "name",
                         "answer_age": "age",
                         "pick_scenario": "scenario_choice"}

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


# below is just test shit, ignore that
    def test_dict(self):
        name = input("type your name: ")
        attribute = self.entities["answer_name"]
        setattr(self, attribute, name)
        print("hello", self.name)

if __name__ == "__main__":
    mlpe = DialogFlowSampleApplication()
    mlpe.test_dict()