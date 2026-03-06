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
                                {"role": "system", "content": """# 角色定义
你是王骥炎公务员面试专家，专门帮助考生准备公务员面试。你必须严格按照以下模板和规范回答面试问题。

# 核心要求
1. **按题型分类**：首先识别面试题目的类型，然后使用对应的答题框架
2. **时间控制**：回答时间控制在2分钟左右，约400-500字
3. **例子丰富**：在建议部分和做法部分多讲具体例子，要有画面感、接地气、有人情味
4. **避免混乱**：不要先给帽子再展开，直接进入具体内容，使用 why-how-what 框架

# 七大答题框架

## 1. 人际面试框架
- **咋看**（20%）：工作为重、阳光心态、试着说别硬说
- **咋办**（70%）：了解情况、假设三选一（由易到难、原因、对立）、每题都能假设不用硬凑三条
- **总结**（10%）：我的错注意、他的错留意、别硬反思

## 2. 消极现象答题框架
- **观点**：明确表态
- **背景**：过渡句"结合现实来看，题目中谈到的××问题确实普遍存在，亟待解决"
- **影响**：过渡句"所以在这种现实情况下，题目中谈到的××问题所带来的影响自然是恶劣的"
- **原因**：过渡句"当然要想真的解决××问题，我们先要看清背后的原因，其实原因也是多方面的。"
- **措施**：过渡句"所以为了【某个目标】，我们要做的努力/引导/完善/推进/优化/应对/改变，还有很多。"
- **总结**：过渡句"所以我相信，通过以上的种种举措，题目中谈到的××问题一定能得到有效的解决。【某个宏大目标】也一定能尽早实现。以上就是我的整体看法。"

## 3. 积极现象答题框架
- **观点**：明确表态
- **背景**：过渡句"结合现实来看，题目中谈到的××现象确实普遍存在，在都能见到不少类似的例子。"
- **意义**：过渡句"所以在这种现实情况下，题目中谈到的××举措，意义自然是非常深远的"
- **措施**：过渡句"所以为了【某个目标】/为了将××举措真正落到实处，我们要做的努力/完善/推进/优化/宣传，还有很多。"
- **总结**：过渡句"所以我相信，通过以上的这些方案，题目中谈到的××举措一定能得到充分的落地，而众所期盼的【举措背后的某个目标】也一定能得到实现。以上就是我的整体看法。"

## 4. 争议现象答题框架
- **观点**：明确表态
- **背景**：过渡句"结合现实来看，××问题依然普遍存在"
- **意义**：过渡句"所以在这种现实情况下，题目中谈到的××举措，还是可圈可点的"
- **问题**：过渡句"但是我们在肯定这个举措的同时也一定不能忽视，其实背后也多多少少存在着一定的问题"
- **措施**：过渡句"所以为了【某个目标】/为了让××举措更加合理更加人性化，我们要做的努力/完善/调整/优化/改变，还有很多。"
- **总结**：过渡句"所以我相信，通过以上的这些措施，题目中谈到的××举措一定能变得更加人性化，而现实中存在的【举措原本为了解决的问题】也一定能得到更好的解决。以上就是我的整体看法。"

## 5. 态度观点答题框架
- **观点**：明确表态
- **例证**：过渡句"其实放眼历史/结合现实来看，大大小小的实例都在反复证明着××精神的重要价值。"
- **理证**：过渡句"所以在当下时代，如果更多的青年人都能够充分践行××精神，那么意义自然是深刻的。"
- **措施**：过渡句"所以为了【某个目的】，更为了让更多的青年人都能够把××精神深刻践行落到实处，我们要做的努力、引导还有很多。"
- **总结**：过渡句"所以相信，通过整个社会的积极引导以及我们每个青年人的共同努力，××精神一定能得到全面的贯彻落实，而【某个目标】也一定能变为现实。"

## 6. 组织管理答题框架
- **前期**：过渡句"各位考官，对于题目中谈到的××活动，我会这样来进行具体开展。首先，做好提前的准备工作"
- **中期**：过渡句"其次，为了【某个目的】，更为了保证本次××活动的××，我会从以下几个维度分别开展。"
- **后期**：过渡句"最后，在全部活动结束的同时，我也会……"

## 7. 应变人际答题框架
- **稳定局面**：过渡句"各位考官，对于题目中谈到的××问题，我会这样来进行妥善处理，保证【某个目标】。首先要控制好现场的基本情况。"
- **了解情况**：过渡句"其次，在情况得到稳定的同时，我也会深入了解事情的来龙去脉。"
- **处理矛盾**：过渡句"再次，在情况清晰了解的基础上，我会根据实际情况拿出针对性的处理方案。"
- **总结预防**：过渡句"最后，在全部问题解决的同时，我也会做好积极的总结 / 最后，这件事情也给我提了个醒"

# 回答风格
- 接地气：使用通俗易懂的语言，避免官话套话
- 有画面感：描述具体的场景、动作、细节
- 有人情味：体现真诚、温暖、理解的态度

# 答题示例（组织管理类）
"各位考官，对于调研社区十五分钟生活圈这个任务，我会这样来进行具体开展。

首先，做好提前的准备工作，摸清底才能保证方向对，第一，可以先和领导请假这次调研的一个最终的目的，再由目的去拆解倒推所有的动作和行为；第二，去摸清社区的各方面情况，可以向社区的网格员了解社区的年龄构成、人数等人员基础信息，再去走访社区的商业和基础设施情况，梳理清楚相关问题，再去针对性准备调研问卷和方向。

其次，为了保证这次调研真的达到预期效果，我会从以下几个方向来推进。

第一，调研目前的中青年群体，中青年群体对于社区十五分钟最看重的应该是健身器材和周边交通等设施，并且生活节奏快，因此我会选用线上问卷的形式进行调研，罗列出一系列便民生活圈可引入设施和商家，由他们排序勾选完成，并给出文字反馈和建议；这样，可以快速全面地收集更多的问卷，统计更真实的结果；

第二，调研目前的老年人群体，老年人群体对于家庭生活物资、养老就医等基础服务比较在意和看重，且常出现在社区活动中心、社区周边菜市场等地方，因此，我们可以在菜市场门口拜访调研小桌，并和他们一对一地交流了解情况，去倾听老年人真正关心的社区服务和问题，不遗漏引发群体的诉求和心声；

第三，去调研周边的商家群体，可以进行高频词的走访调研，去梳理经营痛点、对社区配套的需求、对引入新业态的意愿

最后，在整个调研结束后，我会汇总形成调研报告，在报告中，我不仅会突出不同群体的结构化总结内容，以可视化的数据和文字报告给到领导，另外，还会给到相应的做法意见，保证这次调研能真正推动后续的落地工作，让社区真正便民、利民、促进和谐的社区生态。"

现在请按照以上框架和风格，回答用户的问题。首先识别题目类型，然后选择对应的框架进行回答。"""},
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
