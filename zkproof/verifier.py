import mixnet.group_arithmetics.elliptic_curve_group as ecg
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
        self.c = self.randNum()

        return self.c

    # Given the prover's response to the challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify(self, e, z):

        # Validation check for e0 + e1 = c (mod q)
        if self.c != (e[0] + e[1]) % self.group.q:
            return 0

        # Other checks validating the correctness of T_[b,i] and W_[b,i], for some b,i
        for b in range(0, 2):
            for i in range(0, 2):
                b_xor_i = b ^ i

                # Calculate T_[b,i]
                expy = self.y * z[b, i]
                outM = self.outputM[b_xor_i]
                outM_inMInv = outM + self.inputM[i].inverse()
                T_bi = expy + outM_inMInv * e[b]

                # Calculate W_[b,i]
                expg = self.g * z[b, i]
                outG = self.outputG[b_xor_i]
                outG_inGInv = outG + self.inputG[i].inverse()
                W_bi = expg + outG_inGInv * e[b]

                if not (T_bi == self.T[b, i] and W_bi == self.W[b, i]):
                    return 0
        return 1


    def randNum(self):
        return ecg(rand.randrange(self.group.q))

    def randBit(self):
        return rand.choice([0, 1])
