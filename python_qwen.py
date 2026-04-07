import base64
import cv2
import json
import ollama

# 설명 중심의 모델 - 속도가 엄청 느림
prompt_text = '''
    이 이미지에서 모든 텍스트를 누락 없이 전부 추출해.
    요약내용(summary)과 전체내용(content)을 구분해서 json 형태로 출력해.
    [출력 예시]
    {
        "summary": "한글 요약내용",
        "content": "원문 전체내용"
    }
'''

def vlm_qwen(cv2_images):
    prompt_images = []
    for cv2_image in cv2_images:
        _, buffer = cv2.imencode('.jpg', cv2_image)
        prompt_images.append(base64.b64encode(buffer).decode('utf-8'))
    
    if not prompt_images:
        print("유효하게 인코딩된 이미지가 0개입니다.")
        return {}

    try:
        response = ollama.chat(
            model='qwen3-vl:2b',
            format='json',
            messages=[{
                'role': 'user',
                'content': prompt_text,
                'images': prompt_images,
            }],
            # 0: 즉시 해제, 3600: 1시간 유지, -1: 무한 유지 (기본값은 5분)
            keep_alive=0,
            # 실시간 응답 True
            stream=True
        )

        content = ""
        for chunk in response:
            part = chunk.get('message', {}).get('content', '')
            content += part
            print(part, end='', flush=True)

        # 모델이 마크다운 태그를 붙여줬을 경우를 대비한 정제
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    
    except Exception as e:
        print(f"[분석 에러] {e}")
        return {}