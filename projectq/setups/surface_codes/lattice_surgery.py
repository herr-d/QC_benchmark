from projectq.setups import restrictedgateset
from projectq.setups.decompositions import cnot2rotations
from projectq.ops import (CNOT, BasicRotationGate, HGate, XGate, YGate,
						ZGate, TGate, SGate, TimeEvolution, QubitOperator)
from projectq.cengines import PermutePi4Front, MultiqubitMeasurementCliffordEngine


def get_engine_list():
	# lets start from a circuit that has CNOT, Pauli, S and T and time evolution
	engines = restrictedgateset.get_engine_list(one_qubit_gates=(HGate,XGate,YGate,TGate,SGate),
                    two_qubit_gates=(CNOT,),
                    other_gates=(TimeEvolution,))

	engines = engines + [PermutePi4Front(),MultiqubitMeasurementCliffordEngine()]
	return engines


