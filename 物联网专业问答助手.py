from openai import OpenAI

# 全局配置
API_KEY = "输入你的通义千问api的key"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-turbo"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def llm_ask(user_prompt, system_prompt="你是专业的物联网技术助手"):
    """
    封装通用对话函数：传入问题和角色设定，返回回答，异常友好提示
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            temperature=0.2,
            messages=messages,
            timeout=15
        )
        return resp.choices[0].message.content #默认只返回 1 条回答，取下标0
    except Exception as e:
        return f"调用失败：{str(e)}"

def chat_assistant():
    """多轮对话主程序：带上下文、角色限定、退出逻辑、空输入校验"""
    system_rule = """
    你是专注物联网领域的技术助手，仅限回答嵌入式开发、传感器、单片机、Python开发相关问题。
    回答要求：简洁专业，分点说明核心要点；非相关问题直接回复「抱歉，我仅能解答物联网技术相关问题」；不知道的内容不要编造。
    """
    # 对话历史：保留system + 最近6轮对话，避免上下文超长
    history = [{"role": "system", "content": system_rule}]

    print("="*40)
    print("   物联网专业问答助手 V1.0")
    print("   输入 quit/exit 退出程序")
    print("="*40)

    while True:
        user_input = input("\n你：").strip()
        # 退出逻辑
        if user_input.lower() in ["quit", "exit", "退出"]:
            print("程序已退出，感谢使用")
            break
        # 空输入校验
        if not user_input:
            print("请输入有效问题")
            continue

        # 加入历史
        history.append({"role": "user", "content": user_input})
        # 调用模型
        answer = llm_ask(user_input, system_rule)
        print(f"\n助手：{answer}")
        # 回答加入历史
        history.append({"role": "assistant", "content": answer})

        # 裁剪历史，保留system+最近5轮，防止超长
        if len(history) > 12:
            history = [history[0]] + history[-10:]

if __name__ == "__main__":
    chat_assistant()