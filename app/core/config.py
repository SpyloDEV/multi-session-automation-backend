from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Multi-Session Automation Backend"
    version: str = "0.1.0"


settings = Settings()
