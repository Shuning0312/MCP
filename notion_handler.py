import requests
import json
import os
import re

class NotionHandler:
    """处理与Notion的交互"""
    
    def __init__(self, token=None, database_id=None):
        self.token = token or os.environ.get("NOTION_TOKEN")
        self.database_id = database_id or os.environ.get("NOTION_DATABASE_ID")
        
        if not self.token:
            raise ValueError("需要提供Notion API令牌")
    
    def create_travel_plan_page(self, title, content):
        """在Notion中创建旅游计划页面"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        blocks = self.parse_markdown_to_blocks(content)

        payload = {
            "parent": {"database_id": self.database_id} if self.database_id else {"type": "workspace"},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            },
            "children": blocks
        }

        url = "https://api.notion.com/v1/pages"

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Notion API调用失败: {response.status_code}, {response.text}")

    def parse_markdown_to_blocks(self, content):
        blocks = []
        lines = content.strip().splitlines()

        table_buffer = []

        def flush_table():
            nonlocal table_buffer
            if len(table_buffer) >= 2:
                headers = [h.strip() for h in table_buffer[0].strip("|").split("|")]
                rows = table_buffer[2:] if "---" in table_buffer[1] else table_buffer[1:]
                blocks.append({
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": len(headers),
                        "has_column_header": True,
                        "children": [
                            {
                                "object": "block",
                                "type": "table_row",
                                "table_row": {
                                    "cells": [
                                        [{"type": "text", "text": {"content": cell.strip()}}]
                                        for cell in row.strip("|").split("|")
                                    ]
                                }
                            }
                            for row in rows if row.strip()
                        ]
                    }
                })
            table_buffer = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if "|" in stripped:
                table_buffer.append(stripped)
                continue
            else:
                flush_table()

            if stripped.startswith("# "):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": stripped[2:].strip()}}]
                    }
                })
            elif stripped.startswith("## "):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": stripped[3:].strip()}}]
                    }
                })
            elif stripped.startswith("- "):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": stripped[2:].strip()}}]
                    }
                })
            elif re.match(r"^\d+\.\s+\[.*\]\(.*\)", stripped):
                match = re.match(r"^\d+\.\s+\[(.*)\]\(.*\)", stripped)
                content = match.group(1) if match else stripped
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            elif stripped == "---":
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": part.replace("**", "")},
                                "annotations": {"bold": True} if part.startswith("**") and part.endswith("**") else {}
                            } for part in stripped.split(" ")  # naive bold word split
                        ]
                    }
                })

        flush_table()
        return blocks