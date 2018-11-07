



def permute_control_rotation(control_gate, control_info, rotation, rotation_info):
	r_pos = rotation.qubits.index(control.control_qubits[0])
	# check commutation relation of basis
	if("Z" != rotation_info[0][r_pos][1]): # they anticommute and targets need to be added
		for i in control_info[0]:
			assert((not control.qubits[i[0]] in rotation.qubits))
			rotation_info[0].append((len(rotation.qubits),i[1]))
			rotation.qubits.append(control.qubits[i[0]])
	return

def permute_target_rotation(control_gate, control_info, rotation, rotation_info):
	# first check that controlled gate is pauli
	assert(control_info[1] == "pi")
	if(_calc_parity(control_gate, control_info, rotation, rotation_info) == -1):
		# add control to rotation
		rotation_info[0].append((len(rotation.qubits),"Z"))
		rotation.qubits.append(control.control_qubits[0])
	# otherwise gates commute
	return


# Helper functions

def _calc_parity(left, left_info, right, right_info):
	parity = 1
	for l in left_info:
		try:
			pos = right.qubits.index(left.qubits[l[0]])
		except:
			continue
		# now check if different basis
		for r in right_info:
			if(r[0] == pos and r[1] != l[1]):
				parity *= -1
			else:
				break
	return parity