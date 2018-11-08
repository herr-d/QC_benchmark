
from projectq.cengines import BasicEngine
from projectq.ops import FlushGate, FastForwardingGate, NotMergeable, AllocateQubitGate
from projectq.cengines._permutation._linkedlist import DoubleLinkedList
from projectq.cengines._permutation._permutation_rules import BasePermutationRules

class PermuteBase(BasicEngine):
    """
    Permutes all gates of a certain type to the front. For this the whole
    circuit needs to be read into memory and acted upon. Thus, it breaks the
    streaming operators after its application.

    All commands are stored in a linked lists. This allows O(1) inserts and
    deletion operations. Easy swaps between gates are also possible.
    """
    def __init__(self, permutation_rule):
        """
        Initialize a LocalOptimizer object.

        Args:
            m (int): Number of gates to cache per qubit, before sending on the
                first gate.
        """
        BasicEngine.__init__(self)
        self._dllist = DoubleLinkedList()  # dict of lists containing operations for each qubit
        self._perm = permutation_rule(self._dllist)


    def _send_qubit_pipeline(self):
        """
        Send the first gates that are already in the proper location
        """
        for node in self._dllist:
            self.send([node.data])
        return


    def _permute(self):
        """
        This function needs to be overwritten by the derived class.
        And should perform the Permutation.
        """
        return



    def receive(self, command_list):
        """
        Receive commands from the previous engine and cache them.
        If a flush gate arrives, this engine assumes the circuit is
        finished and sends the permuted circuit to the next engine.
        """
        for cmd in command_list:
            if (isinstance(cmd.gate, FlushGate)):  # flush gate --> permute and flush
                print("Warning: recieved a flush gate. For the permutation engine to work a flush can only be performed at the very end.")
                self.permute()
                self._send_qubit_pipeline()
                self.send([cmd])
            else: # new command
                # push back command into linked list
                self._dllist.push_back(cmd)




class PermutePi4Front(PermuteBase):
    def __init__(self):
        super(PermutePi4Front, self).__init__(BasePermutationRules)


    def permute(self):
        for node in self._dllist:
            if(self._gate_of_interest(node)):
                while(self._permutation_required(node.prev)):
                    self._perm.permute(node.prev, node)
        return


    def _gate_of_interest(self, node):
        if(self._perm.check_clifford(node)):
            return False
        return True


    def _permutation_required(self, left):
        if (left == None or isinstance(left.data.gate,AllocateQubitGate)):
            return False
        if(self._gate_of_interest(left)):
            return False
        return True