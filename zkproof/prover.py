import numpy as np
from mixnet.group_arithmetics.elliptic_curve_group import *

class PermutationProver:
    def __init__(self, generator, grp, y):
        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.group = grp

        # Generator of the group
        self.g = generator

        # Public key
        self.y = y

        return

    # Create a commitment
    def commit(self, inM, inG, outM, outG, b, r):
        # Switching-gate's inputs
        self.inM = inM
        self.inG = inG

        # Switching-gate's outputs
        self.outM = outM
        self.outG = outG

        # Randomly generated b, r0, r1
        self.r = r
        self.b = b
        self.nb = 1 - self.b

        # Generate random values from the group Z_q
        z_nb = [self.group.rand() for i in range(0, 2)]
        self.w = [self.group.rand() for i in range(0, 2)]
        self.e_nb = self.group.rand()

        T = np.zeros((2, 2))
        W = np.zeros((2, 2))

        for i in range(0, 2):
            # Calculate T_[b,i] = exp(y, w_i)
            T[self.b, i] = self.y.exponent(self.w[i])

            # Calculate W_[b,i] = exp(g, w_i)
            W[self.b, i] = self.g.exponent(self.w[i])

            nb_xor_i = self.nb ^ i
            # Calculate T_[nb,i]
            expy = self.y.exponent(z_nb[i])
            outM = self.outM[nb_xor_i]
            inM_inverse = self.inM[i].inverse()
            outM_inMInv = outM * inM_inverse
            T[self.nb, i] = expy * outM_inMInv.exp(self.e_nb)

            # Calculate W_[nb,i]
            expg = self.g.exponent(z_nb[i])
            outG = self.outG[nb_xor_i]
            inG_inverse = self.inG[i].inverse()
            outG_inGInv = outG * inG_inverse
            W[self.nb, i] = expg * outG_inGInv.exp(self.e_nb)

        return T, W

    # Respond to the given challenge (i.e. c)
    def respond(self, c):
        # Calculate e_0, e_1
        e = np.zeros(2)
        e[self.b] = c - self.e_nb
        e[self.nb] = self.e_nb

        # Calculate z_[i,j] (for i,j in [0,1])
        z = np.zeros((2, 2))
        for i in range(0, 2):
            for b in range(0, 2):
                z[b, i] = self.w[i] - e[b] * self.r[i]

        return e, z
