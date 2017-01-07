class Server(object):

    def __init__(self, initial_input, mixnet_stages):
        self._initial_input = initial_input
        self._mixnet_stages = mixnet_stages

    def mix(self):
        outputs = []
        current_input = self._initial_input
        for stage in self._mixnet_stages:
            current_output = self._mix_stage(stage, current_input)
            current_proof = None #  self._prove_stage(current_input, current_output)
            outputs.append((current_output, current_proof))
            current_input = current_output

        return outputs

    @staticmethod
    def _mix_stage(stage, stage_input):
        # initializing an empty dictionary to store all inputs
        output = dict()
        for i, switch in enumerate(stage):
            o0, o1 = switch.switch(stage_input[(0, i)], stage_input[(1, i)])
            output[switch.get_output0_index()] = o0
            output[switch.get_output1_index()] = o1

        return output

    def _prove_stage(self, stage_input, stage_output):
        raise NotImplementedError()
