from mixnet.switch import *
from mixnet.server import *
from mixnet.ElGamalSwitch import ElGamalSwitch, EGTuple
from group_arithmetics.elliptic_curve_group import EllipticCurveGroup
from mixnet.mixnet import MixNetUtils

NET_SIZE = 32

if __name__ == '__main__':
    private_key = 6
    p, q, g = EllipticCurveGroup.generate()
    initial_input = list()
    for index in xrange(1, NET_SIZE + 1):
        initial_input.append(EGTuple((g * index) + ((g * private_key) * index), g * index))

    net = MixNetUtils.get_network_stages(NET_SIZE, SwitchGenerator(ElGamalSwitch))
    s = Server(initial_input, net, g, g * private_key, q)
    bb = s.mix()
    print "done"