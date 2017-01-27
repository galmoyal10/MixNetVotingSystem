import mixnet.group_arithmetics.elliptic_curve_group as ecg
from zkproof.verifier import PermutationVerifier
import hashlib as hl

class FsPermutationVerifier:
    def __init__(self, generator, grp, y, inM, inG, outM, outG):
        # Switch-Gate inputs
        self.inputM = inM
        self.inputG = inG

        # Switch-Gate ouputs
        self.outputM = outM
        self.outputG = outG

        # Group used in the algorithm
        self.group = grp

        # Prover's public key
        self.y = y

        # Generator of the group
        self.g = generator

        # Interactive sigma-protocol verifier
        self.verifier = PermutationVerifier(generator, grp, y, inM, inG, outM, outG)


    # Given the prover's response to the challenge, verify the proof's validity
    # e - array of length 2
    # z - 2x2 matrix
    def verify(self, tMatrix, wMatrix, e, z):
        challenge = self.getChallenge(tMatrix, wMatrix)
        return self.verifier.verify_stateless(e, z, challenge)

    # Create a challenge based on T, W
    def getChallenge(self, tMatrix, wMatrix):
        return hl.sha256(tMatrix.tostring() + wMatrix.tostring())
