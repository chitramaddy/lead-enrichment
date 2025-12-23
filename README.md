# Lead Enrichment Multi-Agent Application

A terminal-based multi-agent application built with Agno that enriches lead information using specialized AI agents.

## Overview

This application uses a coordinator agent to manage three specialized agents that gather different types of information about leads:

1. **Company Information Agent**: Gathers company-level data including company information, recent news, announcements, and key competitors
2. **Individual Information Agent**: Finds individual details like email, phone, title, and social media profiles
3. **Recent Activity Agent**: Discovers recent posts, articles, mentions, and identifies pain points or challenges
4. **Summarizer Agent**: Synthesizes all collected information into a comprehensive summary

## Features

- Terminal-based interface for easy interaction
- Multi-agent coordination using Agno framework
- Structured lead enrichment workflow
- Comprehensive summary generation

## Prerequisites

- Python 3.8 or higher
- Anthropic API key
- Firecrawl API key (optional, for web scraping features)

## Installation

1. Clone or navigate to the project directory:

```bash
cd lead-entrichment
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env.local` file in the project root with your API keys:

```bash
ANTHROPIC_API_KEY=your-anthropic-api-key-here
FIRECRAWL_API_KEY=your-firecrawl-api-key-here
```

**Note:**

- Get your Anthropic API key from the [Anthropic Console](https://console.anthropic.com/api-keys)
- Get your Firecrawl API key from [Firecrawl](https://firecrawl.dev) (optional, only needed for web scraping features)
- The `.env.local` file is already in `.gitignore` and won't be committed to version control

## Usage

Run the application:

```bash
python lead_enrichment.py
```

When prompted, enter your leads in the following format:

```
John Doe, Acme Corp
Jane Smith, Tech Solutions Inc
Bob Johnson, Global Industries
```

Press Enter twice or type 'done' when finished entering leads.

The application will:

1. Process each lead through the specialized agents
2. Gather company, individual, and activity information
3. Generate a comprehensive summary
4. Display the results in the terminal

## Current Status

Currently, the agents provide generic placeholder information as the actual tools (web scraping, search APIs, etc.) are not yet implemented. The structure is in place for easy integration of these tools in the future.

## Future Enhancements

- Integration of web scraping tools for company websites
- Integration of search APIs for finding public information
- Database storage for enriched leads
- Export functionality (CSV, JSON)
- Batch processing capabilities

## License

MIT
