import json

def ollama_result_json(response):
    try:
      content = response["message"]["content"]
      content = content.replace("```json", "").replace("```", "").strip()
      return json.loads(content)
    except json.JSONDecodeError as e:
      return {"summary": "parsing_error", "content": content}
    except Exception as e:
      return {"summary": "system_error", "content": str(e)}

def yolo_result_data(model_names, results):
    result_json = []
    result_cv2_images = []
    for idx, result in enumerate(results):
        result_cv2_images.append(result.plot())
        if hasattr(result, "boxes") and result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                det = {
                    "idx": idx,
                    "cls": int(box.cls[0]),                     # cls tensor([0.])
                    "name": model_names[int(box.cls[0])],       # 물체 이름
                    "conf": float(box.conf[0]),                 # 신뢰도
                    "xyxy": box.xyxy[0].tolist(),               # [x1, y1, x2, y2]
                }
                result_json.append(det)
        elif hasattr(result, "obb") and result.obb is not None and len(result.obb) > 0:
            for obb in result.obb:
                det = {
                    "idx": idx,
                    "cls": int(obb.cls[0]),                     # cls tensor([0.])
                    "name": model_names[int(obb.cls[0])],       # 물체 이름
                    "conf": float(obb.conf[0]),                 # 신뢰도
                    "xywhr": obb.xywhr[0].tolist(),             # [x_center, y_center, width, height, angle]
                    "xyxyxyxy": obb.xyxyxyxy[0].tolist(),       # 좌표 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                }
                result_json.append(det)
    return result_json, result_cv2_images

