from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # 경로 설정
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent
    @property
    def STATIC_PATH(self) -> Path: return self.BASE_PATH / "app" / "static"
    @property
    def TEMPLATES_PATH(self) -> Path: return self.BASE_PATH / "app" / "templates"

    # 모델 설정
    MODEL_KEEP_ALIVE: int = 0                      # 0:즉시 해제, 3600:1시간 유지, -1:무한 유지 (기본값은 5분)
    MODEL_OPTIONS_NUM_PREDICT: int = 5120          # num_predict: 분석 결과에 대한 길이(작은면 결과 짤려서 파싱 오류, 없으면 deepseek 경우 무한 루프)
    MODEL_OPTIONS_TEMPERATURE: float = 0.3         # temperature: 낮으면 일관성 유지
    MODEL_OPTIONS_TOP_P: float = 0.9               # top_p: 낮으면 좁은 답변
    @property
    def MODEL_OPTIONS(self) -> dict:
        return {
            "num_predict": self.MODEL_OPTIONS_NUM_PREDICT,
            "temperature": self.MODEL_OPTIONS_TEMPERATURE,
            # "top_p": self.MODEL_OPTIONS_TOP_P,
        }
    
    # 환경 변수
    PROJECT_NAME: str = "Python Ollam"
    DB_URL: str = "sqlite:///./test.db"
    
    # env 파일 설정 (자동으로 파일 읽기)
    model_config = SettingsConfigDict(env_file=".env")

# 전역에서 사용할 객체 생성
settings = Settings()