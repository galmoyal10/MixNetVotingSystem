from secure_random import SecureRandom


class SwitchVerifier:
    """
    An interactive implementation of a verifier for a single mix-network switch
    """
    def __init__(self, generator, q, y, challenge_func):
        """
        :param generator: Generator of the group
        :param q: Order of group Z_q used in the algorithm
        :param y: Prover's public key
        :param challenge_func: Function used for calculating the challenge
        """

        self.q = q
        self.y = y
        self.g = generator
        self._challenge_func = challenge_func

    def challenge(self, message):
        """
        Return a challenge chosen at random, given the commitment of the prover
        :param message: input message
        :return: challenge derived from the input message
        """
        # Generate a challenge c from Z_q
        self._c = self._challenge_func(message)

        return self._c

    def verify(self, T, W, e, z, in_m, in_g, out_m, out_g):
        """
        Given the switch's inputs and outputs, and the ZK-proof related to it (as described in the article),
        check it's validity.
        :param T: 2x2 Matrix T_{b,i}, containing the inverse value from the value described in the article.
        :param W: 2x2 Matrix W_{b,i}, containing the inverse value from the value described in the article.
        :param e: 2-sized array [e_0, e_1] containing the challenges s.t. e_0 + e_1 = c, where c is the challenge
        dictated by the sigma protocol.
        :param z: 2x2 matrix z_{b,i}, as described in the article (contains the DLog challenges)
        :param in_m: Inputs M_0, M_1 of the switch, as described in the article.
        :param in_g: Inputs G_0, G_1 of the switch, as described in the article.
        :param out_m: Outputs M^_0, M^_1 of the switch, as described in the article.
        :param out_g: Outputs G^_0, G^_1 of the switch, as described in the article.
        :return: whether the given proof is valid or not
        """
        # Validation check for e0 + e1 = c (mod q)
        if (self._c % self.q) != ((e[0] + e[1]) % self.q):
            return False

        # Other checks validating the correctness of T_[b,i] and W_[b,i], for all b,i
        for b in xrange(0, 2):
            for i in xrange(0, 2):
                b_xor_i = b ^ i

                # Calculate T_[b,i]
                t_second_clause = (out_m[b_xor_i] + in_m[i].inverse()) * e[b]
                T_bi = (self.y * z[b][i])
                T_bi_verify = T[b][i].inverse() + t_second_clause

                # Calculate W_[b,i]
                w_second_clause = (out_g[b_xor_i] + in_g[i].inverse()) * e[b]
                W_bi = (self.g * z[b][i])
                W_bi_verify = W[b][i].inverse() + w_second_clause
                if not (T_bi == T_bi_verify and W_bi == W_bi_verify):
                    return False
        return True

    @staticmethod
    def generate_challenge(w_matrix, t_matrix):
        """
        Generates a challenge according the given input matrices. (default method)
        :param w_matrix:
        :param t_matrix:
        :return: challenge derived from the input matrices.
        """
        rand = SecureRandom()
        return rand.getrandbits(len(t_matrix) + len(w_matrix))
