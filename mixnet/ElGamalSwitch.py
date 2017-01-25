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
        r0 = randint(0, self._q)
        r1 = randint(0, self._q)
        b = randint(0, 1)

        o0_switch = EGTuple(i0.m + (self._pk * r0), i0.g + (self._g * r0))
        o1_switch = EGTuple(i1.m + (self._pk * r1), i1.g + (self._g * r1))
        # return the switched output and a bit that indicates whether the inputs were switched or not
        if b:
            return o0_switch, o1_switch, b
        else:
            return o1_switch, o0_switch, b

    def set_enc_params(self, public_key, g, q):
        self._pk = public_key
        self._g = g
        self._q = q