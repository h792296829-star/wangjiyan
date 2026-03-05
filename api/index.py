# Vercel Serverless Function Entry Point (ASGI)
import os
import sys
import json
from typing import Dict, Any

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request

# 设置环境变量
os.environ['COZE_WORKSPACE_PATH'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

async def homepage(request: Request):
    """返回主页"""
    try:
        with open('assets/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, media_type='text/html; charset=utf-8')
    except FileNotFoundError:
        return JSONResponse({'error': 'Homepage not found'}, status_code=404)

async def stream_run(request: Request):
    """处理流式运行请求"""
    try:
        data = await request.json()

        # 导入并运行 Agent
        from src.agents.agent import build_agent
        from langchain_core.messages import HumanMessage, AIMessage

        # 构建 Agent
        agent = build_agent()

        # 获取用户消息
        messages_input = data.get('messages', [])
        if isinstance(messages_input, str):
            messages_input = [HumanMessage(content=messages_input)]
        elif not messages_input:
            messages_input = []

        # 调用 Agent
        result = await agent.ainvoke({'messages': messages_input})

        # 提取回复内容
        response_content = ""
        if isinstance(result, dict):
            messages = result.get('messages', [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                    if isinstance(content, str):
                        response_content = content
                    elif isinstance(content, list):
                        response_content = str(content)
                elif isinstance(last_message, dict):
                    response_content = last_message.get('content', '')
        elif hasattr(result, 'content'):
            content = result.content
            if isinstance(content, str):
                response_content = content
            elif isinstance(content, list):
                response_content = str(content)

        return JSONResponse({
            'content': response_content,
            'status': 'success'
        })

    except Exception as e:
        return JSONResponse({
            'error': str(e),
            'status': 'error'
        }, status_code=500)

# 创建 Starlette 应用
app = Starlette(
    debug=True,
    routes=[
        Route('/', homepage),
        Route('/stream_run', stream_run, methods=['POST']),
        Mount('/static', StaticFiles(directory='assets'), name='static'),
    ]
)
