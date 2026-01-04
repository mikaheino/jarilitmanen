# Plan and Progress

## Goal
Set up Snowflake MCP server and test the connection using curl commands. Create and manage Snowflake databases via MCP.

## New Project: Jari Litmanen ML Project
Create complete ML project solution in Snowflake and store all code in GitHub repository.

## Progress
- [x] Identified issue with curl command syntax
- [x] Fixed Authorization header format (colon should be inside quotes)
- [x] Created test script: test_snowflake_mcp.sh
- [x] Tested Snowflake MCP server connection - curl command works correctly
- [x] Resolved Snowflake network policy configuration issue
- [x] Successfully connected to Snowflake MCP server
- [x] Configured Cursor MCP server in mcp.json
- [x] Added Accept and Content-Type headers to fix SSE streaming error
- [x] Successfully created Snowflake database `FIFA2026` using MCP sql_exec_tool
- [x] Successfully dropped Snowflake database `FIFA2026` using MCP sql_exec_tool
- [x] Created Jari Litmanen ML project structure
- [x] Created LITMANEN database in Snowflake with RAW and FEATURES schemas
- [x] Loaded 58 records of career data into PLAYER_SEASON_DATA table
- [x] Created LITMANEN_FEATURES view with calculated ratios and season sorting
- [x] Created all project files (SQL scripts, Python scripts, requirements.txt, README.md)
- [x] Committed and pushed code to GitHub repository mikaheino/jarilitmanen

## Notes
- The curl command syntax is now correct - Authorization header fixed
- URL: `https://ZUEEMDQ-CONTAINER_SERVICES.snowflakecomputing.com/api/v2/databases/AGENT_GATEWAY/schemas/PUBLIC/mcp-servers/SQL_EXEC_SERVER`
- Bearer token provided
- **Status**: Connection successful! The MCP server responded with available tools
- **Available Tool**: `sql_exec_tool` - A tool to execute SQL queries against the connected Snowflake database

## Snowflake MCP Server Limitations
**Important**: Snowflake managed MCP server only supports **non-streaming responses**. It does NOT support:
- Server-Sent Events (SSE) streaming
- Resources, prompts, roots, notifications
- Version negotiations, life cycle phases, and sampling

**SSE Error Explanation**: 
- The "Failed to open SSE stream: Not Acceptable" error is **expected behavior**
- Cursor tries SSE streaming first (default), gets rejected, then automatically falls back to non-streaming HTTP
- This is a harmless warning - functionality works correctly via HTTP fallback
- No configuration changes needed - this is a Snowflake limitation, not a configuration issue
