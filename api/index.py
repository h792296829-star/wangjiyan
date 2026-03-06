from http.server import BaseHTTPRequestHandler
import json
import os


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 返回前端页面
        if self.path == '/' or self.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>公务员培训助手</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 800px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
            font-size: 14px;
        }

        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }

        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            line-height: 1.6;
            word-wrap: break-word;
        }

        .message.assistant .message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 4px;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message-sender {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }

        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }

        .input-container {
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }

        #messageInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 24px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s;
            resize: none;
            min-height: 48px;
            max-height: 120px;
        }

        #messageInput:focus {
            border-color: #667eea;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 24px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-send:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .btn-mic {
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
        }

        .btn-mic:hover {
            background: #667eea;
            color: white;
        }

        .btn-mic.listening {
            background: #ef4444;
            border-color: #ef4444;
            color: white;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #666;
        }

        .loading.show {
            display: block;
        }

        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #667eea;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-left: 10px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .status {
            padding: 10px 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
            background: #f8f9fa;
        }

        .error {
            color: #ef4444;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 公务员培训助手</h1>
            <p>支持语音输入，智能解答公务员考试相关问题</p>
        </div>

        <div class="chat-container" id="chatContainer">
            <div class="message assistant">
                <div>
                    <div class="message-sender">AI 助手</div>
                    <div class="message-content">
                        你好！我是你的公务员培训助手。你可以通过文字或语音向我提问，我会尽力为你解答公务员考试相关的问题。请问有什么我可以帮助你的？
                    </div>
                </div>
            </div>
            <div class="loading" id="loading">
                正在思考中
            </div>
        </div>

        <div class="status" id="status">
            点击麦克风图标开始语音输入
        </div>

        <div class="input-area">
            <div class="input-container">
                <button class="btn btn-mic" id="micBtn" onclick="toggleSpeech()">
                    🎤 语音
                </button>
                <textarea 
                    id="messageInput" 
                    placeholder="输入你的问题..." 
                    rows="1"
                    onkeydown="handleKeyDown(event)"
                ></textarea>
                <button class="btn btn-send" onclick="sendMessage()">
                    发送
                </button>
            </div>
        </div>
    </div>

    <script>
        const messageInput = document.getElementById('messageInput');
        const chatContainer = document.getElementById('chatContainer');
        const loading = document.getElementById('loading');
        const micBtn = document.getElementById('micBtn');
        const status = document.getElementById('status');
        
        let isListening = false;
        let recognition = null;

        // 检查浏览器是否支持语音识别
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'zh-CN';
            recognition.continuous = false;
            recognition.interimResults = true;

            recognition.onstart = function() {
                isListening = true;
                micBtn.classList.add('listening');
                micBtn.innerHTML = '⏹ 停止';
                status.textContent = '正在听...';
            };

            recognition.onend = function() {
                isListening = false;
                micBtn.classList.remove('listening');
                micBtn.innerHTML = '🎤 语音';
                status.textContent = '点击麦克风图标开始语音输入';
            };

            recognition.onresult = function(event) {
                let finalTranscript = '';
                let interimTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }

                if (finalTranscript) {
                    messageInput.value = finalTranscript;
                    status.textContent = '已识别: ' + finalTranscript;
                } else if (interimTranscript) {
                    status.textContent = '正在识别: ' + interimTranscript;
                }
            };

            recognition.onerror = function(event) {
                status.textContent = '语音识别错误: ' + event.error;
                status.classList.add('error');
                isListening = false;
                micBtn.classList.remove('listening');
                micBtn.innerHTML = '🎤 语音';
            };
        } else {
            micBtn.style.display = 'none';
            status.textContent = '您的浏览器不支持语音输入功能';
            status.classList.add('error');
        }

        function toggleSpeech() {
            if (!recognition) {
                alert('您的浏览器不支持语音输入功能');
                return;
            }

            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }

        function handleKeyDown(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        function addMessage(content, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user' : 'assistant');
            messageDiv.innerHTML = `
                <div>
                    <div class="message-sender">${isUser ? '你' : 'AI 助手'}</div>
                    <div class="message-content">${content}</div>
                </div>
            `;
            chatContainer.insertBefore(messageDiv, loading);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';
            loading.classList.add('show');
            status.textContent = '正在思考中...';
            status.classList.remove('error');

            fetch('/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                loading.classList.remove('show');
                if (data.reply) {
                    addMessage(data.reply, false);
                    status.textContent = 'AI 助手已回复';
                } else {
                    addMessage('抱歉，我遇到了一些问题，请稍后再试。', false);
                    status.textContent = '发生错误';
                    status.classList.add('error');
                }
            })
            .catch(error => {
                loading.classList.remove('show');
                addMessage('抱歉，网络连接出现问题，请检查网络后重试。', false);
                status.textContent = '网络错误';
                status.classList.add('error');
                console.error('Error:', error);
            });
        }

        // 自动调整输入框高度
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode())
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "API is running",
                "endpoints": {
                    "GET /": "返回前端页面",
                    "POST /api": "AI 对话接口"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not Found"}
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        if self.path == '/api':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                message = data.get('message', '')
                
                # 调用 DeepSeek API
                api_key = os.environ.get('COZE_WORKLOAD_IDENTITY_API_KEY')
                base_url = os.environ.get('COZE_INTEGRATION_MODEL_BASE_URL', 'https://api.deepseek.com')
                
                if not api_key:
                    reply = "错误：未配置 API Key，请在环境变量中设置 COZE_WORKLOAD_IDENTITY_API_KEY"
                else:
                    import http.client
                    import json
                    
                    try:
                        # 使用 DeepSeek API
                        headers = {
                            'Authorization': f'Bearer {api_key}',
                            'Content-Type': 'application/json'
                        }
                        
                        body = json.dumps({
                            "model": "deepseek-chat",
                            "messages": [
                                {"role": "system", "content": "你是一个专业的公务员培训助手，擅长解答公务员考试相关的问题，包括申论、行测、面试等内容。请用清晰、准确、接地气的语言回答问题。"},
                                {"role": "user", "content": message}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 2000
                        })
                        
                        # 解析 base_url
                        url_parts = base_url.replace('https://', '').split('/')
                        host = url_parts[0]
                        path = '/' + '/'.join(url_parts[1:]) if len(url_parts) > 1 else '/v1/chat/completions'
                        
                        conn = http.client.HTTPSConnection(host)
                        conn.request('POST', path, body, headers)
                        response = conn.getresponse()
                        data = response.read().decode()
                        
                        if response.status == 200:
                            result = json.loads(data)
                            reply = result['choices'][0]['message']['content']
                        else:
                            reply = f"API 错误 (HTTP {response.status}): {data}"
                        
                        conn.close()
                    except Exception as e:
                        reply = f"调用 AI 服务时出错: {str(e)}"
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"reply": reply}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not Found"}
            self.wfile.write(json.dumps(response).encode())
