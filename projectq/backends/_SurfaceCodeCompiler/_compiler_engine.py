from projectq.cengines import BasicEngine, LastEngineException
from projectq.cengines._permutation._permutation_relations import _GATE_TO_INFO
from projectq.backends._SurfaceCodeCompiler._distillation import DistillationEngine
import projectq.ops as gates

class SurfaceCodeCompileError(RuntimeError):
    pass

class SurfaceCode_Base(BasicEngine):
    def __init__(self, total_err_prob = 0.01):
        BasicEngine.__init__(self)
        self._distEngine = DistillationEngine()
        self._command_buffer = []
        self._Tgate_count = 0
        self._logical_qubit_count = 0
        self._total_err_prob = total_err_prob
        self._remap = dict()


    def is_available(self, cmd):
        """
        Specialized implementation of is_available: Returns True if the
        CommandPrinter is the last engine (since it can print any command).

        Args:
            cmd (Command): Command of which to check availability (all
                Commands can be printed).
        Returns:
            availability (bool): True, unless the next engine cannot handle
                the Command (if there is a next engine).
        """
        try:
            return BasicEngine.is_available(self, cmd)
        except LastEngineException:
            return True

    
    def generate_layout(self):
        raise SurfaceCodeCompileError("Use a derived class to perform"
            "the a proper layouting")


    def logical_error_probability(distance, p_phys):
        """
        Calculates the probability of an error in a single patch of space-time
        volume d^3. Given the distance of the surface code and the physical error-rate.
        """
        # 8 time steps per cycle
        p_phys *= 8

        # use equation from fowlers paper on logical error rate
        tmp = d*math.factorial(d) / (math.factorial(int((d+1)/2) - 1)
            * math.factorial(int((d+1)/2)))
        return tmp * p**int(d+1)/2


    def calc_distance(p_err_out, p_phys, spacetime_volume,
                    min_dist = 3, max_dist = 50):
        """
        Find the lowest distance for which the error rate of the whole circuit
        is given by less than p_err_out. Given a physical error rate of p_phys.  
        """
        for d in range(50):
            if(p_err_out > (1-logical_error_probability(d,p_phys))**spacetime_volume):
                return d
        raise RuntimeError("Could not find a suitable distance")


    def receive(self, command_list):
        """
        TODO
        """
        # TODO: if the commands are grouped assume they are commuting and can
        # be applied in parallel
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
            elif (isinstance(cmd.gate, gates.ClassicalInstructionGate)):
                continue
            elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
                self._Tgate_count += 1
                self._command_buffer.append(cmd)
            else:
                raise TypeError("Non supported gate for the surface"
                    "layouting received: " + str(cmd.gate))
        return



class FastHeuristicLayout(SurfaceCode_Base):
    """
    This heuristic layout uses a time efficient placement of data qubits.
    See arXiv:1808.02892v2 for the details.
    """
    def __init__(self):
        SurfaceCode_Base.__init__()


    def generate_layout():
        # Determine the fidelity of Magic states
        #required_p_err()

        return