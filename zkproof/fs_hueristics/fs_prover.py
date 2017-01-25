from zkproof.prover import PermutationProver
import numpy as np
import mixnet.group_arithmetics.elliptic_curve_group as ecg
import random as rand
from hashlib import sha256

class FsPermutationProver:
    def __init__(self, generator, grp, y):
        self.prover = PermutationProver(generator, grp, y)

    # Create a proof
    def prove(self, inM, inG, outM, outG, b, r):
        T, W = self.prover.commit(inM, inG, outM, outG, b, r)
        challenge = self.getChallenge(T, W)
        e, z = self.prover.respond(challenge)
        return T, W, e, z

    # Create a challenge based on T, W
    def getChallenge(self, tMatrix, wMatrix):
        return sha256(str(tMatrix) + str(wMatrix)).hexdigest()

    # Generate a random number from Z_q (q is given by self.group)
    def randNum(self):
        return rand.randrange(self.group.q)
