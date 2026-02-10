__version__ = "0.1.0"

from .adapters.fastapi import mount_fastapi
from .adapters.flask import mount_flask
from .cli import app
from .client.python_client import RPCClient, RPCError
from .client.ts_codegen import generate_typescript_client, save_typescript_client
from .core.decorators import default_registry, rpc
from .core.introspection import get_procedure_schema, get_registry_schema
from .core.interpreter import handle_request
from .core.models import RpcRequest, RpcResponse
from .core.registry import ProcedureRegistry
from .transport.asgi import PRPCAsgiApp, app as asgi_app

__all__ = [
    "app",
    "ProcedureRegistry",
    "rpc",
    "default_registry",
    "RpcRequest",
    "RpcResponse",
    "handle_request",
    "PRPCAsgiApp",
    "asgi_app",
    "mount_fastapi",
    "mount_flask",
    "RPCClient",
    "RPCError",
    "get_procedure_schema",
    "get_registry_schema",
    "generate_typescript_client",
    "save_typescript_client",
]











