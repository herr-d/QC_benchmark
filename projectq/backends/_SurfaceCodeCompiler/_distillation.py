from ._distillations import DIST_LIBRARY



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
        for dist_info in DIST_LIBRARY:
            p_out = dist_info["reduction factor"] * p_phys ** dist_info["reduction exponent"]
            if(p_out < max_error):
                self._protocol = dist_info
                return
        raise DistillationLibraryError("No suitable distillation protocol found")