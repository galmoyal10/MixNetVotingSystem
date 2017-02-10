import random


class SecureRandom(object):
    """
    This class implements secure randomization.
    Uses the most random module we could find - os.urandom (wrapped in random module)
    """
    def __init__(self):
        self._rand = random.SystemRandom()

    def randrange(self, start, stop=None, step=1):
        """
        Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        """
        return self._rand.randrange(start, stop, step)

    def getrandbits(self, k):
        """getrandbits(k) -> x.  Generates a long int with k random bits."""
        return self._rand.getrandbits(k)

    def randint(self, a, b):
        """
        Return random integer in range [a, b], including both end points.
        """
        return self._rand.randint(a, b)