import asyncio
import websockets
import json

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
    except:
        pass
    finally:
        clients.remove(websocket)

async def send_job(jobid, ms, name):
    data = json.dumps({"jobid": jobid, "ms": ms, "name": name})
    await asyncio.gather(*[client.send(data) for client in clients])

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("✅ WebSocket server running on ws://0.0.0.0:8765")
        while True:
            await asyncio.sleep(1)

asyncio.run(main())
