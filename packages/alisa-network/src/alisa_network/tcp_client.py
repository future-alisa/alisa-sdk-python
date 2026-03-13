import asyncio
import struct
from typing import Optional
from alisa_log import log 

class AlisaTCPClient:
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self._lock = asyncio.Lock()  

    async def connect(self):
        """建立连接（线程安全）"""
        async with self._lock:
            if self.writer and not self.writer.is_closing():
                return
            
            try:
                log.info(f"Connecting to TCP {self.host}:{self.port}...")
                self.reader, self.writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port),
                    timeout=self.timeout
                )
                log.info("TCP Connection established.")
            except Exception as e:
                log.error(f"Failed to connect to TCP: {e}")
                self.writer = None
                raise

    async def send(self, data: str):
        """发送数据：包含自动重连逻辑"""
        if not self.writer or self.writer.is_closing():
            await self.connect()
        assert self.writer is not None
        try:
            body = data.encode('utf-8')
            header = struct.pack('!I', len(body)) 
            self.writer.write(header + body)
            await self.writer.drain() 
        except Exception as e:
            log.error(f"TCP Send Error: {e}")
            self.writer = None 
            raise

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None