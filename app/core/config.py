from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import dotenv
dotenv.load_dotenv()

class Settings(BaseSettings):
    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")
    environment: str = Field(default="development", alias="ENVIRONMENT")

    model_config = {"env_file": ".env"}

    def model_post_init(self, __context) -> None:
        if not self.database_url:
            raise ValueError("DATABASE_URL is required. Set it in environment or .env file.")


settings = Settings()
