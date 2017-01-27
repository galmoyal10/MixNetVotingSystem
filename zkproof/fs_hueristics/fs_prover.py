import random as rand
import hashlib as hl

from zkproof.prover import SwitchProver


class FsSwitchProver:
    def __init__(self, generator, q, y):
        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.q = q

        # Generator of the group
        self.g = generator

        # Public key
        self.y = y

        # Interactive sigma-protocol prover
        self.prover = SwitchProver(generator, q, y)

    # Create a proof
    def prove(self, in_m, in_g, out_m, out_g, b, r):
        t, w = self.prover.commit(in_m, in_g, out_m, out_g, b, r)
        challenge = self.get_challenge(t, w)
        e, z = self.prover.respond(challenge)
        return t, w, e, z

    # Create a challenge based on T, W
    def get_challenge(self, tMatrix, wMatrix):
        return int(hl.sha256(tMatrix.tostring() + wMatrix.tostring()).hexdigest(), 16)
