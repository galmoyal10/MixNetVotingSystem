from zkproof.prover import PermutationProver


class Server(object):

    def __init__(self, initial_input, mixnet_stages):
        self._initial_input = self._generate_initial_input_config(initial_input)
        self._mixnet_stages = mixnet_stages
        # TODO: init prover
        self._prover = PermutationProver()

    def mix(self):
        outputs = []
        current_input = self._initial_input
        for stage in self._mixnet_stages:
            current_output, current_proof = self._mix_and_prove_stage(stage, current_input)
            outputs.append((current_output, current_proof))
            current_input = current_output[0]

        return outputs

    def _mix_and_prove_stage(self, stage, stage_input):
        # initializing an empty dictionary to store all inputs
        output = dict()
        proofs = list()
        for i, switch in enumerate(stage):
            i0 = stage_input[(0, i)]
            i1 = stage_input[(1, i)]
            o0, o1, b = switch.switch(i0, i1)
            proofs.append(self._prove_switch(i0, i1, o0, o1, b))
            output[switch.get_output0_index()] = o0
            output[switch.get_output1_index()] = o1

        return output, proofs

    def _generate_initial_input_config(self, initial_input):
        configured_input = dict()
        for i in range(0, len(initial_input), 2):
            configured_input[(0, i/2)] = initial_input[i]
            configured_input[(1, i/2)] = initial_input[i + 1]
        return configured_input

    def _prove_switch(self, i0, i1, o0, o1, b):
        #TODO: refactor the shit out of this!!!!
        inM = []
        inM[0] = i0.m
        inM[1] = i1.m
        inG = []
        inG[0] = i0.g
        inG[1] = i1.g

        outM = []
        outM[0] = o0.m
        outM[1] = o1.m
        outG = []
        outG[0] = o0.g
        outG[1] = o1.g

        return self._prover.commit(inM, inG, outM, outG, b)