from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # 프로젝트 루트 경로
    BASE_PATH: Path = Path(__file__).resolve().parent
    
    # 환경 변수들 (기본값 설정 가능)
    PROJECT_NAME: str = "VLM Project"
    DB_URL: str = "sqlite:///./test.db"
    
    # 3. .env 파일 설정 (자동으로 파일 읽기)
    model_config = SettingsConfigDict(env_file=".env")

# 전역에서 사용할 객체 생성
settings = Settings()