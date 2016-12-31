from abc import ABCMeta

def MultiplicativeGroup(object):
    __metaclass__ = ABCMeta
    def __init__(self, g, q):
        self._g = g
        self._q = q

    #returns (p,q,g) such as p,q large primes p = 2q+1
    def generate(self):
        raise NotImplementedError()


class MultiplicativeGroupItem(object):
    __metaclass__ = ABCMeta

    def __init__(self, q, value):
        self._q = q
        self._value = value

    # Returns the multiplication of (self * other) mod q
    def operation(self, other):
        assert type(other) is MultiplicativeGroupItem, "parameter given is not a MultiplicativeGroupItem!"
        return MultiplicativeGroupItem(self._q, (self._value * other._value) % self._q )

    # Returns the multiplication of self ^ exp = self * self * .. * self exp times.
    def exponent(self, exp):
        result = MultiplicativeGroupItem(self._q, self.value)

        for i in xrange(0,exp-1):
            result = result.operation(self._value)

        return result


    def inverse(self):
        return



def ZpStar(MultiplicativeGroup):
    def __init__(self, g, q):
        super(MultiplicativeGroup, self).__init__(g,q)

    def generate(self):
        raise NotImplementedError()

