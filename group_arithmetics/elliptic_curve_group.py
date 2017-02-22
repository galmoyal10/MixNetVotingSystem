import tinyec.ec as ec
import tinyec.registry as reg

from group import *
from copy import deepcopy
from asn1crypto.keys import ECPoint

class EcException(Exception):
    def __init__(self):
        self.message = "Invalid elliptic curve point"

    def __str__(self):
        return self.message


class EllipticCurveGroup(MultiplicativeGroup):
    CURVE_NAME = "secp256r1"

    def __init__(self, g, q):
        self._g = g
        self._q = q
        self.q = q

    @classmethod
    def generate(cls, curve_name = CURVE_NAME):
        """
        :return:(p,q,g) such as p,q large primes p = 2q+1
        """

        field = reg.get_curve(curve_name).field
        ec_order = field.n

        return (2*ec_order+1, ec_order, EllipticCurvePoint.from_coords(EllipticCurveGroup.CURVE_NAME,
                                       *field.g))


class EllipticCurvePoint(MultiplicativeGroupItem):
    """
    Concrete implementation of group element based on elliptic curve
    """
    def __init__(self, **kwargs):
        if kwargs.has_key('point') and (type(kwargs['point']) is ec.Point or type(kwargs['point']) is ec.Inf):
            self._ec_point = deepcopy(kwargs['point'])
        elif kwargs.has_key('curve_name') and kwargs.has_key('x_coord') and kwargs.has_key('y_coord'):
            self._ec_point = ec.Point(reg.get_curve(kwargs['curve_name']), kwargs['x_coord'], kwargs['y_coord'])
        if not self._ec_point.on_curve:
            raise EcException

    @classmethod
    def from_coords(cls, curve_name, x, y):
        """
        Creates an elliptic curve point from coordinates
        """
        return EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y)

    @classmethod
    def from_asn1(cls, curve_name, asn1_encoded_bytestring):
        """
        Creates an elliptic curve point from compressed form
        """

        # The point is not compressed
        if asn1_encoded_bytestring[0] == '\x04':
            asn1_ec = ECPoint.load(asn1_encoded_bytestring)
            x, y = asn1_ec.to_coords()
            return EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y)

        # The point is not compressed
        elif asn1_encoded_bytestring[0] == '\x02' or asn1_encoded_bytestring[0] == '\x03':
            print asn1_encoded_bytestring[0]
            key_bytes_len = len(asn1_encoded_bytestring)

            key_type = asn1_encoded_bytestring[0]

            if key_bytes_len != 33:
                raise ValueError("key_bytes must be exactly 33 bytes long when compressed.")

            x = int(asn1_encoded_bytestring[1:33].encode("hex"), 16)
            ys = EllipticCurvePoint._y_from_x(x, curve_name)

            # Pick the one that corresponds to key_type
            last_bit = int(key_type.encode("hex"), 16) - 0x2
            for y in ys:
                if y & 0x1 == last_bit:
                    break

            return EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y)
        # Unsupported ec type.
        else:
            raise EcException()

    @staticmethod
    def _modsqrt(a, n):
        """
        utility function for calculating modulo sqrt
        """
        if a == 0:
            return 0
        elif n == 2:
            return n
        elif n % 4 == 3:
            return pow(a, (n + 1) // 4, n)

    @staticmethod
    def _y_from_x(x, curve_name):
        """
        utility frunction for calculating y coord from x coord
        """
        curve = reg.get_curve(curve_name)
        a = (pow(x, 3, curve.field.p) + curve.a * x + curve.b) % curve.field.p
        y1 = EllipticCurvePoint._modsqrt(a, curve.field.p)
        y2 = curve.field.p - y1
        rv = []

        if EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y1).on_curve:
            rv.append(y1)
        if EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y2).on_curve:
            # Put the even parity one first.
            if y2 & 0x1 == 1:
                rv.append(y2)
            else:
                rv.insert(0, y2)
        return rv

    # multiplicative group element operators

    def _plus(self, other):
        assert type(other) is EllipticCurvePoint, "parameter given is not an Elliptic Curve Point!"
        assert self._ec_point.curve.name == other._ec_point.curve.name, "Points are not on the same curve"

        return EllipticCurvePoint(point=self._ec_point + other._ec_point)

    def _scalar_multiply(self, s):
        return EllipticCurvePoint(point=self._ec_point * s)

    def inverse(self):
        return self.__mul__(-1)

    def __mul__(self, other):
        return self._scalar_multiply(other)

    def __sub__(self, other):
        assert type(other) is EllipticCurvePoint, "parameter given is not an Elliptic Curve Point!"
        return self._plus(other.inverse())

    def __add__(self, other):
        return self._plus(other)

    def __eq__(self, other):
        if type(other) is not EllipticCurvePoint:
            return False
        return self._ec_point == other._ec_point

    def __str__(self):
        return self._ec_point.__str__()

    def __repr__(self):
        return self._ec_point.__repr__()

    def asn1_encode(self):
        return ECPoint.from_coords(self._ec_point.x, self._ec_point.y).dump()

    def on_curve(self):
        return self._ec_point.on_curve