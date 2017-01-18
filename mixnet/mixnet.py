from switch import *
from server import *


def build_network(size, switch_generator):
    """
    size must be a power of 2
    """
    if size == 2:
        network = [[switch_generator.gen((0, 0), (0, 0))]]
    else:
        switches_num = size / 2
        network = [[] for x in range(switches_num)]

        upper_sub_network = build_network(size / 2, switch_generator)
        lower_sub_network = build_network(size / 2, switch_generator)
        # normalizing indices of lower subnetwork
        for switch_row in lower_sub_network:
            for switch in switch_row:
                o0 = switch.get_output0_index()
                o1 = switch.get_output1_index()
                switch.set_output0_index((o0[0], o0[1] + switches_num / 2))
                switch.set_output1_index((o1[0], o1[1] + switches_num / 2))

        next_switch_index = 0
        befor_last_switch_index = 0
        # for every list of switches
        for switch_index in range(0, switches_num):
            next_o0 = next_switch_index
            next_o1 = next_switch_index + switches_num / 2

            # first switch
            network[switch_index].append(switch_generator.gen((switch_index % 2, next_o0), (switch_index % 2, next_o1)))

            # inner switches are defined recursively
            if switch_index < switches_num / 2:
                inner_switchers = upper_sub_network[switch_index]
                # normalizing last switch of inner switch
                inner_switchers[len(inner_switchers) - 1].set_output0_index((0, befor_last_switch_index))
                inner_switchers[len(inner_switchers) - 1].set_output1_index((0, befor_last_switch_index + 1))
                befor_last_switch_index += 2
            else:
                inner_switchers = lower_sub_network[switch_index - size / 2]
                # normalizing last switch of inner switch
                inner_switchers[len(inner_switchers) - 1].set_output0_index((1, befor_last_switch_index - size / 2))
                inner_switchers[len(inner_switchers) - 1].set_output1_index((1, (befor_last_switch_index + 1) - size / 2))
                befor_last_switch_index += 2

            network[switch_index] += inner_switchers

            # last switch is trivial
            network[switch_index].append(switch_generator.gen((0, switch_index),(1,switch_index)))
            if switch_index % 2 == 1:
                next_switch_index += 1

    return network


def get_network_stages(size, switch_generator):
    # building a network and transposing it to a more comfortable form
    return [list(stage) for stage in zip(*build_network(size, switch_generator))]


if __name__ == '__main__':
    net = get_network_stages(1024, SwitchGenerator(DummySwitch))
    s = Server(range(0,1024), net)
    bb = s.mix()
    assert sum(bb[18][0].values()) != sum(range(0,1024)) ,  sum(bb[18][0].values())

    print bb

