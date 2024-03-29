from projectq.backends._SurfaceCodeCompiler._compiler_engine import SurfaceCode_Base, SurfaceCodeCompileError
import projectq.ops as gates
from projectq.cengines._permutation._permutation_relations import _GATE_TO_INFO


class SimpleExporter(SurfaceCode_Base):
    """
    Simple exporter that writes instructions using Alexandru's code
    """

    def __init__(self, output = "instructions", total_err_prob = 0.01):
        SurfaceCode_Base.__init__(self, total_err_prob)
        self._output = output

    def receive(self, command_list):
        """
        TODO
        """
        # Need to specialize the receive command to add Hadamards and S gates
        for cmd in command_list:
            # flush gate --> returns the current stabilizers as parity measurements
            if (isinstance(cmd.gate, gates.FlushGate)):
                # finished perform placement
                self.generate_layout()
            elif (isinstance(cmd.gate, gates.AllocateQubitGate)):
                self._remap[cmd.qubits[0][0].id] = self._logical_qubit_count
                self._logical_qubit_count += 1
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.ParityMeasurementGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.SGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.HGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.DaggeredGate) and isinstance(cmd.gate._gate, gates.SGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.ClassicalInstructionGate)):
                continue

            elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
                self._Tgate_count += 1
                self._command_buffer.append(cmd)

            elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
                self._Tgate_count += 1
                self._command_buffer.append(cmd)
            else:
                raise TypeError("Non supported gate for the surface"
                    "layouting received: " + str(cmd.gate))
        return


    def _basis_trafo(self, info, cmd, fout):
        for basis in info[0]:
            if(basis[1]) == "X":
                fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
            if(basis[1]) == "Y":
                fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
                fout.write("S " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")

    def _basis_trafo_back(self, info, cmd, fout):
        for basis in info[0]:
            if(basis[1]) == "X":
                fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
            if(basis[1]) == "Y":
                fout.write("S " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
                fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")


    def generate_layout(self):
        with open(self._output, "w") as fout:
            # write initialization (all have to be initialized at beginning)
            fout.write("INIT " + str(self._logical_qubit_count) + "\n")
            # perform gates
            for cmd in self._command_buffer:
                if (isinstance(cmd.gate, gates.AllocateQubitGate)):
                    # already done in the beginning
                    continue
                elif (isinstance(cmd.gate, gates.ParityMeasurementGate)):
                    qubits = ""
                    for basis in cmd.gate._bases:
                        qubits += " " + str(self._remap[cmd.qubits[0][basis[0]].id])
                    self._basis_trafo([cmd.gate._bases], cmd, fout)
                    if(len(cmd.gate._bases) == 1):
                        fout.write("MZ" + qubits + "\n")
                    else:
                        fout.write("MZZ" + qubits + "\n")
                    continue
                elif (isinstance(cmd.gate, gates.HGate)):
                    fout.write("H " + str(self._remap[cmd.qubits[0][0].id])+"\n")
                elif (isinstance(cmd.gate, gates.SGate)):
                    fout.write("S " + str(self._remap[cmd.qubits[0][0].id])+"\n")
                elif (isinstance(cmd.gate, gates.DaggeredGate) and isinstance(cmd.gate._gate, gates.SGate)):
                    fout.write("S " + str(self._remap[cmd.qubits[0][0].id])+"\n")
                elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
                    info = _GATE_TO_INFO[type(cmd.gate)](cmd.gate)
                    self._basis_trafo(info, cmd, fout)
                    fout.write("NEED A\n")
                    qubits = ""
                    for basis in info[0]:
                        qubits += " " + str(self._remap[cmd.qubits[0][basis[0]].id])
                    fout.write("MZZ A" + qubits + "\n")
                    fout.write("MX A\n")
                    fout.write("S ANCILLA\n") # TODO: add information for initialization
                    fout.write("MXX ANCILLA" + qubits + "\n")
                    self._basis_trafo_back(info, cmd, fout)

                else:
                    raise TypeError("Non supported gate for the surface"
                        "layouting received: " + str(cmd.gate))