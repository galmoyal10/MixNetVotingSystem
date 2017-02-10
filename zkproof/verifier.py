from secure_random import SecureRandom


class SwitchVerifier:
    def __init__(self, generator, q, y, challenge_func):
        # Switch-Gate inputs

        # Group used in the algorithm
        self.q = q

        # Prover's public key
        self.y = y

        # Generator of the group
        self.g = generator

        self._challenge_func = challenge_func

    # Return a challenge chosen at random, given the commitment of the prover
    def challenge(self, t_matrix, w_matrix):
        self._T = t_matrix
        self._W = w_matrix

        # Generate a challenge c from Z_q
        self._c = self._challenge_func(self._T, self._W)

        return self._c

    # Given the prover's response to the given challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify(self, e, z, in_m, in_g, out_m, out_g):

        # Validation check for e0 + e1 = c (mod q)
        if (self._c % self.q) != ((e[0] + e[1]) % self.q):
            return False

        # Other checks validating the correctness of T_[b,i] and W_[b,i], for some b,i
        for b in xrange(0, 2):
            for i in xrange(0, 2):
                b_xor_i = b ^ i

                # Calculate T_[b,i]
                t_second_clause = (out_m[b_xor_i] + in_m[i].inverse()) * e[b]
                T_bi = (self.y * z[b][i]) + t_second_clause

                # Calculate W_[b,i]
                w_second_clause = (out_g[b_xor_i] + in_g[i].inverse()) * e[b]
                W_bi = (self.g * z[b][i]) + w_second_clause

                if not (T_bi == self._T[b, i] and W_bi == self._W[b, i]):
                    return False
        return True

    # Create a challenge based on T, W
    @staticmethod
    def generate_challenge(w_matrix, t_matrix):
        rand = SecureRandom()
        return rand.getrandbits(len(t_matrix) + len(w_matrix))
