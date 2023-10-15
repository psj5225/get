import asyncio
async def say(what, when): #코루틴은 함수 앞에 async를 붙임
    await asyncio.sleep(when) #코루틴은 await로 완료 대기
    print(what)

async def stop_after(loop, when):
    await asyncio.sleep(when)
    loop.stop()

loop = asyncio.get_event_loop() #이벤트 루프를 가져옴

loop.create_task(say('first hello', 2))
loop.create_task(say('second hello', 1))
loop.create_task(say('third hello', 4))
loop.create_task(stop_after(loop,3))

loop.run_forever()
loop.close()