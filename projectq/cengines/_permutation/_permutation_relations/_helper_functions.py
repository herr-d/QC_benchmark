#
# Contains some helper functions for the description of the commutation relations
#

def modify_gate(gate, new_basis, new_angle):
	"""
	Assigns to the gate a new basis and angle. This function is needed since
	assignments are forbidden in lambda functions.
	"""
	gate[2] = new_angle
	gate[0][0] = (gate[0][0][0],new_basis)
	return


def do_nothing():
	"""
	It does nothing. Literally.
	"""
	return