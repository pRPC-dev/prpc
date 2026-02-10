from fastapi import FastAPI
from prpc import rpc, mount_fastapi
import uvicorn

app = FastAPI(title="pRPC Basic Example")

@rpc
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@rpc
def greet(name: str = "World") -> str:
    """Greets a user."""
    return f"Hello, {name}!"

@rpc
async def get_status() -> dict:
    """Asynchronously returns server status."""
    return {"status": "online", "version": "0.1.0"}

# Mount the RPC handles to /rpc
mount_fastapi(app)

if __name__ == "__main__":
    print("Starting basic_server on http://localhost:8000")
    print("RPC Endpoint: http://localhost:8000/rpc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
