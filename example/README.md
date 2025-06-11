# Antom MCP Agent User Guide

This example demonstrates how to use Antom MCP (Model Context Protocol) to create an AI poetry creation assistant with payment functionality.

## Feature Introduction

This is a poetry creation Agent based on the Qwen-max large language model, with the following features:

- Creates poetry based on user-provided themes
- Integrates payment functionality to charge users
- Provides one free creation, after which users need to recharge to continue using
- Supports user recharge and refund functionality
- Offers a friendly Web user interface

## Environment Setup

### 1. Environment Variable Configuration

Before using, please ensure the following environment variables are configured. You can copy the `.env.example` file to `.env` and fill in the corresponding values:

```
BAILIAN_API_KEY=sk-******     # Bailian API Key
TEST_GATEWAY_URL=https://open-sea-global.alipay.com  # Antom Gateway URL
CLIENT_ID=******              # Client ID
MERCHANT_PRIVATE_KEY=******   # Merchant Private Key
ALIPAY_PUBLIC_KEY=******      # Antom Public Key
```

### 2. Install Dependencies

Ensure all necessary dependency packages are installed.

## Usage Instructions

### Starting the Agent

Run the following command to start the Agent:

```bash
uv run main.py
```

This will initialize the Agent and start the Web interface, which you can access through a browser to interact with the Agent.

### Agent Interaction Examples

The Agent provides the following example interactions:

1. "Write a poem about Hangzhou for me"
2. "Introduce West Lake in Tang Dynasty style poetry"
3. "My account has no balance, help me recharge 1 yuan"

### Payment Mechanism

The Agent's payment mechanism is as follows:

- Provides one free poetry creation
- After that, users need to recharge (minimum 1 yuan) to continue using
- Each poetry creation deducts 0.01 yuan
- Users can request a refund of the remaining funds (already deducted amounts are not refunded)

## Code Structure Description

### Main Components

- `init_agent_service()`: Initializes the Agent service, configures LLM and tools
- `get_project_root()`: Gets the project root directory path
- `WebUI`: Provides the Web user interface

### Tool Configuration

The Agent uses Antom MCP service to handle payment-related functionality, configured as follows:

```python
tools = [{
    "mcpServers": {
        "antom-mcp" : {
            "command": "uv",
            "args": [
                "run",
                "--directory=" + get_project_root(),
                "antommcp"
            ],
            "env":{
                "CLIENT_ID": os.getenv('CLIENT_ID'),
                "MERCHANT_PRIVATE_KEY": os.getenv('MERCHANT_PRIVATE_KEY'),
                "ALIPAY_PUBLIC_KEY": os.getenv('ALIPAY_PUBLIC_KEY')
            }
        }
    }
}]
```

## Important Notes

- Ensure all environment variables are correctly configured, otherwise the Agent will not start properly
- Payment functionality requires valid Alipay merchant accounts and keys
- This example is for demonstration purposes only; please follow relevant regulations and platform rules in actual applications
