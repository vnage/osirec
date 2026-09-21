def format_code_snippet(code, language="python"):
    return f"```{language}\n{code.strip()}\n```"

def base64_encode(text):
    import base64
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    import base64
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "invalid base64 string"