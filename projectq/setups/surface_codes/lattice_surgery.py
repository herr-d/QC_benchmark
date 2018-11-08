from projectq.setups import restrictedgateset
from projectq.setups.decompositions import cnot2rotations
from projectq.ops import (BasicMathGate, ClassicalInstructionGate, CNOT, BasicRotationGate,
                          HGate, XGate, YGate, ZGate, TGate, SGate, TimeEvolution, QubitOperator)
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               TagRemover, PermutePi4Front)


# Write a function which, given a Command object, returns whether the command is supported:
def is_supported(eng, cmd):
	if(isinstance(cmd.gate, ClassicalInstructionGate)):
		return True
	elif(len(cmd.control_qubits) != 0):
		return False
	elif(isinstance(cmd.gate, BasicRotationGate)):
		return True
	elif(isinstance(cmd.gate, XGate) or isinstance(cmd.gate, YGate) or isinstance(cmd.gate, ZGate)):
		return True
	elif(isinstance(cmd.gate, TGate) or isinstance(cmd.gate, SGate) or isinstance(cmd.gate, HGate)):
		return True
	elif(isinstance(cmd.gate, TimeEvolution) or isinstance(cmd.gate, QubitOperator)):
		return True
	return False


def get_engine_list():
	# lets start from a circuit that has CNOT, Pauli, S and T
	engines = restrictedgateset.get_engine_list()

	# now CNOTs need to be replaced by multi qubit rotations which is implemented
	# using Time evolution operators
	rule_set = DecompositionRuleSet(modules=[cnot2rotations]) # this ruleset only impelments a single decompostion

	engines = engines + [AutoReplacer(rule_set),
							TagRemover(),
							InstructionFilter(is_supported),
							PermutePi4Front()]

#	engines = [AutoReplacer(rule_set),InstructionFilter(is_supported)]

	return engines


