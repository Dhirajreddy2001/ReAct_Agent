from typing import Any, List
import re
def as_text(output: Any) -> str:


    if isinstance(output, str):
        return output

    content = getattr(output, "content", None)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return content
    
    if isinstance(content, list):
        parts:List[str] = []
        for block in content:
            t = getattr(block, "text", None)
            if t:
                parts.append(t)
                continue
            if isinstance(block, dict) and "text" in block:
                parts.append(str(block["text"]))
        if parts:
            return "\n".join(parts)

    return str(output)

def normalize(text: str) -> str:

    t = text.lower().strip()
    t = re.sub(r'^(what is|whats|what\'s|tell me|calculate|compute)\s+', '', t)
    t = re.sub(r'[^\w\s\+\-\*\/\^\=]', '', t)
    t = re.sub(r"\s+","",t)
    return t

        