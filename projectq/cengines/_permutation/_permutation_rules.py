import projectq.ops as gates
import cmath
from _linkedlist import DoubleLinkedList
from _permutation_relations import PermutationRuleDoesNotExist
from _permutation_relations import _GATE_TO_INFO, _GATE_FROM_INFO, _COMM_REL

#
# All gates get converted into an easier format using the get basis function.
# The format for all gates is the following:
# [[basis], angle_string, angle_float]
# [basis] is an array of tuples where the first element describes the spin on
# which the operator acts and the second element is the basis ("X", "Y", "Z")
#
# Since only discrete angles are allowed we choose angle_string as an identifier
# between the different commutation relations it can contain the following
# elements: pi, pi2, pi4
# These elements correspond to pi, pi/2 and pi/4 angles or in Z basis to Z-, S-
# or T-gates.
#
# The angle float also contains a sign factor (modulo 2*pi). Thus, angle_float,
# contains more information than the angle_string. All modifications are done
# inside this format and in the end new gates are generated to replace the old
# projectq gates.
#

class BasePermutationRules(object):
	"""
	Class that implements the permutation of two gates.
	It relies on a dict that contains the permutation given two gates.

	Attributes:
        self.linked_list (DoubleLinkedList): All gates of the circuit are stored
        	in this linked list. This allows fast modification and permutations.

	"""

	def __init__(self, linked_list):
		"""
        Initializer: The provided linked list contains all the gates that need
        			on which permutation operations are performed.
		"""
		self.linked_list = linked_list #This is a linked list of all gates in the 


	def permute(self, left, right):
		"""
		Performs a single permutation operation between two neighboring elements
		in the linked list.

		Args:
            left (DLLNode): left node in the linked list.
            right (DLLNode): right node in the linked list.

        Raises:
            Exception if no permutation rule is available.
		"""
		assert(len(left.data.control_qubits)<=1)
		assert(len(right.data.control_qubits)<=1)

		left_info = _GATE_TO_INFO[type(left.data.gate)](left.data.gate)
		right_info = _GATE_TO_INFO[type(right.data.gate)](right.data.gate)


		# cannot permute two pi/8 rotations
		assert((not left_info[1] == "pi4") or (not right_info[1] == "pi4"))
		
		# check for control
		if(len(left.data.control_qubits) != 0 or len(right.data.control_qubits)!=0):
			self._permute_control_gates(left.data, right.data, left_info, right_info)
			self.linked_list.swap_elements(left,right)
			return

		# perform permutation of not controlled gates
		self._permute_multiqubit(left.data, right.data, left_info, right_info)
		self.linked_list.swap_elements(left,right)
		return


	def _permute_multiqubit(self, left, right, left_info, right_info):
		"""
		Permutes two gates. The permutation relation of multi-qubit rotations
		are performed through a reduction to many single qubit commutation rules.

		Args:
            left (Command): Command for the left gate of the commutation
            right (Command): Command for the right gate of the commutation
            left_info (list): information on the left gate (from basis dictionary)
            right_info (list): information on the right gate (from basis dictionary)

        Raises:
            Exception if no permutation rule is available.
		"""
		for left_i in range(len(left_info[0])):
			for right_i in range(len(right_info[0])):
				# applied on the same qubit?
				if(left.qubits[left_info[0][left_i][0]] == right.qubits[right_info[0][right_i][0]]):
					# generate single qubit gate i.e. basis array of length 1
					new_left_info = [[left_info[0][left_i]], left_info[1], left_info[2]]
					new_right_info = [[right_info[0][right_i]], right_info[1], right_info[2]]

					self._permute_single(new_left_info, new_right_info)
					
					# now update the multi qubit elements
					left_info[0][left_i] = new_left_info[0][0] # update basis
					right_info[0][right_i] = new_right_info[0][0] # update basis
					left_info[2] = new_left_info[2] # update angle
					right_info[2] = new_right_info[2] # update angle

		# create new command for the permuted gates
		left.gate = BasePermutationRules._generate_gate(left_info)
		right.gate = BasePermutationRules._generate_gate(right_info)
		return


	def _permute_control_gates(self, left, right, left_info, right_info):
		"""
		Permutation rule between control gate and rotation

		Args:
            left (BasicGate): left gate of the commutation
            right (BasicGate): right gate of the commutation
            left_info (list): information on the left gate (from get_basis function)
            right_info (list): information on the right gate (from get_basis function)

        Raises:
            Exception if no permutation rule is available.
		"""

		# TODO
		return


	def _permute_single(self, left, right):
		"""
		Performes the permutation of two single qubit gates. Is used as a
		subroutine for multi-qubit rotational permutations.

		Args:
            left (list): information on the left gate (from the basis dictionary)
            right (list): information on the right gate (from the basis dictionary)

        Raises:
            Exception if no permutation rule is available.
		"""

		# perform permutation rule from dict
		key = (left[1],right[1])
		if(not key in _COMM_REL):
			raise PermutationRuleDoesNotExist("""This is not a valid gate for the 
			permutation rules. Allowed gatesets are currently: Pauli-rotations
			and controlled Pauli-rotations. Any other gate is currently 
			unsupported. Be sure to use the predefined decomposition rules.""")
		_COMM_REL[key](left, right)
		return


	def _generate_gate(gate):
		"""
		Translates from the symbolic description of gates back into a projectq
		gate using the dictionary below.
		"""
		if(len(gate[0])==1): # single qubit gate
			if(gate[0][0][1] in _GATE_FROM_INFO):
				return _GATE_FROM_INFO[gate[0][0][1]](gate[2])
		else: # multiqubit gate
			# use the updated basis information
			return gates.TimeEvolution(gate[2], gates.QubitOperator(gate[0]))
		raise PermutationRuleDoesNotExist("""Cannot create rotation gate from the
			provided information.""")