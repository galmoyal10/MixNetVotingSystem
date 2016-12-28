from switch import Switch
from random import randint
Z_Q = None

class EGTuple:
    def __init__(self, m, g):
        self.m = m
        self.g = g

class ElGamalSwitch(Switch):
    def __init__(self,o1=(0, 0), o2=(0, 0)):
        super(ElGamalSwitch, self).__init__(o1, o2)

    def switch(self, i0, i1):
        r0 = Z_Q.generate()
        r1 = Z_Q.generate()
        b = randint(0, 1)

        i0_switch = EGTuple(i0.m * (self._pk ^ r0), i0.g * (self._g ^ r0))
        i1_switch = EGTuple(i1.m * (self._pk ^ r1), i1.g * (self._g ^ r1))

        if b:
            return i0_switch, i1_switch
        else:
            return i1_switch, i0_switch



    def setEncParams(self, public_key, g):
        self._pk = public_key
        self._g = g