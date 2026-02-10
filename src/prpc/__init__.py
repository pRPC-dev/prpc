__version__ = "0.1.0"

from .cli import app
from .core.decorators import default_registry, rpc
from .core.registry import ProcedureRegistry

__all__ = ["app", "ProcedureRegistry", "rpc", "default_registry"]


