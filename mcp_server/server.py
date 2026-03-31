from tools.classify_intent import run_tool as run_classify_intent
from tools.detect_missing_pieces import run_tool as run_detect_missing_pieces
from tools.structure_instruction import run_tool as run_structure_instruction
from tools.optimize_prompt import run_tool as run_optimize_prompt
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PromptSense MCP Server")


@mcp.tool()
def classify_intent(input_data: dict) -> dict:
    return run_classify_intent(input_data)


@mcp.tool()
def detect_missing_pieces(input_data: dict) -> dict:
    return run_detect_missing_pieces(input_data)


@mcp.tool()
def structure_instruction(input_data: dict) -> dict:
    return run_structure_instruction(input_data)


@mcp.tool()
def optimize_prompt(input_data: dict) -> dict:
    return run_optimize_prompt(input_data)


if __name__ == "__main__":
    mcp.run()