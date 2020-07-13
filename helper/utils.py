import asyncio
import aiohttp
import os


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'{path} 已创建！')
    else:
        print(f'{path} 已存在！')
    return os.path.abspath(path)


# 异步 request
async def request(url='', method='get', cookies='', headers='', **kwargs):
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.request(
                method=method, url=url, headers=headers, **kwargs) as resp:
            return await resp.read()


# 异步调度函数
def handle_tasks(loop, func, args):
    if isinstance(args, list):
        tasks = [asyncio.ensure_future(func(arg)) for arg in args]
        loop.run_until_complete(asyncio.wait(tasks))
        return [task.result() for task in tasks]
    elif isinstance(args, str):
        task = asyncio.ensure_future(func(args))
        loop.run_until_complete(task)
        return [task.result()]


if __name__ == "__main__":
    urls = 'http://www.baidu.com'
    # urls = [urls for _ in range(3)]
    loop = asyncio.get_event_loop()
    res = handle_tasks(loop, request, urls)
    loop.close()
    assert res is not None
    print(res)
