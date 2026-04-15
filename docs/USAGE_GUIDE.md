# Sidekick Usage Guide

## 🎯 What Can Sidekick Do?

Your Sidekick is a **Worker-Evaluator multi-agent system** powered by Gemini 2.5 Flash with access to powerful tools. Here's what it can accomplish:

---

## 🛠️ Available Tools

### 1. **Web Browser** (Playwright)
- Navigate to websites
- Click elements
- Extract text and data
- Take screenshots
- Fill forms

### 2. **Web Search** (SerpAPI)
- Search Google for current information
- Get real-time data
- Find recent news and updates

### 3. **Wikipedia**
- Research topics
- Get factual information
- Access encyclopedic knowledge

### 4. **Python REPL**
- Execute Python code
- Perform calculations
- Data processing
- Generate visualizations (saved to files)

### 5. **File Management**
- Create files in `sandbox/`
- Read files
- Write reports
- Organize data

### 6. **Push Notifications** (Optional)
- Send completion alerts
- Notify on important events

---

## 💡 Best Use Cases

### 📊 Research & Reports
**Perfect for:**
- Market research (e.g., competitive landscape analysis)
- Competitive analysis
- Topic summaries
- Data gathering and synthesis

**Example Tasks:**
```
"Research the top 5 AI companies in Finland and create a summary report"

"Find the latest news about LangGraph and summarize the key developments"

"Compare the features of Gradio vs Streamlit and save to a markdown file"
```

**Success Criteria Examples:**
- "Create a markdown file with at least 5 companies, their descriptions, and websites"
- "Summary should be 3-5 paragraphs with sources cited"

---

### 🌐 Web Data Extraction
**Perfect for:**
- Scraping product information
- Monitoring websites
- Extracting structured data
- Checking prices or availability

**Example Tasks:**
```
"Go to example.com/products and extract all product names and prices"

"Navigate to GitHub trending repositories and list the top 10 Python projects"

"Check the weather forecast for Helsinki and save it to a file"
```

**Success Criteria Examples:**
- "Save a JSON file with product names and prices"
- "Create a table with repository names, stars, and descriptions"

---

### 🔢 Data Analysis & Calculations
**Perfect for:**
- Complex calculations
- Data processing
- Statistical analysis
- Code execution

**Example Tasks:**
```
"Calculate the compound interest for €10,000 at 5% over 10 years and show the yearly breakdown"

"Generate a Fibonacci sequence up to 100 and save it to a file"

"Analyze this dataset: [paste data] and calculate mean, median, and standard deviation"
```

**Success Criteria Examples:**
- "Show calculations step-by-step in a markdown file"
- "Include a Python code snippet that can be reused"

---

### 📝 Content Creation
**Perfect for:**
- Writing summaries
- Creating structured documents
- Formatting data
- Generating reports

**Example Tasks:**
```
"Create a README.md template for a Python project with best practices"

"Write a 5-paragraph blog post about multi-agent AI systems"

"Generate a weekly report template with sections for tasks, achievements, and blockers"
```

**Success Criteria Examples:**
- "Include code examples and proper markdown formatting"
- "Save as a .md file in the sandbox"

---

### 🔍 Fact-Checking & Verification
**Perfect for:**
- Verifying information
- Cross-referencing sources
- Getting current data
- Checking facts

**Example Tasks:**
```
Task: "Search for 'Python async best practices', read the top 3 articles, and create a summary"

"What is the current population of Helsinki? Use multiple sources"

"Check if LangGraph 1.0 has been released and what are the new features"
```

**Success Criteria Examples:**
- "Provide at least 2 sources for the information"
- "Include publication dates for all sources"

---

### 🤖 Automation Tasks
**Perfect for:**
- Multi-step workflows
- Combining multiple tools
- Scheduled information gathering
- Repetitive tasks

**Example Tasks:**
```
"Search for 'Python async best practices', read the top 3 articles, and create a summary"

"Find the latest Gemini API documentation, extract key features, and save to a file"

"Monitor example.com/status every hour and notify me if it changes" (with push notifications)
```

**Success Criteria Examples:**
- "Complete all steps and save final summary to summary.md"
- "Include timestamps for when each source was accessed"

---

## 🎨 How to Write Effective Prompts

### The Two-Part System

Sidekick uses a **two-field interface**:

1. **Task Field**: What you want done
2. **Success Criteria Field**: How you'll know it's done right

### Task Field Best Practices

**✅ Good:**
```
"Research the top 3 SaaS companies in Finland providing AI solutions"
```

**❌ Avoid:**
```
"Find some companies"
```

**Tips:**
- Be specific about what you want
- Include context if needed
- Mention output format (file, summary, list, etc.)
- Specify data sources if important

### Success Criteria Best Practices

**✅ Good:**
```
"Create a markdown file with company names, service descriptions, and contact info. Include at least 3 options."
```

**❌ Avoid:**
```
"Make it good"
```

**Tips:**
- Define the output format
- Specify minimum requirements (e.g., "at least 5 items")
- Mention quality expectations
- Include structure requirements

---

## 🚀 Power User Tips

### 1. **Chain Multiple Tools**
```
Task: "Search for 'LangGraph tutorial', navigate to the official docs, 
       extract the getting started guide, and save it as a markdown file"

Success Criteria: "File should include code examples and be properly formatted"
```

### 2. **Use Python for Complex Logic**
```
Task: "Calculate the ROI for a €50,000 investment with monthly returns 
       of €500 over 5 years, accounting for 2% annual inflation"

Success Criteria: "Show calculations in Python code and save both code 
                   and results to a file"
```

### 3. **Combine Search + Analysis**
```
Task: "Find the current price of Bitcoin, Ethereum, and Cardano, 
       then calculate which has grown the most in the last 24 hours"

Success Criteria: "Create a comparison table with prices and percentage changes"
```

### 4. **Iterative Research**
```
Task: "Research AI agent frameworks, compare LangGraph, CrewAI, and AutoGen, 
       then create a decision matrix for choosing one"

Success Criteria: "Include pros/cons for each and a recommendation based on 
                   ease of use, features, and community support"
```

### 5. **Structured Data Extraction**
```
Task: "Go to example.com/team, extract all team member names and roles, 
       and save as a CSV file"

Success Criteria: "CSV should have columns: Name, Role, and be properly formatted"
```

---

## ⚠️ Current Limitations

### What Sidekick CAN'T Do (Yet)

1. **No Long-Term Memory**: Each session is independent
2. **No Image Generation**: Can't create images (only text/data)
3. **No Audio/Video**: Can't process or create multimedia
4. **Sandbox Only**: File operations limited to `sandbox/` directory
5. **No External APIs**: Can't directly call arbitrary APIs (only built-in tools)
6. **No Email**: Can't send emails (use push notifications instead)

### Workarounds

- **Memory**: Save important info to files in sandbox for next session
- **Images**: Use Python to generate charts/graphs and save as files
- **APIs**: Use Python REPL to make API calls if needed
- **Email**: Use push notifications or save drafts to files

---

## 📋 Example Workflows

### Workflow 1: Daily News Digest
```
Task: "Search for today's top 5 tech news stories, summarize each in 2-3 sentences, 
       and save to daily_digest.md with timestamps"

Success Criteria: "File should include headlines, summaries, sources, and be 
                   dated with today's date"
```

### Workflow 2: Competitive Analysis
```
Task: "Research [Competitor Name], find their main products, pricing, and 
       recent news. Create a competitive analysis report"

Success Criteria: "Markdown report with sections: Overview, Products, Pricing, 
                   Recent Developments, and SWOT analysis"
```

### Workflow 3: Code Documentation
```
Task: "Search for Python asyncio best practices, extract the top 10 tips, 
       and create a cheat sheet with code examples"

Success Criteria: "Markdown file with each tip explained and a working code 
                   example for each"
```

### Workflow 4: Data Collection
```
Task: "Find the top 10 Python libraries for data science, get their GitHub 
       stars, last update date, and description"

Success Criteria: "Create a table sorted by stars with columns: Name, Stars, 
                   Last Update, Description, GitHub URL"
```

---

## 🎯 Success Criteria Templates

Copy and adapt these for your tasks:

### For Research Tasks:
```
"Create a markdown file with:
- At least [X] sources
- Summary of [Y] paragraphs
- Key findings in bullet points
- Sources cited with URLs"
```

### For Data Extraction:
```
"Save data as [format] with:
- Columns: [list columns]
- At least [X] rows
- Properly formatted and validated"
```

### For Analysis Tasks:
```
"Provide:
- Step-by-step calculations
- Final result clearly stated
- Code used (if applicable)
- Saved to [filename]"
```

### For Web Scraping:
```
"Extract and save:
- [Specific data points]
- In [format] format
- With [X] minimum items
- Include source URL and timestamp"
```

---

## 🔄 The Worker-Evaluator Loop

**How it works:**

1. **You submit**: Task + Success Criteria
2. **Worker executes**: Uses tools to complete task
3. **Evaluator checks**: Did it meet success criteria?
4. **If NO**: Worker tries again with feedback
5. **If YES**: Task complete!

**This means:**
- Sidekick will keep trying until success criteria are met
- Clear success criteria = faster completion
- Vague criteria = may loop unnecessarily

---

## 💪 Best Practices Summary

1. **Be Specific**: Clear tasks get better results
2. **Define Success**: Good criteria prevent loops
3. **Use Files**: Save outputs for later reference
4. **Combine Tools**: Don't limit to one tool per task
5. **Iterate**: Start simple, then add complexity
6. **Check Sandbox**: Review outputs in `sandbox/` folder
7. **Monitor Console**: Watch for errors or tool usage
8. **Save Templates**: Reuse successful prompts

---

## 🎓 Learning Curve

### Beginner Tasks (Start Here)
- Simple searches and summaries
- Basic calculations
- Single-page web scraping
- File creation

### Intermediate Tasks
- Multi-source research
- Data analysis with Python
- Multi-step web navigation
- Structured reports

### Advanced Tasks
- Complex workflows combining all tools
- Iterative research with refinement
- Large-scale data extraction
- Automated monitoring

---

## 📞 Getting Help

- **Errors?** Check the console output
- **Not working?** Review success criteria
- **Stuck in loop?** Make criteria more specific
- **Tool not used?** Explicitly mention it in task
- **Need debugging?** See `TROUBLESHOOTING.md`

---

## 🚀 Next Steps

1. **Try the examples** above to get familiar
2. **Experiment** with different tool combinations
3. **Save successful prompts** for reuse
4. **Build workflows** for repetitive tasks
5. **Extend with new tools** as needed (see development.md)

---

**Remember**: Sidekick is most powerful when you give it clear goals and let it figure out the best way to use its tools to achieve them!
