import os
import yaml
from pathlib import Path
from pydantic import BaseModel, ValidationError

from .database import DatabaseConfig
from .redis import RedisConfig
from .jwt import JWTConfig
from .api_ir import ApiIrConfig

# ============================================================
# Helper: ENV substitution
# ============================================================

def _env_interpolate_string(content: str) -> str:
    """
    Interpolate environment variables in a string (before YAML parsing).
    Supports ${VAR} and ${VAR:-default} syntax.
    """
    import re
    
    def replace_env(match):
        var_expr = match.group(1)
        if ":-" in var_expr:
            var_name, default_value = var_expr.split(":-", 1)
            env_value = os.getenv(var_name, default_value)
        else:
            env_value = os.getenv(var_expr, "")
        return str(env_value)
    
    # Replace ${VAR} or ${VAR:-default} patterns
    pattern = r'\$\{([^}]+)\}'
    return re.sub(pattern, replace_env, content)

def _env_interpolate(value: any) -> any:
    """
    Recursively replace ${VAR} or ${VAR:-default} inside strings with os.environ values.
    Supports nested lists and dicts.
    """
    if isinstance(value, str):
        if "${" in value:
            start = value.find("${")
            end = value.find("}", start)
            if end != -1:
                var_expr = value[start + 2:end]
                # Check for default value syntax: VAR:-default
                if ":-" in var_expr:
                    var_name, default_value = var_expr.split(":-", 1)
                    env_value = os.getenv(var_name, default_value)
                else:
                    env_value = os.getenv(var_expr, "")
                return value[:start] + env_value + value[end + 1:]
        return value

    if isinstance(value, list):
        return [_env_interpolate(v) for v in value]

    if isinstance(value, dict):
        return {k: _env_interpolate(v) for k, v in value.items()}

    return value

# -----------------------------
# Root Config
# -----------------------------

class ServiceConfig(BaseModel):
    service: dict
    database: DatabaseConfig
    redis: RedisConfig
    jwt: JWTConfig
    api_ir: ApiIrConfig
    logging: dict

    class Config:
        validate_assignment = True

# ============================================================
# Loader Function
# ============================================================
def load_service_config(path: str | Path = None) -> ServiceConfig:
    """
    Reads config.yml, performs environment variable substitution,
    and returns a typed ServiceConfig object.
    """
    if path is None:
        path = Path(__file__).resolve().parent.parent.parent / "config.yml"

    if not Path(path).exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    # Read file as string first to do env interpolation before YAML parsing
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Interpolate environment variables in the YAML content string
    content = _env_interpolate_string(content)
    
    # Now parse the YAML
    raw = yaml.safe_load(content)

    try:
        config = ServiceConfig(**raw)
    except ValidationError as e:
        raise RuntimeError(f"Invalid configuration structure:\n{e}")

    return config
