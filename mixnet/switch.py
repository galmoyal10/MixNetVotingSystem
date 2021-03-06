import abc


class Switch:
    """
    defines an interface for a mixnet switch
    """
    __metaclass__ = abc.ABCMeta


    def __init__(self, o0=(0, 0), o1=(0, 0)):
        """
        initializes switch with output configuration
        a tuple is defined as (<first/second entry>, <switch index>)
        :param o0: configuration for output 0
        :param o1: configuration for output 1
        """
        self._output = [o0, o1]

    def get_specific_output_index(self, index):
        return self._output[index]

    # returns configuration of specific output
    def get_output0_index(self):
        return self.get_specific_output_index(0)

    def get_output1_index(self):
        return self.get_specific_output_index(1)

    def set_specific_output_index(self, index, output_tuple):
        self._output[index] = output_tuple

    #sets configuration of specific ouptut
    def set_output0_index(self, output_tuple):
        self.set_specific_output_index(0, output_tuple)

    def set_output1_index(self, output_tuple):
        self.set_specific_output_index(1, output_tuple)

    @abc.abstractmethod
    def switch(self, i0, i1):
        raise NotImplementedError()


class DummySwitch(Switch):
    def __init__(self, o1=(0, 0), o2=(0, 0)):
        super(DummySwitch, self).__init__(o1, o2)

    def switch(self, i0, i1):
        return i1, i0, 1


class SwitchGenerator:
    def __init__(self, switch_type):
        self._switch_type = switch_type

    def gen(self, o0=(0, 0), o1=(0,0)):
        return self._switch_type(o0, o1)
