import mixnet.group_arithmetics.elliptic_curve_group as ecg
import random as rand

class SwitchVerifier:
    def __init__(self, generator, grp, y):
        # Switch-Gate inputs

        # Group used in the algorithm
        self.group = grp

        # Prover's public key
        self.y = y

        # Generator of the group
        self.g = generator
        rand.seed(17)

    # Return a challenge chosen at random, given the commitment of the prover
    def challenge(self, wMatrix, tMatrix):
        self.T = tMatrix
        self.W = wMatrix

        # Generate a challenge c from Z_q
        self.c = self.get_challenge(self.T, self.W)

        return self.c

    # Given the prover's response to the challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify(self, e, z, in_m, in_g, out_m, out_g):
        # Validation check for e0 + e1 = c (mod q)
        if self.c != (e[0] + e[1]) % self.group.q:
            return False

        # Other checks validating the correctness of T_[b,i] and W_[b,i], for some b,i
        for b in xrange(0, 2):
            for i in xrange(0, 2):
                b_xor_i = b ^ i

                # Calculate T_[b,i]
                t_second_clause = (out_m[b_xor_i] + in_m[i].inverse()) * e[b]
                T_bi = self.y * z[b, i] + t_second_clause

                # Calculate W_[b,i]
                w_second_clause = (out_g[b_xor_i] + in_g[i].inverse()) * e[b]
                W_bi = self.g * z[b, i] + w_second_clause

                if not (T_bi == self.T[b, i] and W_bi == self.W[b, i]):
                    return False
        return True

    # Given the prover's response to the given challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify_stateless(self, e, z,in_m, in_g, out_m, out_g, c):
        self.c = c

        # Validation check for e0 + e1 = c (mod q)
        if self.c != (e[0] + e[1]) % self.group.q:
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

    # Create a challenge based on T, W
    def get_challenge(self, tMatrix, wMatrix):
        return rand.getrandbits(len(tMatrix) + len(wMatrix))
