from projectq.cengines._permutation import PermutePi4Front
import projectq
from projectq.ops import X, Y, Z, S, T, Rx, Ry, Rz, FlushGate
import cmath
import pytest

class A:
	def receive(self, cmd):
		pass


def test_PermutePi4Front():
	eng = projectq.MainEngine()
	perm = PermutePi4Front()
	qubit = eng.allocate_qubit()
	perm.next_engine = A()
	perm.receive([X.generate_command(qubit)])
	perm.receive([Y.generate_command(qubit)])
	perm.receive([T.generate_command(qubit)])
	perm.receive([FlushGate().generate_command(qubit)])
	return