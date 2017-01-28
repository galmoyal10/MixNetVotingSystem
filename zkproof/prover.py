import numpy as np
import random as rand


class SwitchProver:
    def __init__(self, generator, q, y):
        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.q = q

        # Generator of the group
        self.g = generator

        # Public key
        self.y = y

        return

    # Create a commitment
    def commit(self, in_m, in_g, out_m, out_g, b, r):

        # Randomly generated b, r0, r1
        self._r = r
        self._b = b
        self._nb = 1 - self._b

        # Generate random values from the group Z_q
        z_nb = [self.rand_num() for _ in xrange(2)]
        self.w = [self.rand_num() for _ in xrange(2)]
        self._e_nb = self.rand_num()

        T = np.zeros((2, 2), dtype=type(self.g))
        W = np.zeros((2, 2), dtype=type(self.g))

        for i in xrange(0, 2):
            # Calculate T_[b,i] = exp(y, w_i)
            T[self._b, i] = self.y * self.w[i]

            # Calculate W_[b,i] = exp(g, w_i)
            W[self._b, i] = self.g * self.w[i]

            nb_xor_i = self._nb ^ i

            # Calculate T_[nb,i]
            second_clause = (out_m[nb_xor_i] + in_m[i].inverse()) * self._e_nb
            T[self._nb, i] = (self.y * z_nb[i]) + second_clause

            # Calculate W_[nb,i]
            outG_inGInv = (out_g[nb_xor_i] + in_g[i].inverse()) * self._e_nb
            W[self._nb, i] = (self.g * z_nb[i]) + outG_inGInv

        return T, W

    # Respond to the given challenge (i.e. c)
    def respond(self, c):
        # Calculate e_0, e_1
        e = [0,0]
        e[self._b] = (c - self._e_nb) % self.q
        e[self._nb] = self._e_nb

        # Calculate z_[i,j] (for i,j in [0,1])
        z = [[0,0], [0,0]]
        for i in range(0, 2):
            for b in range(0, 2):
                z[b][i] = (self.w[i] - (e[b] * self._r[i])) % self.q

        return e, z

    def rand_num(self):
        return rand.randrange(self.q)
