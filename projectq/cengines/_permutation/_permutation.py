
from projectq.cengines import BasicEngine
from projectq.ops import FlushGate, FastForwardingGate, NotMergeable
from ._linkedlist import DoubleLinkedList

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
        self._perm = permutation_rule
        self._dllist = DoubleLinkedList()  # dict of lists containing operations for each qubit


    def _send_qubit_pipeline(self, idx, n):
        """
        Send the first gates that are already in the proper location
        """

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
            if cmd.gate == FlushGate():  # flush gate --> permute and flush
                print("Warning: recieved a flush gate. For the permutation engine to work a flush can only be performed at the very end.")
                self.perform_permutation()
                self.send([cmd])

            else: # new command
                # push back command into linked list
                self._dllist.push_back(cmd)




class PermuteFront(PermuteBase):
    def permute(self):
        for node in self._dllist:
            # iteration along the linked list
            # once a gate is found it is permuted to the front using
            if(perm.gate_of_interest(node)):
                # create a block of this single gate
                # This is needed because additional gates are created by the
                # permutation rules and need to be moved to the front

                block = [node]
                current = block[0].prev
                while(perm.permutation_required(current, block)):
                    #TODO
                    print("Todo")

        return
