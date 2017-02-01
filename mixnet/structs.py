class SwitchProof(object):
    def __init__(self, inputs, outputs, proof):
        self.inputs = inputs
        self.outputs = outputs
        self.proof = proof


class DlogProof(object):
    class FirstMessage(object):
        def __init__(self,gr ,hr):
            self.gr = gr
            self.hr = hr
    class FinalMessage(object):
        def __init__(self, gr, hr, xcr):
            self.xcr = xcr


class Message(object):
    def __init__(self, clause0, clause1):
        self.clause0 = clause0
        self.clause1 = clause1