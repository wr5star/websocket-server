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

# WebSocket server (Render should NOT health-check this)
async def start_websocket():
    print("✅ WebSocket running on port 8765")
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # keep alive

# Health-check HTTP server (Render will ping this instead)
async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_http():
    app = web.Application()
    app.add_routes([web.get("/", health_check)])  # GET automatically covers HEAD
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    print("🟢 HTTP health check on port 10000")

async def main():
    await asyncio.gather(start_websocket(), start_http())

if __name__ == "__main__":
    asyncio.run(main())
