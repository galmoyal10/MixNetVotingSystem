from abc import ABCMeta


class MultiplicativeGroup(object):
    __metaclass__ = ABCMeta

    # returns (p,q,g) such as p,q large primes p = 2q+1
    def generate(self):
        raise NotImplementedError()


class MultiplicativeGroupItem(object):
    __metaclass__ = ABCMeta

    # Returns the multiplication of (self * other) mod q
    def __add__(self, other):
        raise NotImplementedError()

    # Returns the multiplication of self ^ exp = self * self * .. * self exp times.
    def __mul__(self, other):
        raise NotImplementedError()

    def inverse(self):
        raise NotImplementedError()