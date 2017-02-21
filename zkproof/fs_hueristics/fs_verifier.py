from zkproof.verifier import SwitchVerifier
import hashlib as hl


class FsSwitchVerifier:
    """
    A non-interactive implementation of a verifier for a single mix-network switch, using Fiat-Shamir hueristics.
    """
    def __init__(self, generator, q, y):
        """
        :param generator: Generator of the group
        :param q: Order of group Z_q used in the algorithm
        :param y: Prover's public key
        :param challenge_func: Function used for calculating the challenge
        """
        self.q = q
        self.y = y
        self.g = generator

        # Interactive sigma-protocol verifier
        self.verifier = SwitchVerifier(generator, q, y, FsSwitchVerifier.getChallenge)

    def verify(self, message, T, W, e, z, in_m, in_g, out_m, out_g):
        """
        Given the switch's inputs and outputs, and the ZK-proof related to it (as described in the article),
        check it's validity.
        :param message: the first-message protobuf object (used to create the challenge).
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
        self.verifier.challenge(message)
        return self.verifier.verify(T, W, e, z, in_m, in_g, out_m, out_g)

    # Create a challenge based on T, W
    @staticmethod
    def getChallenge(message):
        """
        Create a challenge, derived by the input message
        :param message:
        :return: a challenge derived from the input message.
        """
        return int(hl.sha256(message).hexdigest(), 16)
