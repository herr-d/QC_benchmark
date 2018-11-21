import json
from os import listdir
from os.path import isfile, join

FILENAMES = [name for name in listdir("distillations") if isfile(join("distillations", name))]




class DistillationLibraryError(Exception):
    pass


class DistillationEngine(object):
    def __init__(self):
        self._protocol = None
        pass

    def required_p_err(no_magic_states, max_total_err):
        return 1-(1-max_total_err)**(1./no_magic_states)

    def find_distillation_protocol(max_error, p_phys):
        # TODO: add more distillation protocols
        # TODO: make the decision more intelligent and don't
        #       just pick the first suitable
        for FILENAMES in self.library:
            with open(filename) as fin:
                dist_info = json.load(fin)
                p_out = dist_info["reduction factor"] * p_phys ** dist_info["reduction exponent"]
                if(p_out < max_error):
                    self._protocol = dist_info
                    return
        raise DistillationLibraryError("No suitable distillation protocol found")