import asyncio
import json
from typing import Any, Dict

from langchain_mcp_adapters.client import MultiServerMCPClient

# Load MCP configuration
DEFAULT_MCP_CONFIG = {"mcpServers": {}}


# MCP configuration is stored in mcp_config.json file
def load_mcp_config() -> Dict[str, Any]:
    try:
        with open("mcp_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config["mcpServers"]
    except FileNotFoundError:
        return DEFAULT_MCP_CONFIG


# Clean up MCP client
async def cleanup_mcp_client(client=None):
    """MCP 클라이언트를 정리합니다."""
    if client is not None:
        try:
            # langchain-mcp-adapters 0.1.0부터는 context manager를 사용하지 않습니다
            # 클라이언트는 자동으로 정리됩니다
            print("MCP client cleanup initiated.")
        except Exception as e:
            print(f"Error occurred while cleaning up MCP client: {str(e)}")


# Initialize MCP client
async def initialize_mcp_client():
    """MCP 클라이언트를 초기화하고 사용 가능한 도구를 반환합니다."""
    mcp_config = load_mcp_config()

    # 서버별로 개별 초기화를 시도하고 성공한 것만 사용
    working_servers = {}
    failed_servers = []

    for server_name, server_config in mcp_config.items():
        try:
            print(f"Trying to initialize server: {server_name}...")
            # 개별 서버로 클라이언트 생성
            temp_client = MultiServerMCPClient({server_name: server_config})
            # 도구 로드 시도
            await temp_client.get_tools()
            working_servers[server_name] = server_config
            print(f"[SUCCESS] Server '{server_name}' initialized successfully")
        except Exception as e:
            failed_servers.append(server_name)
            print(
                f"[FAILED] Server '{server_name}' failed to initialize: {str(e)[:100]}"
            )

    if not working_servers:
        raise Exception("No MCP servers could be initialized successfully")

    if failed_servers:
        print(f"\nWarning: {len(failed_servers)} server(s) failed: {', '.join(failed_servers)}")

    # 성공한 서버들로만 최종 클라이언트 생성
    try:
        client = MultiServerMCPClient(working_servers)
        tools = await client.get_tools()
        return client, tools
    except Exception as e:
        print(f"Error occurred while initializing MCP client: {str(e)}")
        raise


# Test MCP tool calls
async def test_mcp_tool(mcp_tools):
    try:
        # Test calls
        for tool in mcp_tools:
            print(f"[Tool] {tool.name}")
    except Exception as e:
        print(f"Error occurred during test call: {str(e)}")
