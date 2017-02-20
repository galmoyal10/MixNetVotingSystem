from abc import ABCMeta, abstractmethod


class MultiplicativeGroup(object):
    """
    interface for multiplicative group
    """
    __metaclass__ = ABCMeta

    @classmethod
    def generate(cls):
        """
        returns group generator and order
        :return:
        """
        raise NotImplementedError()


class MultiplicativeGroupItem(object):
    """
    interface for multiplicative group item
    """
    __metaclass__ = ABCMeta

    # interface for operators
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

