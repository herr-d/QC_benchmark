from ._gates import MeasurementGate


class ParityMeasurementGate(MeasurementGate):
	def __init__(self, bases):
		"""
		
		"""
		self._bases = []
		for el in term.split():
			if len(el) < 2:
				raise ValueError('term specified incorrectly.')
				_bases.append((int(el[1:]), el[0]))

		# Test that _bases has correct format of tuples
		for local_operator in _bases:
			qubit_num, action = local_operator
			if not isinstance(action, str) or action not in 'XYZ':
				raise ValueError("Invalid action provided: must be "
					"string 'X', 'Y', or 'Z'.")
				if not (isinstance(qubit_num, int) and qubit_num >= 0):
					raise QubitOperatorError("Invalid qubit number "
						"provided to QubitTerm: "
						"must be a non-negative "
						"int.")
		# Sort and add to self.terms:
		_bases.sort(key=lambda loc_operator: loc_operator[0])
		return

	def __or__(self, qubits):
		"""
		Only accepts a 
		"""
        qubits = self.make_tuple_of_qureg(qubits)
        if len(qubits) != 1:
            raise TypeError("Only one qubit or qureg allowed.")
        
        # Check that Qureg has enough qubits:
        num_qubits = len(qubits[0])
        non_trivial_qubits = set()
        for index, action in _bases:
            non_trivial_qubits.add(index)
        if max(non_trivial_qubits) >= num_qubits:
            raise ValueError("QubitOperator acts on more qubits than the qureg "
                             "is applied to.")
        
        # Perform X,Y,Z measurement if ParityMeasurement acts only on one qubit
        if len(_bases) == 1:
            if _bases[0][1] == "X":
            	H | qubits[0][_bases[0][0]]
                Measure | qubits[0][_bases[0][0]]
            elif _bases[0][1] == "Y":
            	S*H | qubits[0][_bases[0][0]]
                Measure | qubits[0][_bases[0][0]]
            elif _bases[0][1] == "Z":
                Measure | qubits[0][_bases[0][0]]
            return

        # Create new ParityMeasurement gate with rescaled qubit indices in
        # 0,..., len(non_trivial_qubits) - 1
        new_index = dict()
        non_trivial_qubits = sorted(list(non_trivial_qubits))
        for i in range(len(non_trivial_qubits)):
            new_index[non_trivial_qubits[i]] = i
        new_paritymeasurement = ParityMeasurementGate()
        new_bases = [tuple(new_index[index], action) for index, action in _bases]
        new_qubits = [qubits[0][i] for i in non_trivial_qubits]
        # Apply new gate
        cmd = new_qubitoperator.generate_command(new_qubits)
        apply_command(cmd)
		pass