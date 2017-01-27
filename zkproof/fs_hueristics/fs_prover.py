import numpy as np
import mixnet.group_arithmetics.elliptic_curve_group as ecg
import random as rand
from zkproof.prover import PermutationProver
import hashlib as hl

class FsPermutationProver:
    def __init__(self, generator, grp, y):
        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.group = grp

        # Generator of the group
        self.g = generator

        # Public key
        self.y = y

        # Interactive sigma-protocol prover
        self.prover = PermutationProver(generator, grp, y)

    # Create a proof
    def prove(self, inM, inG, outM, outG, b, r):
        T, W = self.prover.commit(inM, inG, outM, outG, b, r)
        challenge = self.getChallenge(T, W)
        e, z = self.prover.respond(challenge)

        return T, W, e, z

    # Create a challenge based on T, W
    def getChallenge(self, tMatrix, wMatrix):
        # TODO : Change to protobuf serialization
        return hl.sha256(tMatrix.tostring() + wMatrix.tostring())

    # Generate a random number from Z_q (q is given by self.group)
    def randNum(self):
        return rand.randrange(self.group.q)
