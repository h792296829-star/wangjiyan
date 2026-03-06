# Vercel Serverless Function Entry Point
import os
import sys

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# 设置环境变量
os.environ['COZE_WORKSPACE_PATH'] = project_root

# 导入 ASGI 应用
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request

async def homepage(request: Request):
    """返回主页"""
    try:
        html_path = os.path.join(project_root, 'assets', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
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
        from langchain_core.messages import HumanMessage

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
        import traceback
        error_detail = traceback.format_exc()
        return JSONResponse({
            'error': str(e),
            'detail': error_detail,
            'status': 'error'
        }, status_code=500)

# 创建 Starlette 应用
app = Starlette(
    debug=False,
    routes=[
        Route('/', homepage),
        Route('/stream_run', stream_run, methods=['POST']),
        Mount('/static', StaticFiles(directory=os.path.join(project_root, 'assets')), name='static'),
    ]
)

# Vercel ASGI handler
asgi_handler = app
