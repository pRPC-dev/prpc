import uuid
from typing import Any, Dict, List, Optional, Union

import anyio
import httpx


class RPCClient:
    """
    A dynamic RPC client for pRPC.
    Allows calling remote procedures as if they were local methods.
    """

    def __init__(self, base_url: str, is_async: bool = True) -> None:
        """
        Initialize the RPC client.

        Args:
            base_url: The base URL of the pRPC server (e.g., http://localhost:8000).
            is_async: Whether to use async mode. Defaults to True.
        """
        self.base_url = base_url.rstrip("/")
        self.is_async = is_async
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=self.base_url)
        return self._client

    def __getattr__(self, name: str) -> Any:
        """
        Dynamically handle method calls.
        """
        if self.is_async:

            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await self._call_async(name, *args, **kwargs)

            return async_wrapper
        else:

            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return anyio.run(self._call_async, name, *args, **kwargs)

            return sync_wrapper

    async def _call_async(self, method: str, *args: Any, **kwargs: Any) -> Any:
        client = self._get_client()
        payload = self._prepare_payload(method, *args, **kwargs)
        response = await client.post("/rpc", json=payload)
        return self._handle_response(response)

    def _prepare_payload(self, method: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        params: Union[List[Any], Dict[str, Any]]
        if kwargs:
            params = kwargs
        else:
            params = list(args)

        return {
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params,
        }

    def _handle_response(self, response: httpx.Response) -> Any:
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            raise RuntimeError(f"RPC Error: {data['error']}")
        return data.get("result")

    async def aclose(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    def close(self) -> None:
        if self._client:
            # anyio.run can't be used here easily if a loop is running
            # but we can try to close it synchronously if it's just the client
            # For simplicity in this library, we'll use anyio.run
            try:
                anyio.run(self._client.aclose)
            except RuntimeError:
                # Loop already running, we might be in trouble but we'll try to just null it
                pass
            self._client = None

    async def __aenter__(self) -> "RPCClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.aclose()

    def __enter__(self) -> "RPCClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
