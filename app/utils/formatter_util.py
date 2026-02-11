import json
from typing import Any, Dict, List
from app.services.log_service import LogService

def _format_value(value: Any) -> str:
    """Format a single value for display"""
    if value is None:
        return "<em style='color: #999;'>N/A</em>"
    elif isinstance(value, bool):
        return f"<span style='color: {'green' if value else 'red'};'><strong>{'Yes' if value else 'No'}</strong></span>"
    elif isinstance(value, (list, tuple)):
        if not value:
            return "<em style='color: #999;'>Empty</em>"
        items_html = "".join(f"<li>{_format_value(v)}</li>" for v in value)
        return f"<ul style='margin: 5px 0;'>{items_html}</ul>"
    elif isinstance(value, dict):
        return _format_dict(value)
    else:
        return str(value).replace("<", "&lt;").replace(">", "&gt;")


def _format_dict(data: Dict[str, Any], indent: int = 0) -> str:
    """Format a dictionary recursively"""
    if not data:
        return "<em style='color: #999;'>Empty</em>"
    
    items_html = ""
    for key, value in data.items():
        label = key.replace("_", " ").title()
        formatted_val = _format_value(value)
        items_html += f"<p style='margin: 8px 0;'><strong>{label}:</strong> {formatted_val}</p>"
    
    return items_html


def format_form(title: str, raw_json: str) -> str:
    """
    Format JSON form data to HTML with better styling and structure.
    
    Args:
        title: HTML title/heading
        raw_json: JSON string to format
        
    Returns:
        Formatted HTML string
    """
    try:
        data = json.loads(raw_json)
        
        html_parts = [
            "<style>",
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }",
            ".form-container { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 10px 0; }",
            ".form-title { font-size: 24px; margin-bottom: 15px; color: #333; }",
            "</style>",
            f"<div class='form-container'>",
            f"<h2 class='form-title'>{title}</h2>",
        ]
        
        if isinstance(data, dict):
            html_parts.append(_format_dict(data))
        else:
            html_parts.append(f"<p>{_format_value(data)}</p>")
        
        html_parts.append("</div>")
        return "\n".join(html_parts)
        
    except json.JSONDecodeError as e:
        LogService.ERROR.log(f"Invalid JSON in form formatter: {str(e)}", level="ERROR")
        return f"<p style='color: red;'>Error: Invalid JSON format</p>"
    except Exception as e:
        LogService.ERROR.log(f"Error formatting form data: {str(e)}", level="ERROR")
        return f"<p style='color: red;'>Error: {str(e)}</p>"