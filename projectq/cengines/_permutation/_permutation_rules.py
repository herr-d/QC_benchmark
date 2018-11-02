
import projectq.ops as gates
import cmath
from _linkedlist import DoubleLinkedList
from projectq.ops._qubit_operator import _PAULI_OPERATOR_PRODUCTS, QubitOperator
from projectq.ops import TimeEvolution

#
# From the description of arXiv:1808.02892
#


#
# The code for this engine needs to be restructured
# I think the best way would be to have a new folder with all possible
# permutation relations. Similar to how merging of gates is implemented
#

#needed for the comparison of angles
_PRECISION = 10**-6

# define an error if incorrect gates are used
class PermutationRuleDoesNotExist(TypeError):
    pass


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
		left_info = self.get_basis(left.data.gate)
		right_info = self.get_basis(right.data.gate)


		# cannot permute two pi/8 rotations
		assert((not left_info[1] == "pi4") or (not right_info[1] == "pi4"))
		
		# check for control
		if(len(left.data.control_qubits) != 0 or len(right.data.control_qubits)!=0):
			self.permute_control_gates(left.data, right.data, left_info, right_info)
			self.linked_list.swap_elements(left,right)
			return

		# perform permutation of not controlled gates
		self.permute_multiqubit(left, right, left_info, right_info)
		self.linked_list.swap_elements(left,right)
		return


	def get_basis(self, gate):
		"""
		Extract basic information from input gates such that the approprate
		commutation relations can be chosen.

		Args:
            gate (BasicGate): Gate that is involved in the permutation

        Raises:
            Exception if no permutation rule is available.
		"""
		if (isinstance(gate, gates.HGate)):
			return ["H", "H"]
		if(isinstance(gate,gates.XGate)):
			return ["X", "pi"]
		if(isinstance(gate,gates.Rx)):
			if(abs(gate.angle)-cmath.pi < _PRECISION):
				return ["X", "pi"]
			elif(abs(gate.angle)-cmath.pi/2 < _PRECISION):
				return ["X", "pi2"]
			elif(abs(gate.angle)-cmath.pi/4 < _PRECISION):
				return ["X", "pi4"]
		if(isinstance(gate,gates.YGate)):
			return ["Y", "pi"]
		if(isinstance(gate,gates.Ry)):
			if(abs(gate.angle)-cmath.pi < _PRECISION):
				return ["Y", "pi"]
			elif(abs(gate.angle)-cmath.pi/2 < _PRECISION):
				return ["Y", "pi2"]
			elif(abs(gate.angle)-cmath.pi/4 < _PRECISION):
				return ["Y", "pi4"]
		if(isinstance(gate,gates.ZGate)):
			return ["Z", "pi"]
		if(isinstance(gate,gates.Rz)):
			if(abs(gate.angle)-cmath.pi < _PRECISION):
				return ["Z", "pi"]
			elif(abs(gate.angle)-cmath.pi/2 < _PRECISION):
				return ["Z", "pi2"]
			elif(abs(gate.angle)-cmath.pi/4 < _PRECISION):
				return ["Z", "pi4"]
		if(isinstance(gate,gates.SGate)):
			return ["Z", "pi2"]
		if(isinstance(gate,gates.TGate)):
			return ["Z", "pi4"]

		# multi target rotations are implemented using the TimeEvolution class
		if(isinstance(gate,TimeEvolution)):
			if (isinstance(gate.hamiltonian, QubitOperator)):
				# the hamiltonian should only have one term with 1
				assert(len(gate.hamiltonian.terms) == 1)
				bases = list(H.terms.keys())[0]

				#only allow prefactor of 1 (the angle is given by the time)
				assert(list(gate.hamiltonian.values())[0] == 1)

				# time in TimeEvolution operator gives rotation angle
				if(abs(gate.time)-cmath.pi/2 < _PRECISION):
					return [bases, "pi2"]
				elif(abs(gate.time)-cmath.pi/4 < _PRECISION):
					return [bases, "pi4"]

		raise PermutationRuleDoesNotExist("""This is not a valid gate for the 
			permutation rules. Allowed gatesets are currently: Pauli-rotations
			and controlled Pauli-rotations. Any other gate is currently 
			unsupported. Be sure to use the predefined decomposition rules.""")


	def permute_multiqubit(self, left, right, left_info, right_info):
		"""
		Permutes two gates. The permutation relation of multi-qubit rotations
		are performed through a reduction to many single qubit commutation rules.

		Args:
            left (BasicGate): left gate of the commutation
            right (BasicGate): right gate of the commutation
            left_info (list): information on the left gate (from get_basis function)
            right_info (list): information on the right gate (from get_basis function)

        Raises:
            Exception if no permutation rule is available.
		"""
		# bring any other rotation gate into right form
		try:
			langle = left.data.gate.angle
		except:
			langle = 0

		try:
			rangle = right.data.gate.angle
		except:
			rangle = 0

		if(not isinstance(left_info[0], list)):
			# check for Hadamard
			#if(left_info[0] == "H"):
			#	right.data.gate = comm_rel_Hadamard_Rot(right.data, right_info)
			#	return
			left_info[0] = [[(0, left_info[0]), 1]]

		if(not isinstance(right_info[0],list)):
			# check for Hadamard
			#if(right_info[0] == "H"):
			#	left.data.gate = comm_rel_Hadamard_Rot(left.data, left_info)
			#	return
			right_info[0] = [[(0, right_info[0]), 1]]

		# now both rotations are guaranteed to be in the format multi qubit rotations:
		for l in left_info[0]:
			for r in right_info[0]:
				#applied on the same qubit?
				if(left.data.qubits[l[0][0]] == right.data.qubits[r[0][0]]):
					new_left_info = [l[0][1], left_info[1]]
					new_right_info = [r[0][1], right_info[1]]
					new_left = generate_gate(new_left_info[0], langle)
					new_right = generate_gate(new_right_info[0], rangle)
					self.permute_single(new_left, new_right, new_left_info, new_right_info)
					# now update the multi qubit elements
					l[1] =  new_left_info[0] # update basis
					r[1] =  new_right_info[0] # update basis
					#update angles
					try:
						langle = new_left.angle
					except:
						pass

					try:
						rangle = new_right.angle
					except:
						pass


		#now create new command for the permuted gates
		if(len(left_info[0])==1): # single qubit gate
			left.data.gate = generate_gate(left_info[0][0][1],langle)
		else: # multiqubit gate
			# use the updated basis information
			left.data.gate = TimeEvolution(gates.QubitOperator())
		if(len(right_info[0])==1): # single qubit gate
			right.data.gate = generate_gate(right_info[0][0][1],rangle)	

		return


	def permute_control_gates(self, left, right, left_info, right_info):
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
		return


	def permute_single(self, left, right,left_info, right_info):
		"""
		Performes the permutation of two single qubit gates. Is used as a
		subroutine for multi-qubit rotational permutations.

		Args:
            left (BasicGate): left gate of the commutation
            right (BasicGate): right gate of the commutation
            left_info (list): information on the left gate (from get_basis function)
            right_info (list): information on the right gate (from get_basis function)

        Raises:
            Exception if no permutation rule is available.
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


#
# Helper functions that are needed for performing the permutations.
# Maybe move these to a separate library folder that lists all possible
# permutation relations
#


def comm_rel_Hadamard_Rot(rot, rot_info):
	"""
	Changes the rotation when it is commuted with a Hadamard operator
	"""
	basis = "Z"
	if(rot_info[0] == "X"):
		basis = "Z"
	elif(rot_info[0] == "Z"):
		basis = "X"
	else: # for Y rotations the angle gets flipped
		rot.angle = 2*cmath.pi - rot.angle
		return
	return generate_gate(basis, rot.angle)


def comm_rel_Pi2_Pi4(left, right,left_info, right_info):
	angle = left.angle
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left_info[0],right_info[0])]
	factor *= 1.j
	if (abs(factor - 1) < PRECISION):
		angle *= 2*cmath.pi-angle
	swap_modify_right(left, right, angle)
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


def generate_gate(basis, angle):
	"""
	Translates from the symbolic relation back to a message that is
	interpretable by compiler engines
	"""
	if(basis == "H"):
		return gates.HGate()
	if(basis=="X"):
		return gates.Rx(angle)
	elif(basis=="Y"):
		return gates.Ry(angle)
	elif(basis=="Z"):
		return gates.Rz(angle)

	print(basis + " " + str(angle))
	raise PermutationRuleDoesNotExist("""Cannot create rotation gate from the
		provided information.""")





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
				comm_rel_Hadamard_Rot(left, left_info),
	("H","pi"): lambda left, right, left_info, right_info:
				comm_rel_Hadamard_Rot(right, right_info),
	("pi2","pi2"): lambda left, right, left_info, right_info:
				_swap_modify_right(left, right, -right_info[1]),
	("pi4","pi2"): comm_rel_Pi2_Pi4,
	("pi2","pi4"): comm_rel_Pi2_Pi4,
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