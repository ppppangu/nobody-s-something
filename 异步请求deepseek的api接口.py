import os
from dotenv import load_dotenv, find_dotenv

import time
import asyncio
import aiohttp

load_dotenv(find_dotenv())
deepseek_api_key = os.getenv("DeepSeek_API_KEY")

semaphore =asyncio.Semaphore(1000)

async def _get_response(message,max_retries=3):
    async with semaphore:
        for i in range(max_retries):
            try:
                async with aiohttp.ClientSession(
                    base_url='https://api.deepseek.com/v1/',
                    headers = {"Content-Type":"application/json","Authorization":f"Bearer {deepseek_api_key}"}
                ) as session:
                    payload = {
                        'model':'deepseek-chat',
                        'messages':[
                            {'role':'system','content':'you are an ai assistant'},
                            {'role':'user','content':message}
                        ]
                    }
                    async with session.post(url='chat/completions',json=payload) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            pass
                            #print(f'Request failed with status {response.status}')
            except Exception as e:
                print(f'error:{e},等待第{i+1}/{max_retries}次请求')
            await asyncio.sleep(2**i)
        print(f'{message}请求未发送成功')
        return {'error': 'Failed after retries', 'message': message}
async def _main(num):
    start = time.time()
    messages = [f'{i}加100等于多少，只回答最后的结果即可' for i in range(num)]
    tasks = [_get_response(i) for i in messages]
    results = await asyncio.gather(*tasks,return_exceptions=True)
    # 记录失败的请求
    failed_requests = [messages[i] for i, result in enumerate(results) if 'error' in result]

    # 对失败的请求进行再次处理
    while failed_requests:
        print(f"Retrying {len(failed_requests)} failed requests...")
        retry_tasks = [_get_response(msg) for msg in failed_requests]
        retry_results = await asyncio.gather(*retry_tasks,return_exceptions=True)#出现异常后不会停止

        # 更新成功和失败的请求
        failed_requests = [failed_requests[i] for i, result in enumerate(retry_results) if 'error' in result]
        results.extend(retry_results)
    for result in results:
        print(result)

    success_count = len([res for res in results if 'error' not in res])
    print(f"成功的请求数量: {success_count}/{num}")
    end = time.time()
    print(f'{num}次请求用{semaphore}个最大并发数下耗费总时间为{end-start}s')

asyncio.run(_main(2000))