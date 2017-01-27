from abc import ABCMeta, abstractmethod


class MultiplicativeGroup(object):
    __metaclass__ = ABCMeta

    # returns (p,q,g) such as p,q large primes p = 2q+1
    @classmethod
    def generate(cls):
        raise NotImplementedError()


class MultiplicativeGroupItem(object):
    __metaclass__ = ABCMeta

    # Returns the multiplication of (self * other) mod q
    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError()

    @abstractmethod
    def __mul__(self, other):
        """
        :return: multiplication of self * exp = self + self + .. + self exp times.
        """
        raise NotImplementedError()

    @abstractmethod
    def inverse(self):
        raise NotImplementedError()

    def __rmul__(self, other):
        return self.__mul__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

