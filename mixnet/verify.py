from proto.adapters import deserialize
from structs import SwitchProof
from itertools import izip
from zkproof.fs_hueristics.fs_verifier import FsSwitchVerifier
import hashlib as hl
from group_arithmetics.elliptic_curve_group import *

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
    verifier = FsSwitchVerifier()
    proofs[0][0]
    for layer in mixnet_output:
        for switch in layer:
            T = [[switch.proof.firstMessage.clause0.clause0.gr, switch.proof.firstMessage.clause0.clause1.gr],
                 [switch.proof.firstMessage.clause1.clause0.gr, switch.proof.firstMessage.clause1.clause1.gr]]
            W = [[switch.proof.firstMessage.clause0.clause0.hr, switch.proof.firstMessage.clause0.clause1.hr],
                 [switch.proof.firstMessage.clause1.clause0.hr, switch.proof.firstMessage.clause1.clause1.hr]]
            for i in xrange(2):
                for j in xrange(2):
                    T[i][j] = asn1_to_curvepoint(T[i][j])
                    W[i][j] = asn1_to_curvepoint(W[i][j])

            in_m = [asn1_to_curvepoint(input.c1) for input in switch.inputs]
            in_g = [asn1_to_curvepoint(input.c2) for input in switch.inputs]
            out_m = [asn1_to_curvepoint(output.c1) for output in switch.outputs]
            out_g = [asn1_to_curvepoint(output.c2) for output in switch.outputs]

            z = [[switch.proof.finalMessage.clause0.clause0.xcr, switch.proof.finalMessage.clause0.clause1.xcr],
                 [switch.proof.finalMessage.clause1.clause0.xcr, switch.proof.finalMessage.clause1.clause1.xcr]]
            c0 = switch.proof.finalMessage.c0
            c1 = hl.sha256(switch.proof.SerializeToString()) - c0
            assert verifier.verify(T, W, [c0, c1], z, in_m, in_g, out_m, out_g)
    print "Done, all proofs have been verified."

def asn1_to_curvepoint(asn_point):
    return EllipticCurvePoint.from_asn_bytestring(EllipticCurveGroup.CURVE_NAME, asn_point)

if __name__ == '__main__':
    verify(r"C:\test\mixed.enc")



