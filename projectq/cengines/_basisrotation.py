
import projectq
from projectq.cengines import (BasicEngine,
                               ForwarderEngine,
                               CommandModifier)
import projectq.ops as gates


class BasisRotation(BasicEngine):
    """
    This engine transforms the Basis of TimeEvolution and ParityMeasurementGate operators
    to the Z basis, by inserting appropriate basis tranformation operations
    """
    def __init__(self):
        BasicEngine.__init__(self)

    
    def TimeEvolution(self, cmd):
        """
        Handles the basis transformation for TimeEvolution operators
        """
        assert(isinstance(cmd.gate.hamiltonian, gates.QubitOperator))
        bases = list(cmd.gate.hamiltonian.terms.keys())[0]
        self.rotation(bases, cmd)
        new_bases = tuple(((basis[0],"Z") for basis in bases))
        new_cmd = gates.TimeEvolution(cmd.gate.time, gates.QubitOperator(new_bases)).generate_command(cmd.qubits[0])
        self.send([new_cmd])
        self.dagger_rotation(bases, cmd)


    def ParityMeasurementGate(self, cmd):
        """
        Handles the basis transformation for ParityMeasurementGates
        """
        self.rotation(cmd.gate._bases, cmd)
        new_bases = list((basis[0],"Z") for basis in cmd.gate._bases)
        new_cmd = gates.ParityMeasurementGate(new_bases).generate_command(cmd.qubits[0])
        self.send([new_cmd])
        self.dagger_rotation(cmd.gate._bases, cmd)


    def rotation(self, bases, cmd):
        """
        Handles general basis rotations using a list of bases
        """
        for basis in bases:
            if(basis[1]) == "X":
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])
            if(basis[1]) == "Y":
                self.send([gates.S.generate_command(cmd.qubits[0][basis[0]])])
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])


    def dagger_rotation(self, bases, cmd):
        """
        Handles general basis rotations using a list of bases
        """
        for basis in bases:
            if(basis[1]) == "X":
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])
            if(basis[1]) == "Y":
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])
                self.send([gates.Sdag.generate_command(cmd.qubits[0][basis[0]])])



    def receive(self, command_list):
        for cmd in command_list:

            if(isinstance(cmd.gate, gates.TimeEvolution)):
                self.TimeEvolution(cmd)

            elif(isinstance(cmd.gate, gates.ParityMeasurementGate)):
                self.ParityMeasurementGate(cmd)

            else:
                #just send the command along
                self.send([cmd])