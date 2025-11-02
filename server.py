import asyncio
import websockets
from aiohttp import web

connected = set()

async def ws_handler(websocket):
    connected.add(websocket)
    print("🟢 Client connected:", websocket.remote_address)
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    except websockets.ConnectionClosed:
        print("🔴 Client disconnected:", websocket.remote_address)
    finally:
        connected.remove(websocket)

async def websocket_server():
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        print("✅ WebSocket server ready on port 8765")
        await asyncio.Future()  # Keep running forever

# --- HTTP Health Endpoint (for Render) ---
async def health_check(request):
    return web.Response(text="OK", status=200)

async def main():
    # aiohttp web server for health check
    app = web.Application()
    app.add_routes([web.get("/", health_check), web.head("/", health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    # Run both WebSocket and HTTP together
    await websocket_server()

if __name__ == "__main__":
    asyncio.run(main())
