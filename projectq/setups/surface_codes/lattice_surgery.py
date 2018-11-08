from projectq.setups import restrictedgateset
from projectq.setups.decompositions import cnot2rotations

def _cnot_instruction_filter():

	return False


def get_engine_list():
	# lets start from a circuit that has CNOT, Pauli, S and T
	engines = restrictedgateset.get_engine_list()

	# now CNOTs need to be replaced by multi qubit rotations which is implemented
	# using Time evolution operators
	rule_set = DecompositionRuleSet(modules=[cnot2rotations]) # this ruleset only impelments a single decompostion

	engines = engines + [AutoReplacer(rule_set),
							TagRemover(5),
							InstructionFilter(_cnot_instruction_filter),
							PermutePi4Front()]

	return engines


