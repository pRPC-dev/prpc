import pytest
from prpc import rpc, asgi_app, default_registry, RPCClient

@pytest.fixture(autouse=True)
def clear_registry():
    default_registry._procedures.clear()

@pytest.mark.anyio
async def test_client_async_success():
    @rpc
    def add(a: int, b: int) -> int:
        return a + b
    
    # We use asgi transport to test without a real server
    async with RPCClient("http://test", is_async=True) as client:
        # Mocking the internal client to use ASGITransport
        import httpx
        client._client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=asgi_app), 
            base_url="http://test"
        )
        
        result = await client.add(10, 20)
        assert result == 30
        
        # Test keyword arguments
        result = await client.add(a=5, b=5)
        assert result == 10

def test_client_sync_success():
    @rpc
    def multiply(a: int, b: int) -> int:
        return a * b
    
    # Sync mode also uses _client (bridged by anyio)
    with RPCClient("http://test", is_async=False) as client:
        # Mocking the internal client to use ASGITransport
        import httpx
        client._client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=asgi_app), 
            base_url="http://test"
        )
        
        result = client.multiply(10, 2)
        assert result == 20

@pytest.mark.anyio
async def test_client_async_error():
    @rpc
    def fail():
        raise ValueError("RPC Error Test")
    
    async with RPCClient("http://test") as client:
        import httpx
        client._client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=asgi_app), 
            base_url="http://test"
        )
        
        with pytest.raises(RuntimeError) as exc:
            await client.fail()
        assert "RPC Error Test" in str(exc.value)

