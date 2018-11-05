from _linkedlist import DoubleLinkedList
from _permutation_rules import BasePermutationRules
import projectq
import cmath
import pytest


_PRECISION = 10**-5



@pytest.fixture
def linkedlist():
	return DoubleLinkedList()

@pytest.fixture
def eng():
	return projectq.MainEngine()


#
# Tests for complete permutations are below
# these will check for errors in the commutation relations
#
# All possible cases need to be tested thus the many functions
#

def test_H_Rxpi(linkedlist, eng):
    rules = BasePermutationRules(linkedlist)
    qureg = eng.allocate_qureg(3)

    H = projectq.ops.H
    Rx = projectq.ops.Rx(cmath.pi)
    
    linkedlist.push_back(H.generate_command(qureg[0]))
    linkedlist.push_back(Rx.generate_command(qureg[0]))

    assert(linkedlist.head.data.gate == H)
    assert(isinstance(linkedlist.back.data.gate, projectq.ops.Rx))

    rules.permute(linkedlist.head,linkedlist.back)

    assert(isinstance(linkedlist.head.data.gate, projectq.ops.Rz))
    assert(linkedlist.back.data.gate == H)

    return


def test_H_X_different_targets(linkedlist, eng):
    rules = BasePermutationRules(linkedlist)
    qureg = eng.allocate_qureg(3)

    H = projectq.ops.H
    Rx = projectq.ops.X

    linkedlist.push_back(H.generate_command(qureg[0]))
    linkedlist.push_back(Rx.generate_command(qureg[1]))

    rules.permute(linkedlist.head,linkedlist.back)

    assert(isinstance(linkedlist.head.data.gate, projectq.ops.Rx))
    assert(linkedlist.back.data.gate == H)
    return



def test_Rzpi2_Rxpi(linkedlist, eng):
    rules = BasePermutationRules(linkedlist)
    qureg = eng.allocate_qureg(3)

    Rz = projectq.ops.Rz(cmath.pi/2)
    Rx = projectq.ops.Rx(cmath.pi)
    
    linkedlist.push_back(Rz.generate_command(qureg[0]))
    linkedlist.push_back(Rx.generate_command(qureg[0]))

    rules.permute(linkedlist.head,linkedlist.back)

    assert(isinstance(linkedlist.head.data.gate, projectq.ops.Rx))
    assert(isinstance(linkedlist.back.data.gate, projectq.ops.Rz))

    assert(abs(linkedlist.back.data.gate.angle - (2*cmath.pi - cmath.pi/2)) < _PRECISION)
    return


def test_Rxpi4_Rzpi2(linkedlist, eng):
    rules = BasePermutationRules(linkedlist)
    qureg = eng.allocate_qureg(3)

    Rx = projectq.ops.Rx(cmath.pi/2)
    Rz = projectq.ops.Rz(cmath.pi/4)
    
    linkedlist.push_back(Rx.generate_command(qureg[0]))
    linkedlist.push_back(Rz.generate_command(qureg[0]))

    rules.permute(linkedlist.head,linkedlist.back)

    print(linkedlist.head.data)
    print(linkedlist.back.data)

    assert(isinstance(linkedlist.head.data.gate, projectq.ops.Ry))
    assert(isinstance(linkedlist.back.data.gate, projectq.ops.Rx))

    assert(abs(linkedlist.head.data.gate.angle - (2*cmath.pi - cmath.pi/4)) < _PRECISION)
    return


def test_Rzpi2_Rxpi4(linkedlist, eng):
    rules = BasePermutationRules(linkedlist)
    qureg = eng.allocate_qureg(3)

    Rz = projectq.ops.Rz(cmath.pi/4)
    Rx = projectq.ops.Rx(cmath.pi/2)

    linkedlist.push_back(Rz.generate_command(qureg[0]))
    linkedlist.push_back(Rx.generate_command(qureg[0]))

    rules.permute(linkedlist.head,linkedlist.back)

    print(linkedlist.head.data)
    print(linkedlist.back.data)

    assert(isinstance(linkedlist.head.data.gate, projectq.ops.Rx))
    assert(isinstance(linkedlist.back.data.gate, projectq.ops.Ry))

    assert(abs(linkedlist.back.data.gate.angle - cmath.pi/4) < _PRECISION)
    return




def test_multiqubit_permutation_rules(linkedlist, eng):
	return