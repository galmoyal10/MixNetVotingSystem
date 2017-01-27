from zkproof.verifier import SwitchVerifier
import hashlib as hl


class FsSwitchVerifier:
    def __init__(self, generator, q, y):
        # Group used in the algorithm
        self.q = q

        # Prover's public key
        self.y = y

        # Generator of the group
        self.g = generator

        # Interactive sigma-protocol verifier
        self.verifier = SwitchVerifier(generator, q, y, FsSwitchVerifier.getChallenge)


    # Given the prover's response to the challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify(self, tMatrix, wMatrix, e, z, in_m, in_g, out_m, out_g):
        self.verifier.challenge(tMatrix, wMatrix)
        return self.verifier.verify(e, z, in_m, in_g, out_m, out_g)

    # Create a challenge based on T, W
    @staticmethod
    def getChallenge(tMatrix, wMatrix):
        return int(hl.sha256(tMatrix.tostring() + wMatrix.tostring()).hexdigest(), 16)
