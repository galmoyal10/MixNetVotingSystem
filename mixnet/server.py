from zkproof.fs_hueristics.fs_prover import FsSwitchProver
from zkproof.fs_hueristics.fs_verifier import FsSwitchVerifier


class Server(object):
    """
    operates the mixing and proving
    """
    def __init__(self, initial_input, mixnet_layers, generator, public_key, q):
        """
        initializes the server
        :param initial_input: initial input to mixnet
        :param mixnet_layers: the mixnet itself
        :param generator: multiplicative group generator
        :param public_key: public key used in encryption
        :param q: a big prime
        """
        self._initial_input = Server._generate_initial_input_config(initial_input)
        for layer in mixnet_layers:
            for switch in layer:
                switch.set_enc_params(public_key, generator, q)
        self._mixnet_layers = mixnet_layers
        self._prover = FsSwitchProver(generator, q, public_key)
        self._verifier = FsSwitchVerifier(generator, q, public_key)

    def mix(self):
        """
        Given the benes network, mix the initial input through all the layers
        """
        outputs = []
        current_input = self._initial_input

        # For each layer in the network, apply the mix over all the switches,
        # and provide a proof of the performed switch.
        for layer_index, layer in enumerate(self._mixnet_layers):
            current_output, current_proof = self._mix_and_prove_layer(layer_index, layer, current_input)
            outputs.append((current_output, current_proof))
            current_input = current_output

        return outputs

    def _mix_and_prove_layer(self, layer_index, layer, layer_input):
        """
        Mix all the switches in the given layer
        :param layer_index: index of layer in mixnet
        :param layer: layer switches
        :param layer_input: input to layer
        :return: outputs of layer and proofs of correctness
        """
        # initializing an empty dictionary to store all inputs
        output = dict()
        proofs = list()
        for i, switch in enumerate(layer):
            i0 = layer_input[(0, i)]
            i1 = layer_input[(1, i)]
            # Perform generate the output for the next layer
            o0, o1, b, r = switch.switch(i0, i1)

            # Prepare a proof using the output result
            proof = self._prove_switch(i0, i1, o0, o1, b, r)
            proofs.append(proof)

            # For debugging purposes, verify the calculated proof is valid
            inM, inG = Server.cross_tuples(i0, i1)
            outM, outG = Server.cross_tuples(o0, o1)
            assert self._verifier.verify(proof[0], proof[1], proof[2], proof[3], inM, inG, outM, outG)
            print "Proof ({}, {}) was successfully verified".format(layer_index, str(i))

            output[switch.get_output0_index()] = o0
            output[switch.get_output1_index()] = o1

        return output, proofs

    # Generate the initial configuration of the benes-network, given the initial inputs (i.e. initial ciphertexts)
    @staticmethod
    def _generate_initial_input_config(initial_input):
        configured_input = dict()
        for i in range(0, len(initial_input), 2):
            configured_input[(0, i/2)] = initial_input[i]
            configured_input[(1, i/2)] = initial_input[i + 1]
        return configured_input

    # Provide the proof for the given <input,output>
    def _prove_switch(self, i0, i1, o0, o1, b, r):
        inM, inG = Server.cross_tuples(i0, i1)
        outM, outG = Server.cross_tuples(o0, o1)

        return self._prover.prove(inM, inG, outM, outG, b, r)

    # Given two tuples (m1, g1), (m2, g2), return [(m1, m2), (g1, g2)]
    @staticmethod
    def cross_tuples(t1, t2):
        return [t1.m, t2.m], [t1.g, t2.g]
