"""
Lead Enrichment Multi-Agent Application

A terminal application that uses a coordinator agent to manage three specialized agents
for enriching lead information with company data, individual details, and recent activity.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from agno.team import Team
from agno.agent import Agent
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.duckduckgo import DuckDuckGoTools

# Load environment variables from .env.local file
env_path = Path(__file__).parent / '.env.local'
load_dotenv(env_path)


def get_leads_from_user():
    """Prompt user for a list of leads in the terminal."""
    print("\n" + "="*60)
    print("Lead Enrichment Application")
    print("="*60)
    print("\nPlease provide a list of leads to enrich.")
    print("Format: Name, Company (one per line, or comma-separated)")
    print("Example: John Doe, Acme Corp")
    print("Enter 'done' when finished, or press Enter twice to submit:\n")
    
    leads = []
    while True:
        line = input().strip()
        if line.lower() == 'done':
            break
        if not line:
            if leads:
                break
            continue
        leads.append(line)
    
    if not leads:
        print("\nNo leads provided. Exiting.")
        return None
    
    # Format leads for the agents
    leads_text = "\n".join([f"- {lead}" for lead in leads])
    return leads_text


def create_company_agent():
    """Create agent for company-level information."""
    return Agent(
        id="company-agent",
        name="Company Information Agent",
        model="anthropic:claude-sonnet-4-20250514",
        tools=[FirecrawlTools(enable_crawl=True, limit=5)],
        role="Find publicly available company-level information including company data, recent news and announcements and scrape company website data.",
        instructions="""
        You are responsible for gathering company-level information for leads.
        Your tasks include:
        1. Finding company data (size, industry, location, etc.)
        2. Researching recent news and announcements maximum of 3 news articles
        3. Scraping company website for additional context using the FirecrawlTools
        
        SOURCE ATTRIBUTION: If you find information from LinkedIn company pages, always note this in your response.
        For example: "Company Size: 500-1000 employees (source: LinkedIn)" or "Industry: Technology (source: LinkedIn)".
        This helps the summarizer agent properly attribute the information sources.
        
        IMPORTANT SEARCH STRATEGY:
        - Always start with simple, focused search queries WITHOUT special characters
        - Replace "&" with "and", avoid commas and other special characters in queries
        - Example: Use "JPMorgan Chase" instead of "JPMorgan Chase & Co"
        - If a search returns "No results found" or "Could not run function" error:
          * Try an even simpler query (e.g., just "Company Name" without additional words)
          * Remove special characters and use plain text only
        - Break complex queries into simpler parts (e.g., search "Company Name" separately from "Company Name news")
        
        5. Present accurately and concisely the information gathered, noting when search results were unavailable
        Format your response clearly with sections for each type of information.
        """
    )


def create_individual_agent():
    """Create agent for individual-level information."""
    return Agent(
        id="individual-agent",
        name="Individual Information Agent",
        model="anthropic:claude-sonnet-4-20250514",
        tools=[],
        role="Find information about individuals including email, phone, title, and other details from public sources and LinkedIn profiles.",
        instructions="""
        You are responsible for gathering individual-level information for leads.
        Your tasks include:
        1. Finding email addresses
        2. Finding phone numbers
        3. Identifying job titles and roles
        4. Finding information from public sources and LinkedIn profiles using BrightData MCP tools
        
        IMPORTANT: You have access to BrightData MCP server through the Model Context Protocol.
        Use the available BrightData MCP tools to search for LinkedIn profiles, email addresses, phone numbers,
        and other individual information. The MCP tools should be automatically available to you.
        
        SOURCE ATTRIBUTION: When you find information from LinkedIn profiles or pages, always note this in your response.
        For example: "Email: john.doe@company.com (source: LinkedIn)" or "Title: VP of Engineering at Acme Corp (source: LinkedIn)".
        This helps the summarizer agent properly attribute the information sources.
        
        IMPORTANT SEARCH STRATEGY:
        - Always start with simple, focused search queries WITHOUT special characters
        - Replace "&" with "and", avoid commas and other special characters in queries
        - If a search returns "No results found" or "Could not run function" error:
          * Try an even simpler query (e.g., just "Person Name" without additional words)
          * Remove special characters and use plain text only
        - Try variations: "Person Name", "Person Name Company", "Person Name email", "Person Name phone"
        - Break complex queries into simpler parts
        
        5. Present accurately and concisely the information gathered, noting when search results were unavailable
        Format your response clearly with sections for each type of information.
        """
    )


def create_activity_agent():
    """Create agent for recent activity and pain points."""
    return Agent(
        id="activity-agent",
        name="Recent Activity Agent",
        model="anthropic:claude-sonnet-4-20250514",
        tools=[],
        role="Find recent posts, articles, and mentions about individuals. Identify recent pain points or challenges mentioned publicly.",
        instructions="""
        You are responsible for gathering recent activity and insights about leads.
        Your tasks include:
        1. Finding recent posts and articles by or about the individual
        2. Identifying public mentions
        3. Extracting pain points or challenges mentioned
        4. Analyzing sentiment and key themes
        
        IMPORTANT SEARCH STRATEGY:
        - Always start with simple, focused search queries WITHOUT special characters
        - Replace "&" with "and", avoid commas and other special characters in queries
        - If a search returns "No results found" or "Could not run function" error:
          * Try an even simpler query (e.g., just "Person Name" without additional words)
          * Remove special characters and use plain text only
        - Try variations: "Person Name", "Person Name articles", "Person Name mentions", "Person Name Company"
        - Break complex queries into simpler parts
        - You have access to BrightData MCP server through the Model Context Protocol. Use the available BrightData MCP tools 
          to search for recent posts, articles, and mentions about individuals and identify recent pain points or challenges mentioned publicly.
        - Provide general insights based on industry trends and typical pain points when specific data is unavailable
        
        Format your response clearly with sections for each type of information, noting when search results were unavailable.
        """
    )


def create_summarizer_agent():
    """Create agent for summarizing all collected information."""
    return Agent(
        id="summarizer-agent",
        name="Summarizer Agent",
        model="anthropic:claude-sonnet-4-20250514",
        role="Synthesize and summarize all information collected from the three specialized agents into a comprehensive lead enrichment report.",
        instructions="""
        You are responsible for creating a comprehensive summary of all lead enrichment data.
        Your tasks include:
        1. Reviewing information from Company Information Agent
        2. Reviewing information from Individual Information Agent
        3. Reviewing information from Recent Activity Agent
        4. Synthesizing all information into a clear, structured summary
        5. Highlighting key insights and actionable information
        
        Make sure you format your summary with all of the following sections:
        - Executive Summary
        - Company Overview
        - Individual Profile (including email, phone, title, and other details)
        - Recent Activity & Insights
        - Key Opportunities & Pain Points
        - Recommendations
        
        IMPORTANT: When citing information sources, always include the source attribution:
        - If information comes from LinkedIn profiles or pages, explicitly mention "source: LinkedIn" 
        - For example: "John Doe is the VP of Engineering at Acme Corp (source: LinkedIn)"
        - Include source attribution for all individual profile information (email, phone, title, etc.) when it comes from LinkedIn
        - Include source attribution for company information when it comes from LinkedIn company pages
        """
    )


def create_enrichment_team():
    """Create the main enrichment team with all agents."""
    # Create specialized agents
    company_agent = create_company_agent()
    individual_agent = create_individual_agent()
    activity_agent = create_activity_agent()
    summarizer_agent = create_summarizer_agent()
    
    # Create the main team with coordinator
    team = Team(
        name="Lead Enrichment Team",
        members=[company_agent, individual_agent, activity_agent, summarizer_agent],
        model="anthropic:claude-sonnet-4-20250514",
        instructions="""
        You are the coordinator for a lead enrichment team. Your role is to:
        1. Receive a list of leads from the user
        2. Delegate tasks to specialized team members:
           - company-agent: Gather company-level information
           - individual-agent: Gather individual-level information
           - activity-agent: Gather recent activity and pain points
        3. Once all agents have completed their research, delegate to summarizer-agent
           to create a comprehensive summary
        4. Present the final summary to the user
        
        Always coordinate with all three research agents first, then pass their
        findings to the summarizer agent for final synthesis.
        """
    )
    
    return team


def main():
    """Main application entry point."""
    # Check if API key is loaded
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n" + "="*60)
        print("ERROR: ANTHROPIC_API_KEY not found!")
        print("="*60)
        print("\nPlease ensure your .env.local file exists and contains:")
        print("ANTHROPIC_API_KEY=your-api-key-here")
        print("\nThe .env.local file should be in the same directory as lead_enrichment.py")
        print("="*60 + "\n")
        return
    
    # Get leads from user
    leads = get_leads_from_user()
    if not leads:
        return
    
    # Create the enrichment team
    print("\n" + "="*60)
    print("Initializing Lead Enrichment Team...")
    print("="*60 + "\n")
    
    team = create_enrichment_team()
    
    # Create the enrichment request
    request = f"""
    Please enrich the following leads with comprehensive information:
    
    {leads}
    
    Coordinate with your team members to:
    1. Gather company-level information for each lead
    2. Gather individual-level information for each lead
    3. Gather recent activity and pain points for each lead
    4. Create a comprehensive summary of all findings
    
    Present the final summary in a clear, structured format.
    """
    
    # Run the team
    print("Processing leads...\n")
    print("="*60 + "\n")
    
    team.print_response(request, stream=True, show_members_responses=True)
    
    print("\n" + "="*60)
    print("Lead Enrichment Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

