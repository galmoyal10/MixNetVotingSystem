import tinyec.ec as ec
import tinyec.registry as reg

from asn1crypto.keys import ECPoint

from group import *
from copy import deepcopy


class EllipticCurveGroup(MultiplicativeGroup):
    def __init__(self, g, q):
        self._g = g
        self._q = q
        self.q = q

    def generate(self):
        """
        :return:(p,q,g) such as p,q large primes p = 2q+1
        """
        raise NotImplementedError()


class EllipticCurvePoint(MultiplicativeGroupItem):

    def __init__(self, **kwargs):
        if kwargs.has_key('point') and (type(kwargs['point']) is ec.Point or type(kwargs['point']) is ec.Inf):
            self._ec_point = deepcopy(kwargs['point'])
        elif kwargs.has_key('curve_name') and kwargs.has_key('x_coord') and kwargs.has_key('y_coord'):
            self._ec_point = ec.Point(reg.get_curve(kwargs['curve_name']), kwargs['x_coord'], kwargs['y_coord'])
        else:
            raise NotImplementedError("Unexpected input at point initialization")

    @classmethod
    def from_coords(cls, curve_name, x, y):
        return EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y)

    @classmethod
    def from_asn_bytestring(cls, curve_name, bytestring):
        """
        Creates an elliptic curve point from asn-1 encoded bytestring
        """
        asn1_ec = ECPoint.load(bytestring)
        x,y = asn1_ec.to_coords()
        return EllipticCurvePoint(curve_name=curve_name, x_coord=x, y_coord=y)


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