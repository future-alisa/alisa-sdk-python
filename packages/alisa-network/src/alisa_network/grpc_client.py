import grpc

class AlisaGRPCClient:
    def __init__(self, target: str):
        self.target = target
        self.channel = grpc.aio.insecure_channel(
            target,
            options=[
                ('grpc.keepalive_time_ms', 10000),
                ('grpc.keepalive_timeout_ms', 5000),
                ('grpc.http2.max_pings_without_data', 0),
            ]
        )

    async def get_stub(self, stub_class):
        """注入 Stub 类"""
        return stub_class(self.channel)

    async def close(self):
        await self.channel.close()