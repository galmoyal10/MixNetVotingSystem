from proto.adapters import deserialize
from proto.proto_files import concrete_crypto_pb2
from proto.adapters.structs import SwitchProof
from itertools import izip
from zkproof.fs_hueristics.fs_verifier import FsSwitchVerifier
import hashlib as hl
from group_arithmetics.elliptic_curve_group import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_public_key


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)


def format_protobuf_output(header, ciphers, proofs):
    """
    returns a matrix of SwitchProofs assembled from protobuf output file in the specified format
    :param header: the MixBatchHeader of the mixnet proofs
    :param ciphers: a matrix of ElGamalCiphertext
    :param proofs: a matrix of Mix2Proof
    :return:
    """
    if header.layers == 1:
        return [[SwitchProof(ciphers[0], ciphers[1], proofs[0][0])]]
    mixnet_output = []
    for layer in xrange(0, header.layers - 1):
        layer_proofs = []
        for proof, input in zip(proofs[layer], pairwise(ciphers[layer])):
            layer_proofs.append(SwitchProof([input[0], input[1]], [ciphers[layer + 1][proof.location.out0], ciphers[layer + 1][proof.location.out1]], proof))
        mixnet_output.append(layer_proofs)
    return mixnet_output


def get_mixnet_output(input_file):
    """
    generates a matrix of SwitchProofs from mixer.jar utility output file
    :param input_file: the output of the mixer.jar
    """
    header, ciphers, proofs = deserialize.deserialize_mixnet_output_from_file(input_file)
    return format_protobuf_output(header, ciphers, proofs)


def get_first_message_clauses(switch_proof, field_name, curve_name):
    """
    retrieves a matrix of first clause fields from protobuf message
    :param switch_proof: the proof to extract the clause from
    :param field_name: field name in clause ("gr" or "hr")
    :param curve_name: curve name...
    :return: a matrix of inputs from first message of proof
    """
    return [[decode_curve_point(getattr(switch_proof.firstMessage.clause0.clause0, field_name).data, curve_name).inverse(),
             decode_curve_point(getattr(switch_proof.firstMessage.clause0.clause1, field_name).data, curve_name).inverse()],
            [decode_curve_point(getattr(switch_proof.firstMessage.clause1.clause0, field_name).data, curve_name).inverse(),
             decode_curve_point(getattr(switch_proof.firstMessage.clause1.clause1, field_name).data, curve_name).inverse()]]


def get_w(switch_proof, curve_name):
    return get_first_message_clauses(switch_proof, "gr", curve_name)


def get_t(switch_proof, curve_name):
    return get_first_message_clauses(switch_proof, "hr", curve_name)


def decode_curve_point(compressed_point, curve_name):
    return EllipticCurvePoint.from_asn1(curve_name, compressed_point)


def parse_public_key(key_bytes):
    """
    parses public key represented by an elliptic curve point that was used in mixing from raw bytes
    :return: curve name and public key coordinates
    """
    b = bytes(key_bytes)
    key = load_der_public_key(b, default_backend())
    return key.public_numbers()


def get_public_key(key_file):
    """
    reads public key used in mixing from input file
    :param key_file: the path file to read the public key from
    :return: the public key and the curve name used
    """
    raw_public_key = deserialize.deserialize_from_file(key_file, concrete_crypto_pb2.ElGamalPublicKey)[0].subject_public_key_info
    public_key_info = parse_public_key(raw_public_key)
    public_key = EllipticCurvePoint.from_coords(public_key_info.curve.name, public_key_info.x, public_key_info.y)
    return public_key, public_key_info.curve.name


def verify(input_file, key_file):
    """
    verify a mixnet output
    :param input_file: the mixnet output file
    :param key_file: the public key file
    :return: true if verification succeeded, otherwise an exception is thrown
    """
    public_key, curve_name = get_public_key(key_file)
    _, order, generator = EllipticCurveGroup.generate(curve_name)

    mixnet_output = get_mixnet_output(input_file)
    print "***Starting Verification***\n" \
          "Mixnet Size: {} X {}".format(len(mixnet_output[0]) * 2, len(mixnet_output))
    verifier = FsSwitchVerifier(generator, order, public_key)
    for layerIndex, layer in enumerate(mixnet_output):
        for switchIndex, switch in enumerate(layer):
            print "Verifying Switch proof {} of Layer {}".format(switchIndex, layerIndex)
            W = get_w(switch.proof, curve_name)
            T = get_t(switch.proof, curve_name)

            in_g = [decode_curve_point(input.c1.data, curve_name) for input in switch.inputs]
            in_m = [decode_curve_point(input.c2.data, curve_name) for input in switch.inputs]
            out_g = [decode_curve_point(output.c1.data, curve_name) for output in switch.outputs]
            out_m = [decode_curve_point(output.c2.data, curve_name) for output in switch.outputs]

            z = [[int(switch.proof.finalMessage.clause0.clause0.xcr.data.encode("hex"), 16), int(switch.proof.finalMessage.clause0.clause1.xcr.data.encode("hex"), 16)],
                 [int(switch.proof.finalMessage.clause1.clause0.xcr.data.encode("hex"), 16), int(switch.proof.finalMessage.clause1.clause1.xcr.data.encode("hex"), 16)]]
            message = switch.proof.firstMessage.SerializeToString()
            challenge = int(hl.sha256(message).hexdigest(), 16)
            c0 = int(switch.proof.finalMessage.c0.data.encode("hex"), 16)
            c1 = (challenge - c0) % order
            if not verifier.verify(message, T, W, [c0, c1], z, in_m, in_g, out_m, out_g):
                print "Verification error!\n" \
                      "Proof location: Layer={}, Switch in Layer={}".format(layerIndex, switchIndex)
                return False
            print "Verified successfully"
            print "***"
    return True
