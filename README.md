# Antom MCP Server

A Model Context Protocol (MCP) compatible server that integrates Ant International's Antom payment APIs, enabling AI assistants to handle payment and refund operations seamlessly.

## Overview

The Antom MCP Server wraps Ant International's Antom payment APIs into standardized MCP tools, allowing AI assistants to securely process payment-related operations during conversations. With this server, you can create payment sessions, query transaction status, handle refunds, and more directly through AI interactions.

## Features

### 💳 Payment Operations
- **Create Payment Session** (`create_payment_session`): Generate payment sessions for client-side SDK integration
- **Query Payment Details** (`query_payment_detail`): Retrieve transaction status and information for submitted payment requests
- **Cancel Payment** (`cancel_payment`): Cancel payments when results are not returned within expected timeframes

### 💰 Refund Operations
- **Create Refund** (`create_refund`): Initiate full or partial refunds against successful payments
- **Query Refund Details** (`query_refund_detail`): Check refund status for previously submitted refund requests


## Prerequisites

Before using the Antom MCP Server, ensure you have:

- **Python 3.11 or higher**
- **uv** (recommended package manager) or **pip**
- **Valid Antom Merchant Account** with:
  - Merchant Client ID (CLIENT_ID)
  - Merchant RSA Private Key (MERCHANT_PRIVATE_KEY)
  - Alipay RSA Public Key (ALIPAY_PUBLIC_KEY)
  - Payment Redirect Return URL (PAYMENT_REDIRECT_URL)
  - Payment Notification Callback URL (PAYMENT_NOTIFY_URL)


## Quick Start

### 1. Installation

#### Direct Usage with uvx (Recommended)
```bash
uvx ant-intl-antom-mcp
```

#### Install from Source

```shell
git clone https://github.com/alipay/global-antom-mcp.git
cd global-antom-mcp
uv install
```

### 2. MCP Client Configuration
Add the following configuration to your MCP client:

```json
{
  "mcpServers": {
    "antom-mcp-server": {
      "command": "uvx",
      "args": ["ant-intl-antom-mcp"],
      "env": {
        "GATEWAY_URL": "https://open-sea-global.alipay.com",
        "CLIENT_ID": "your_client_id_here",
        "MERCHANT_PRIVATE_KEY": "your_merchant_private_key_here",
        "ALIPAY_PUBLIC_KEY": "your_alipay_public_key_here",
        "PAYMENT_REDIRECT_URL": "/",
        "PAYMENT_NOTIFY_URL": "https://your-domain.com/payment/notify"
      }
    }
  }
}
```

### 3. Environment Variables

| Variable | Required | Description                                                            |
| --- |----------|------------------------------------------------------------------------|
| `GATEWAY_URL` | ❌        | Antom API gateway URL (defaults to https://open-sea-global.alipay.com) |
| `CLIENT_ID` | ✅        | Merchant client ID for identity verification                           |
| `MERCHANT_PRIVATE_KEY` | ✅        | Merchant RSA private key for request signing                           |
| `ALIPAY_PUBLIC_KEY` | ✅        | Alipay RSA public key for response verification                        |
| `PAYMENT_REDIRECT_URL` | ❌        | The user is redirected to after the payment is completed               |
| `PAYMENT_NOTIFY_URL` | ❌        | Payment result notification callback URL                               |


## Integration Example
Here's how you can integrate the Antom MCP Server with your AI agent (using QwenAgent as an example):

```python
import os
from qwen_agent.agents import Assistant

# Configure the MCP server as a tool
tools = [{
    "mcpServers": {
        "antom-mcp-server": {
            "command": "uvx",
            "args": ["ant-intl-antom-mcp"],
            "env": {
                "CLIENT_ID": os.getenv('CLIENT_ID'),
                "MERCHANT_PRIVATE_KEY": os.getenv('MERCHANT_PRIVATE_KEY'),
                "ALIPAY_PUBLIC_KEY": os.getenv('ALIPAY_PUBLIC_KEY'),
                "GATEWAY_URL": "https://open-sea-global.alipay.com",
                "PAYMENT_REDIRECT_URL": "/",
                "PAYMENT_NOTIFY_URL": "https://your-domain.com/notify"
            }
        }
    }
}]

# Create your AI assistant with payment capabilities
bot = Assistant(
    llm={'model': 'qwen-max', 'api_key': 'your-api-key'},
    function_list=tools,
    system_message="You are a helpful assistant with payment processing capabilities."
)
```

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Model Context Protocol](https://modelcontextprotocol.io/) for the standard
- [Antom Integration](https://docs.antom.com/ac/cashierpay/quick_start?platform=Web&client=HTML&server=Python&integration_type=CKP-HOSTED) for the Antom payment platform
