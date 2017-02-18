class SwitchProof(object):
    """
    defines a complete proof of a mixnet switch
    """
    def __init__(self, inputs, outputs, proof):
        self.inputs = inputs
        self.outputs = outputs
        self.proof = proof