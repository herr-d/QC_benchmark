"""
Registers a decomposition for a CNOT gate into a single multi qubit rotation
which is implemented using the TimeEvolution gate and additional single qubit rotations.
"""

from projectq.cengines import DecompositionRule
from projectq.meta import Compute, get_control_count, Uncompute
from projectq.ops import X, QubitOperator, TimeEvolution
	

def _decompose_cnot_rotation(cmd):
    """ Decompose CNOT gates. """
    ctrl = cmd.control_qubits
    target = cmd.qubits
    eng = cmd.engine
    qreg = [ctrl, target]
    H = QubitOperator("Z0 X1")
    T = TimeEvolution(-cmath.pi/4, H)
    T | qreg
    Rz(cmath.pi) | ctrl
    Rx(cmath.pi) | target



def _recognize_cnot(cmd):
    return get_control_count(cmd) == 1


#: Decomposition rules
all_defined_decomposition_rules = [
    DecompositionRule(X.__class__, _decompose_cnot_rotation, _recognize_cnot)
]
