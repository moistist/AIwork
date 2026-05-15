#!/usr/bin/env python3
import json
import os
from datetime import datetime

def update_tokens():
    tokens_path = "data/tokens.json"
    
    with open(tokens_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update validity periods to future dates
    today = datetime.now()
    for token in data["tokens"]:
        # Set validity period to 6 months from now
        validity = today.replace(month=today.month + 6 if today.month < 7 else today.month - 6, year=today.year if today.month < 7 else today.year + 1)
        token["validityPeriod"] = validity.strftime("%Y-%m-%d")
        token["status"] = "active"
    
    with open(tokens_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_tools():
    tools_path = "data/tools.json"
    
    with open(tools_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add a sample new tool (in real scenario, you'd crawl or fetch from an API)
    new_tools = [
        {
            "id": "perplexity",
            "name": "Perplexity",
            "category": "聊天",
            "description": "AI搜索引擎，提供实时信息和深度回答。",
            "tags": ["搜索", "对话", "实时信息"],
            "url": "https://www.perplexity.ai",
            "pricing": "免费/付费",
            "features": ["实时搜索", "深度问答", "多模态", "引用来源"]
        }
    ]
    
    # Add new tools if not already present
    existing_ids = [tool["id"] for tool in data["tools"]]
    for tool in new_tools:
        if tool["id"] not in existing_ids:
            data["tools"].append(tool)
    
    with open(tools_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("Updating AIwork data files...")
    update_tokens()
    update_tools()
    print("Update complete!")
