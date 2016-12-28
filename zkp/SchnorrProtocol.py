# Schnorr's Protocol - Prover Implementation
class SchnorrProver:
    def __init__(self, generator, grp, secret):
        # Secret to be used for knowledge-proof
        self.x = secret

        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.group = grp

        # Generator of the group
        self.g = generator


    # Create a commitment for some randomness r, and return g^r
    def commit(self):
        # Generate a commitment
        self.comm = 0
        return

    # Respond to the given challenge (i.e. c) - send the message r+cx
    def respond(self, c):
        return

# Schnorr's Protocol - Verifier Implementation
class SchnorrVerifier:
    def __init__(self, generator, grp, yval):
        # Group used in the algorithm (in order to perform addition, multiplication and exponentiation)
        self.group = grp

        # Generator of the group
        self.g = generator

        # The number that need we need to verify it's dlog
        self.y = yval


    # Return a challenge chosen at random, given the commitment of the prover
    def challenge(self, commitment):
        # The prover's commitment
        self.pComm = commitment

        # Generate a challenge that'll be sent to the prover
        self.c = 0
        return

    # Given the prover's response to the challenge, verify whether the following
    # equation holds or not: pow(g, s)=pComm*pow(y, c)
    def verify(self, s):
        isValid = 0

        return isValid