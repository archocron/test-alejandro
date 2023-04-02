import asyncio

# coroutine to send message to server
async def send_message(writer):
    loop = asyncio.get_event_loop()
    while True:
        data = await loop.run_in_executor(None, input) + '\n'
        writer.write(data.encode())
        await writer.drain()
        if data =="quit\n":
            break
    # close connection
    writer.close()
    await writer.wait_closed() 

# coroutine to handle received messages
async def receive_message(reader):
    while True:
        data = await reader.read(1024)
        message = data.decode().strip()
        if not message:
            break
        print(message)

# main coroutine
async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 65432)
    await asyncio.gather(send_message(writer), receive_message(reader))      

asyncio.run(main())