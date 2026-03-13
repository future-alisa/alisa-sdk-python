import httpx
from typing import Optional, Dict, Any

class AlisaHTTPClient:
    def __init__(self, base_url: str = "", timeout: float = 10.0):
        # 生产级连接池配置
        limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            limits=limits,
            http2=True  # 默认开启 HTTP/2
        )

    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """统一请求入口，增加异常捕获"""
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # 这里可以调用之前封装的 log.error
            raise RuntimeError(f"HTTP Error: {e.response.status_code}")
        except Exception as e:
            raise RuntimeError(f"Network Error: {str(e)}")

    async def close(self):
        await self.client.aclose()