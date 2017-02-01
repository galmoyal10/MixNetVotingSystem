from switch import Switch
from random import randint

class EGTuple:
    def __init__(self, m, g):
        self.m = m
        self.g = g


class ElGamalSwitch(Switch):
    def __init__(self,o1=(0, 0), o2=(0, 0)):
        super(ElGamalSwitch, self).__init__(o1, o2)

    def switch(self, i0, i1):
        r0 = randint(0, self._group_order)
        r1 = randint(0, self._group_order)
        b = randint(0, 1)

        i0_switch = EGTuple(i0.m + (self._pk * r0), i0.g + (self._generator * r0))
        i1_switch = EGTuple(i1.m + (self._pk * r1), i1.g + (self._generator * r1))
        # return the switched output and a bit that indicates whether the inputs were switched or not
        if b:
            return i1_switch, i0_switch, b, [r0,r1]
        else:
            return i0_switch, i1_switch, b, [r0,r1]

    def set_enc_params(self, public_key, g, q):
        self._pk = public_key
        self._generator = g
        self._group_order = q
