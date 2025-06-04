# Gemini Pro Company Research Automation

A Selenium-based automation script that generates comprehensive research reports for multiple companies using Google's Gemini Pro AI.

## Features

- Automatically generates detailed company research reports including:
  - SWOT Analysis
  - Industry Profile 
  - Industry Trends
  - Company Challenges
  - Competitor Analysis
- Uses Gemini Pro 2.5 with Deep Research capability
- Automatically saves reports to Google Docs
- Processes multiple companies in sequence
- Includes error handling and retry mechanisms
- Shows real-time progress with timestamps

## Prerequisites

- Python 3.x
- Chrome browser
- Selenium WebDriver
- Active Chrome debugging session on port 9222

## Required Python Packages

```bash
pip install selenium
```

## Setup Instructions

### 1. Start Chrome with Remote Debugging (Mac)
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### 2. Run the Script
```bash
python automation.py
```