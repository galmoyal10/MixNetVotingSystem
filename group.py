
def IMultiplicativeGroup(object):
    def __init__(self, g, q, operation):
        self._g = g
        self._q = q
        self._operation = operation

    #returns (p,q,g) such as p,q large primes p = 2q+1
    def generate(self):
        raise NotImplementedError()


class IGroupItem(object):
    def __init__(self, q, value, ):
        self._q = q
        self._value = value

    def operation(self):
        raise NotImplementedError()

    def exponent(self):
        raise NotImplementedError()

    def inverse(self):
        raise NotImplementedError()



def ZpStar(IMultiplicativeGroup):
    def __init__(self, g, q):
        super(IMultiplicativeGroup, self).__init__(g,q)

    def generate(self):
        raise NotImplementedError()

