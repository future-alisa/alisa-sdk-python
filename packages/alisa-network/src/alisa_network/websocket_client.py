import asyncio
import logging
import json
from websockets.asyncio.client import connect

class WSClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.ws = None
        self._stop_event = asyncio.Event()
        self._connected = asyncio.Event()

    async def start(self):
        while not self._stop_event.is_set():
            try:
                async with connect(self.uri, ping_interval=20) as websocket:
                    self.ws = websocket
                    self._connected.set()
                    logging.info("WebSocket 已连接")
                    
                    await self._message_handler(websocket)
            except Exception as e:
                self._connected.clear()
                self.ws = None
                if not self._stop_event.is_set():
                    logging.error(f"连接断开: {e}，5秒后重连...")
                    await asyncio.sleep(5)

    async def _message_handler(self, websocket):
        """
        这里不再引用 self.ws，而是直接用参数传进来的已确认存在的连接对象。
        解决了 IDE 报红 NoneType 不可迭代的问题。
        """
        async for message in websocket:
            asyncio.create_task(self.on_message(message))

    async def on_message(self, message):
        data = json.loads(message)
        print(f"收到数据: {data}")

    async def send(self, payload):
        await self._connected.wait()
        assert self.ws is not None
        await self.ws.send(json.dumps(payload))

    async def stop(self):
        self._stop_event.set()
        if self.ws:
            await self.ws.close()