import asyncio
import websockets
from aiohttp import web
import os

# ===============================
#  WebSocket Server (Port 8765)
# ===============================
connected_clients = set()

async def handler(websocket):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")

async def start_websocket():
    port = 8765
    print(f"✅ WebSocket server ready on port {port}")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # Run forever

# ===============================
#  HTTP Health Check (Port 10000)
# ===============================
async def healthcheck(request):
    return web.Response(text="OK", status=200)

async def start_http():
    app = web.Application()
    app.add_routes([web.get("/", healthcheck)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    print("🟢 Health check running on port 10000")

# ===============================
#  Run Both
# ===============================
async def main():
    await asyncio.gather(start_websocket(), start_http())

if __name__ == "__main__":
    asyncio.run(main())
