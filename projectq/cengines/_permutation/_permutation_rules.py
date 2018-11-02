
import projectq.ops as gates
from ._linkedlist import DoubleLinkedList
from projectq.ops._qubit_operator import _PAULI_OPERATOR_PRODUCTS, QubitOperator
from projectq.ops import TimeEvolution

#
# From the description of arXiv:1808.02892
#


_PRECISION = 10**-6

# define an error if incorrect gates are used
class PermutationRuleDoesNotExist(TypeError):
    pass


class BasePermutationRules(object):

	def __init__(self, linked_list):
		self.linked_list = linked_list


	def permute(self, left, right):
		assert(len(left.data.controls)<=1)
		assert(len(right.data.controls)<=1)

		left_info = self.get_basis(left.data.gate)
		right_info = self.get_basis(right.data.gate)

		# cannot permute two pi/8 rotations
		assert((not left_info[1] == "pi4") or (not right_info[1] == "pi4"))
		
		# check for control
		if(len(left.data.control_qubits) != 0 or len(right.data.control_qubits)!=0):
			self.permute_control_gates(left.data, right.data, left_info, right_info)
			self.linked_list.swap_elements(left,right)

		#check multi qubit operators
		if(isinstance(left_info[0], tuple) or isinstance(right_info[0], tuple)):
			self.permute_multiqubit(left.data, right.data, left_info, right_info)
			self.linked_list.swap_elements(left,right)
			return

		else: # both single qubit gates
			assert(len(left.qubits) == 1)
			assert(len(right.qubits) == 1)

			if(left.qubits[0] != right.qubits[0]):
				self.linked_list.swap_elements(left,right)
				return
			self.permute_single(left.datat, right.data, left_info, right_info)
			self.linked_list.swap_elements(left,right)
		return


	def get_basis(self, gate):
		if (isinstance(gate, gates.H)):
			return "H", "H"
		if(isinstance(gate,gates.X)):
			return "X", "pi"
		if(isinstance(gate,gates.Rx)):
			if(abs(gate.angle)-cmath.pi/2 < PRECISION):
				return "X", "pi2"
			elif(abs(gate.angle)-cmath.pi/4 < PRECISION):
				return "X", "pi4"
		if(isinstance(gate,gates.Y)):
			return "Y", "pi"
		if(isinstance(gate,gates.Ry)):
			if(abs(gate.angle)-cmath.pi/2 < PRECISION):
				return "Y", "pi2"
			elif(abs(gate.angle)-cmath.pi/4 < PRECISION):
				return "Y", "pi4"
		if(isinstance(gate,gates.Z)):
			return "Z", "pi"
		if(isinstance(gate,gates.Rz)):
			if(abs(gate.angle)-cmath.pi/2 < PRECISION):
				return "Z", "pi2"
			elif(abs(gate.angle)-cmath.pi/4 < PRECISION):
				return "Z", "pi4"
		if(isinstance(gate,gates.S)):
			return "Z", "pi2"
		if(isinstance(gate,gates.T)):
			return "Z", "pi4"
		# multi target rotations are implemented using the TimeEvolution class
		if(isinstance(gate,TimeEvolution)):
			if (isinstance(gate.hamiltonian, QubitOperator)):
				# the hamiltonian should only have one term with 1
				assert(len(gate.hamiltonian.terms) == 1)
				bases = list(H.terms.keys())[0]

				#only allow prefactor of 1 (the angle is given by the time)
				assert(list(gate.hamiltonian.values())[0] == 1)

				# time in TimeEvolution operator gives rotation angle
				if(abs(gate.time)-cmath.pi/2 < PRECISION):
					return bases, "pi2"
				elif(abs(gate.time)-cmath.pi/4 < PRECISION):
					return bases, "pi4"

		raise PermutationRuleDoesNotExist("""This is not a valid gate for the 
			permutation rules. Allowed gatesets are currently: Pauli-rotations
			and controlled Pauli-rotations. Any other gate is currently 
			unsupported. Be sure to use the predefined decomposition rules.""")


	def permute_multiqubit(left, right, left_info, right_info):

		# bring any other rotation gate into right form
		if(not isinstance(left_info[0], tuple)):
			#hadamard?
			if(left_info[0] == "H"):
				
			left_info[0] = (((0, left_info[0]), 1))
		if(not isinstance(right_info[0],tuple)):
			if(right_info[0] == "H"):
				TODO
			right_info[0] = (((0, right_info[0]), 1))

		# now in the proper format:
		for l in left_info[0]:
			for r in right_info[0]:
				#applied on the same qubit?
				if(left.qubits[l[0]] == right.qubits[r[0]])
					new_left_info = (l[1], left_info[1])
					new_right_info = (r[1], right_info[1])
					new_left = 
					new_right = TODO
					permute_single(new_left, new_right, new_left_info, new_right_info)
					# now update the multi qubit elements
					
					left_info = TODO
					right_info = TODO
		return


	def permute_control_gates(left,right, left_info, right_info):
		return


	def permute_single(left, right,left_info, right_info):
		"""
		Performes the permutation of two single qubit gates
		"""

		# perform permutation rule from dict
		key = (left_info[1],right_info[1])
		if(not key in _ROT_COMM_REL):
			raise PermutationRuleDoesNotExist("""This is not a valid gate for the 
			permutation rules. Allowed gatesets are currently: Pauli-rotations
			and controlled Pauli-rotations. Any other gate is currently 
			unsupported. Be sure to use the predefined decomposition rules.""")

		_ROT_COMM_REL[key](left, right, left_info, right_info)
		return




def comm_rel_Hadamard_Rot(rot, rot_info):
	rot_info = swapXandZ(rot_info)
	rot = generate_command(rot_info)
	return rot

def comm_rel_Pi2_Pi4(left, right,left_info, right_info):
	angle = left.angle
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left_info[0],right_info[0])]
	factor *= 1.j
	if (abs(factor - 1) < PRECISION):
		angle *= -1
	swap_modify_right(left, right, angle)
	return

def comm_rel_Pi4_Pi8(left, right,left_info, right_info):
	angle = right.angle
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left_info[0],right_info[0])]
	factor *= 1.j
	if (abs(factor - 1) < PRECISION):
		angle *= -1
	swap_modify_left(left, right, angle)
	return




def perm_multiqubitop_hadamard(hadamard ):
	pos = obtain_same_qubit(right,left)
	if(pos == -1):
		return
	right_info[pos][1] = swapXandZ(right_info[pos][1])
	right.hamiltonian.terms = {right_info: 1.}
	return


def swap_modify_left(left, right, angle):
	new_basis = _PAULI_OPERATOR_PRODUCTS[(left_info[0],right_info[0])]
	# global phases can be ignored
	right.data = get_operation(new_basis[1], angle)
	return

def swap_modify_right(left, right, angle):
	new_basis = _PAULI_OPERATOR_PRODUCTS[(left_info[0],right_info[0])]
	# global phases can be ignored
	left.data = get_operation(new_basis[1], angle)
	return


def obtain_same_qubit(multiqubit,single):
	for i in range(len(multiqubit.qubits)):
		if(single.qubits[0] == multiqubit.qubits[i]):
			return i
	return -1


def generate_command(rotation_info):
	"""
	Translates from the symbolic relation back to a message that is
	interpretable by compiler engines
	"""
	if(rotation_info[0]=="X"):
		return gates.Rx(rotation_info[1])
	elif(rotation_info[0]=="Y"):
		return gates.Ry(rotation_info[1])
	elif(rotation_info[0]=="Z"):
		return gates.Rz(rotation_info[1])

	raise PermutationRuleDoesNotExist("""Cannot create rotation gate from the
		provided information.""")

def swapXandZ(input, angle):
	if(input == "X"):
		return "Z", angle
	elif(input == "Z"):
		return "X", angle
	return input, angle









# lookup table: which function implements the correct commutation relation
# given the a pair of operators as key
#
# This lookup table implemets the following commutation relations relation
# (1) P * P'(phi) = P'(phi) * P
# (2) P'(phi) * P = P * P'(-phi)
# (3) P(pi/2) * P'(phi) = (i P P')(phi) * P(pi/2)
# (4) P'(phi) * P(pi/2) = P(pi/2) * (i P P')(-phi)
# 
# Here, P and P' are bases for one of the Pauli-rotations (Rx, Ry, Rz).
# The angle pi/2 indicates S gates, phi is arbitrary and if the angle is omitted,
# a standard Pauli operator (angle = pi) is used.


_ROT_COMM_REL = {
	("H","pi2"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(right, right_info),
	("pi2","H"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(left, left_info),
	("pi4","H"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(left, left_info),
	("H","pi4"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(right, right_info),
	("pi","H"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(right, right_info),
	("H","pi"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(left, left_info),
	("pi2","pi2"): lambda left, right, left_info, right_info:
				_swap_modify_right(left, right, -right_info[1]),
	("pi4","pi2"): _comm_rel_Pi2_Pi4,
	("pi2","pi4"): _comm_rel_Pi2_Pi4,
	("pi","pi"): lambda left, right, left_info, right_info:
				ll.swap_elements(left, right),
	("pi","pi2"): lambda left, right, left_info, right_info:
				_swap_modify_right(left, right, -right_info[1]),
	("pi2","pi"): lambda left, right, left_info, right_info:
				_swap_modify_left(left, right, -left_info[1]),
	("pi","pi4"): lambda left, right, left_info, right_info:
				_swap_modify_right(left, right, -right_info[1]),
	("pi4","pi"): lambda left, right, left_info, right_info:
				_swap_modify_left(left, right, -left_info[1])
}