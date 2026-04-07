import json
import ollama
from datetime import datetime

# 추론 중심의 모델 - 결과 안남옴
prompt = '''
    이 이미지에서 모든 텍스트를 누락 없이 전부 추출해.
    요약내용(summary)과 전체내용(content)을 구분해서 json 형태로 출력해.
    [출력 예시]
    {
        "summary": "한글 요약내용",
        "content": "원문 전체내용"
    }
'''

def vlm_llama(base64_images):
    try:
        print(f"분석 시작: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': base64_images,
            }],
            # 0: 즉시 해제, 3600: 1시간 유지, -1: 무한 유지 (기본값은 5분)
            keep_alive=0
        )
        print(f"분석 종료: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

        content = response['message']['content']
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    
    except Exception as e:
        print(f"[분석 에러] {e}")
        return {}