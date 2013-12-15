from Box2D import *
class myDestructionListener(b2DestructionListener):
    def __init__(self): super(myDestructionListener, self).__init__()
    def SayGoodbye(self,var):
        print var