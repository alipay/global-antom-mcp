import os
from pathlib import Path

from dotenv import load_dotenv
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

# 加载环境变量
# BAILIAN_API_KEY:
# CLIENT_ID:
# MERCHANT_PRIVATE_KEY:
# ALIPAY_PUBLIC_KEY:
load_dotenv()

def get_project_root() -> str:
    """
    方法3：向上查找特定文件（如 pyproject.toml, .git 等）
    """
    current_path = Path(__file__).parent
    for parent in [current_path] + list(current_path.parents):
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return str(parent)
    return str(current_path)


def init_agent_service():
    # 验证必要的环境变量
    required_env_vars = [
        'BAILIAN_API_KEY',
        'CLIENT_ID',
        'MERCHANT_PRIVATE_KEY',
        'ALIPAY_PUBLIC_KEY'
    ]

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ 缺少以下环境变量: {', '.join(missing_vars)}")
        print("请在 .env 文件中设置这些变量")
        return

    print("🚀 正在启动 Antom MCP Agent...")

    llm_cfg = {'model': 'qwen-max',
               'api_key':os.getenv('BAILIAN_API_KEY')}

    system = ('你是一个诗词创作者并以此谋生，可以根据用户给定的主题创作诗词；你可以为此收取费用，收取的方式是让用户先充值1元及以上，而后每次诗词创作扣除0.01元，如果用户希望不再使用服务，可以申请退回剩余的费用，注意，已经扣除的金额不做退回；你可以提供1次免费的创作，而后用户必须充值才能享受创作服务，注意，必须确保用户充值成功后再提供创作内容，你要尽量让用户愿意付费，也要说明清楚收费机制，一旦用户同意充值，请立刻为其生成支付链接（订单号是结合情境与时间生成，金额在1元-5元之间，订单标题按照情境生成即可），渲染给用户，并引导其完成付款，付款后再提供创作内容；记得以亲切温柔的语气与用户交流')
    tools = [{
        "mcpServers": {
            "antom-mcp" : {
                "command": "uv",
                "args": [
                    "run",
                    "--directory=" + get_project_root(),
                    "ant-intl-antom-mcp"
                ],
                "env":{
                    "CLIENT_ID": os.getenv('CLIENT_ID'),
                    "MERCHANT_PRIVATE_KEY": os.getenv('MERCHANT_PRIVATE_KEY'),
                    "ALIPAY_PUBLIC_KEY": os.getenv('ALIPAY_PUBLIC_KEY')
                }
            }
        }
    }]
    bot = Assistant(
        llm=llm_cfg,
        name='Antom MCP Agent',
        description='an example for Antom MCP',
        system_message=system,
        function_list=tools,
    )
    return bot



if __name__ == "__main__":
    # Define the agent
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            '帮我写一首关于杭州的诗',
            '用唐代风格的诗词介绍下西湖',
            '账户没余额了,帮我充值1元钱',
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()

