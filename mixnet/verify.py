from proto.adapters import deserialize
from structs import SwitchProof
from itertools import izip


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)


def format_protobuf_output(header, cyphers, proofs):
    mixnet_output = []
    for layer in xrange(0, header.layers - 1):
        layer_proofs = []
        for proof, input in zip(proofs[layer], pairwise(cyphers[layer])):
            layer_proofs.append(SwitchProof([input[0], input[1]], [cyphers[layer + 1][proof.location.out0], cyphers[layer + 1][proof.location.out1]], proof))
        mixnet_output.append(layer_proofs)
    return mixnet_output

def verify(input_file):
    header, cyphers, proofs = deserialize.deserialize_mixnet_output_from_file(input_file)
    mixnet_output = format_protobuf_output(header, cyphers, proofs)
    print "hello"

if __name__ == '__main__':
    verify(r"C:\test\mixed.enc")



