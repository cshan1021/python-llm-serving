from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 경로 설정
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent
    @property
    def STATIC_PATH(self) -> Path: return self.BASE_PATH / "app" / "static"
    @property
    def TEMPLATES_PATH(self) -> Path: return self.BASE_PATH / "app" / "templates"

    # OLLAMA API URL
    OLLAMA_TEXT_ENDPOINT: str = "http://localhost:11434/api/generate"
    OLLAMA_CHAT_ENDPOINT: str = "http://localhost:11434/api/chat"
    # OPENAI API URL
    OPENAI_TEXT_ENDPOINT: str = "http://localhost:8000/v1/completions"
    OPENAI_CHAT_ENDPOINT: str = "http://localhost:8000/v1/chat/completions"

    # 환경 변수
    PROJECT_NAME: str = "Python LLM Serving"
    DB_URL: str = "sqlite:///./test.db"
    
    # env 파일 설정 (자동으로 파일 읽기)
    model_config = SettingsConfigDict(env_file=".env")

# 전역에서 사용할 객체 생성
settings = Settings()