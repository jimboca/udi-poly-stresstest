
""" Node classes used by the Stress Test Node Server. """

try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface

from .STNode1      import STNode1
from .Controller   import Controller
