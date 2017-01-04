from mixnet.group_arithmetics.elliptic_curve_group import *
import random as rand
class PermutationVerifier:
    def __init__(self, generator, grp, y):
        # Group used in the algorithm
        self.group = grp

        # Prover's public key
        self.y = y

        # Generator of the group
        self.g = generator
        rand.seed(17)
        return

    def generateBits(self, n):
        return rand.getrandbits(k=n)

    def resetParameters(self, inM, inG, outM, outG):
        # Switch-Gate inputs
        self.inputM = inM
        self.inputG = inG

        # Switch-Gate ouputs
        self.outputM = outM
        self.outputG = outG

        return

    # Return a challenge chosen at random, given the commitment of the prover
    def challenge(self, wMatrix, tMatrix):
        self.T = tMatrix
        self.W = wMatrix

        # Generate a challenge c from Z_q
        self.c = self.group.rand()

        return self.c

    # Given the prover's response to the challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify(self, e, z):

        # Validation check for e0 + e1 = c (mod q)
        if e[0] + e[1] != self.c:
            return 0

        # Other checks validating the correctness of T_[b,i] and W_[b,i], for some b,i
        for b in range(0, 2):
            for i in range(0, 2):
                b_xor_i = b ^ i

                # Calculate T_[b,i]
                expy = self.y.exponent(z[b, i])
                outM = self.outputM[b_xor_i]
                inM_inverse = self.inputM[i].inverse()
                outM_inMInv = outM * inM_inverse
                T_bi = expy * outM_inMInv.exp(e[b])

                # Calculate W_[b,i]
                expg = self.g.exponent(z[b, i])
                outG = self.outputG[b_xor_i]
                inG_inverse = self.inputG[i].inverse()
                outG_inGInv = outG * inG_inverse
                W_bi = expg * outG_inGInv.exp(e[b])

                if not (T_bi == self.T[b, i] and W_bi == self.W[b, i]):
                    return 0
        return 1