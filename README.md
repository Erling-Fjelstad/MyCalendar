# My Calendar

A modern calendar application built with **Streamlit**, **SQLite**, and **Python** with AI integration via **Claude Desktop**.  
Designed for personal use to efficiently manage tasks, lectures, and exercises with features like weekly repeats and visual timeline views.

## Features

- **Interactive Calendar** - Weekly and daily views with visual event timeline
- **Multiple Event Types** - Tasks, Lectures, and Exercises  
- **Weekly Repeats** - Automatically schedule recurring events
- **Full CRUD** - Create, read, update, and delete events
- **AI Integration** - Manage calendar through Claude desktop
- **Storage** - SQLite database

## Quick Start

### Prerequisites
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Claude Desktop](https://claude.ai/download) for MCP server integration (optional)

### Setup for the application

Clone the repository:
```bash
git clone https://github.com/Erling-Fjelstad/MyCalendar.git
cd MyCalendar
```

Run the streamlit application:
```bash
uv run streamlit run app.py
```

### Setup the mcp-server:

Open the Claude desktop config file for macOS/linux:
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```
or for Windows:
```bash
code $env:AppData\Claude\claude_desktop_config.json
```

Paste this into the config file for macOS/Linux:
```bash
{
  "mcpServers": {
    "myCalendar": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/MyCalendar",
        "run",
        "mcp_server.py"
      ]
    }
  }
}
```
or for Windows:
```bash
{
  "mcpServers": {
    "myCalendar": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\MyCalendar",
        "run",
        "mcp_server.py"
      ]
    }
  }
}
```

Now you can open Claude Desktop and use the available tools.


> [!WARNING]  
> This project is **under development** (work in progress).