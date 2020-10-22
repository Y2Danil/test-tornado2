import asyncio

async def a():
  print('a')
  await asyncio.sleep(2)
  await print('a')

async def b():
  print('b')
  await asyncio.sleep(2)
  print('b')
  
async def c():
  print('c')
  await asyncio.sleep(2)
  print('c')
  
ioloop = asyncio.get_event_loop()
tasks = [a(), b(), c()]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()