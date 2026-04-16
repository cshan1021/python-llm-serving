import json

def ollama_to_json(response):
    try:
      content = response['message']['content']
      content = content.replace('```json', '').replace('```', '').strip()
      return json.loads(content)
    except json.JSONDecodeError as e:
      return {"summary": "parsing_error", "content": content}
    except Exception as e:
      return {"summary": "system_error", "content": str(e)}