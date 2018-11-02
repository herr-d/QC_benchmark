from _linkedlist import DoubleLinkedList
from _permutation_rules import BasePermutationRules
import projectq
import cmath
import pytest



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

def test_single_qubit_permutation_rules(linkedlist, eng):
    rules = BasePermutationRules(linkedlist)
    qureg = eng.allocate_qureg(3)

    H = projectq.ops.H
    Rx = projectq.ops.Rx(cmath.pi)
    
    linkedlist.push_back(H.generate_command(qureg[0]))
    linkedlist.push_back(Rx.generate_command(qureg[0]))

    assert(linkedlist.head.data.gate == H)
    assert(isinstance(linkedlist.back.data.gate, projectq.ops.Rx))

    rules.permute(linkedlist.head,linkedlist.back)

    for elem in linkedlist:
    	print(elem.data)

    assert(isinstance(linkedlist.head.data.gate, projectq.ops.Rz))
    assert(linkedlist.back.data.gate == H)
    return


def test_multiqubit_permutation_rules(linkedlist, eng):
	return