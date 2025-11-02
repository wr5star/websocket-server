import asyncio
import websockets
from aiohttp import web

connected = set()

async def ws_handler(websocket):
    print("Client connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected.remove(websocket)
        print("Client disconnected")

# WebSocket server
async def start_websocket():
    print("✅ WebSocket running on port 8765")
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

# HTTP health check (Render uses this)
async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_http():
    app = web.Application()
    # ✅ Only GET route — do NOT add web.head()
    app.add_routes([web.get("/", health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    print("🟢 Health check running on port 10000")

async def main():
    await asyncio.gather(start_websocket(), start_http())

if __name__ == "__main__":
    asyncio.run(main())
