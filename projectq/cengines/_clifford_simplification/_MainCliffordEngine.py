
from projectq.cengines import BasicEngine
from projectq.cengines._permutation._permutation_rules import BasePermutationRules
from projectq.cengines._clifford_simplification._CliffordSimulator import CliffordSimulator
import projectq.ops as gates


class CliffordEngine(BasicEngine):
    def __init__(self):
        super(CliffordEngine, self).__init__()
        self._simulator = CliffordSimulator()
        self._gates = []



class MultiqubitMeasurementCliffordEngine(CliffordEngine):
    """
    Performs Simulation of quantum circuits using the Stabilizer formalism.
    Currently non-Clifford gates are not supported.
    """
    def __init__(self):
        super(MultiqubitMeasurementCliffordEngine, self).__init__()
        self._simulator = CliffordSimulator()

    def perform_simulation(self):
        for gate in reversed(self._gates):
            self._simulator.apply_operation(gates.get_inverse(gate))

        for bases, qubits, parity in self._simulator.return_stabilizers():
            cmd = gates.ParityMeasurementGate(bases,parity).generate_command(qubits)
            self.send([cmd])

    def receive(self, command_list):
        """
        Receive commands from the previous engine and cache them.
        If a flush gate arrives, this engine assumes the circuit is
        finished and sends the permuted circuit to the next engine.
        """
        for cmd in command_list:
            if (isinstance(cmd.gate, gates.FlushGate)): # flush gate --> returns the current stabilizers as parity measurements
                self.perform_simulation()
                # reset the simulator
                self._gates = []
                self._simulator = CliffordSimulator()
                self.send([cmd])
            elif (isinstance(cmd.gate, gates.AllocateQubitGate)):
                self._simulator.add_qubit_to_dict(cmd.qubits[0])
                self.send([cmd]) # send gate along
            elif (isinstance(cmd.gate, gates.MeasureGate)):
                self._simulator.add_stabilizer([(cmd.qubits[0],"Z")])
            elif (isinstance(cmd.gate, gates.ClassicalInstructionGate)):
                return
            elif (BasePermutationRules.is_clifford(cmd.gate)):
                self._gates.append(cmd)
            elif (len(self._gates) == 0):
                # non-clifford rotation from the beginning of the circuit
                self.send([cmd])
            else: # new command
                raise TypeError("This gate is not supported")