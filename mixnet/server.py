from zkproof.fs_hueristics.fs_prover import FsSwitchProver
from zkproof.fs_hueristics.fs_verifier import FsSwitchVerifier


class Server(object):

    def __init__(self, initial_input, mixnet_stages, generator, public_key, q):
        self._initial_input = self._generate_initial_input_config(initial_input)
        for layer in mixnet_stages:
            for switch in layer:
                switch.set_enc_params(public_key, generator, q)
        self._mixnet_stages = mixnet_stages
        self._prover = FsSwitchProver(generator, q, public_key)
        self._verifier = FsSwitchVerifier(generator, q, public_key)

    def mix(self):
        outputs = []
        current_input = self._initial_input
        for stage in self._mixnet_stages:
            current_output, current_proof = self._mix_and_prove_stage(stage, current_input)
            outputs.append((current_output, current_proof))
            current_input = current_output

        return outputs

    def _mix_and_prove_stage(self, stage, stage_input):
        # initializing an empty dictionary to store all inputs
        output = dict()
        proofs = list()
        for i, switch in enumerate(stage):
            i0 = stage_input[(0, i)]
            i1 = stage_input[(1, i)]
            o0, o1, b, r = switch.switch(i0, i1)
            proof = self._prove_switch(i0, i1, o0, o1, b, r)
            proofs.append(proof)
            inM, inG = Server.cross_tuples(i0, i1)
            outM, outG = Server.cross_tuples(o0, o1)
            assert self._verifier.verify(proof[0], proof[1], proof[2], proof[3], inM, inG, outM, outG)

            output[switch.get_output0_index()] = o0
            output[switch.get_output1_index()] = o1

        return output, proofs

    def _generate_initial_input_config(self, initial_input):
        configured_input = dict()
        for i in range(0, len(initial_input), 2):
            configured_input[(0, i/2)] = initial_input[i]
            configured_input[(1, i/2)] = initial_input[i + 1]
        return configured_input


    def _prove_switch(self, i0, i1, o0, o1, b, r):
        #TODO: refactor the shit out of this!!!!
        inM, inG = Server.cross_tuples(i0, i1)
        outM, outG = Server.cross_tuples(o0, o1)

        return self._prover.prove(inM, inG, outM, outG, b, r)


    @staticmethod
    def cross_tuples(t1, t2):
        crossed_t1 = [0] * 2
        crossed_t1[0] = t1.m
        crossed_t1[1] = t2.m
        crossed_t2 = [0] * 2
        crossed_t2[0] = t1.g
        crossed_t2[1] = t2.g

        return crossed_t1, crossed_t2