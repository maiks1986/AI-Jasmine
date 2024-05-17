from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, Json, ValidationError

class IoModel(BaseModel):
    useTool: Optional[List[Tool]]
    message: Optional[str]

class Tool(BaseModel):
    tool: str = Field(..., description='')
    arguments: Json[Any]