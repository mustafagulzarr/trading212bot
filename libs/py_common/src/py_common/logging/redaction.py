SENSITIVE_KEYS = {"api_key", "api_secret", "secret", "password", "token", "authorization", "auth_header", "cookie"}


def redact_payload(value):
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if k.lower() in SENSITIVE_KEYS:
                out[k] = "<redacted>"
            else:
                out[k] = redact_payload(v)
        return out
    if isinstance(value, list):
        return [redact_payload(v) for v in value]
    if isinstance(value, str) and value.startswith("Basic "):
        return "<redacted>"
    return value
