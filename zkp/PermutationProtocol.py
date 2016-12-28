import numpy

class PermutationProver:
    def __init__(self, generator, grp, bit):
        # Random bit computed by the machine, provided for knowledge-proof
        self.b = bit

        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.group = grp

        # Generator of the group
        self.g = generator
        return

    # Create a commitment for some randomness r, and return g^r
    def commit(self):
        # Generate random values from the group Z_q
        self.w = [0, 0]
        self.z_nb = [0, 0]
        self.e_nb = 0

        T = numpy.zeros((2, 2))
        # Calculate T_[b,i] = exp(y, w_i)
        for i in range(0, 1):
            continue
        # Calculate T_[nb,i]
        for i in range(0, 1):
            continue

        W = numpy.zeros((2, 2))
        # Calculate W_[b,i] = exp(g, w_i)
        for i in range(0, 1):
            continue
        # Calculate W_[nb,i]
        for i in range(0, 1):
            continue

        return T, W

    # Respond to the given challenge (i.e. c)
    def respond(self, c):
        e = numpy.zeros(2)
        z = numpy.zeros((2, 2))

        # Calculate e_0, e_1

        # Calculate z_[i,j] (for i,j in [0,1])
        return e, z


class PermutationVerifier:
    def __init__(self, generator, grp, inM, inG, outM, outG):
        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.group = grp

        # Generator of the group
        self.g = generator

        # Switch-Gate inputs
        self.inputM = inM
        self.inputG = inG

        # Switch-Gate ouputs
        self.outputM = outM
        self.outputG = outG

    # Return a challenge chosen at random, given the commitment of the prover
    def challenge(self, wMatrix, tMatrix):
        self.tMatrix = tMatrix
        self.wMatrix = wMatrix

        # Generate a challenge c from Z_q
        self.c = 0

        return self.c

    # Given the prover's response to the challenge, verify the proof's validity
    def verify(self, eArray, zMatrix):
        isValid = 0

        # Validation check for c = (e0 + e1) mod q

        # Other checks validating the correctness of T_[b,i] and W_[b,i]

        return isValid