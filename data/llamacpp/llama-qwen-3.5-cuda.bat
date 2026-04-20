@echo off
title Qwen3.5 Server Runner
chcp 65001

:: --- 설정 영역: 본인의 경로에 맞게 수정하세요 ---
set LLAMA_PATH=C:\00_work\00_program\llama-b8833-bin-win-cuda-12.4-x64
set LLAMA_PORT=8000
set MODEL_PATH=C:\00_work\03_model\gguf\Qwen3.5\Qwen3.5-4B-Q4_K_M.gguf
set MMPROJ_PATH=C:\00_work\03_model\gguf\Qwen3.5\mmproj-Qwen3.5-4B-BF16.gguf
set MODEL_ALIAS=qwen3.5:4b
:: ------------------------------------------

echo [!] Qwen3.5 서버를 시작합니다...
echo [!] 모델: %MODEL_PATH%
echo [!] 브라우저에서 http://127.0.0.1:"%LLAMA_PORT%"접속

cd /d "%LLAMA_PATH%"

.\llama-server.exe ^
  --model "%MODEL_PATH%" ^
  --alias "%MODEL_ALIAS%" ^
  --mmproj "%MMPROJ_PATH%" ^
  --ctx-size 4096 ^
  --temp 0.3 ^
  --n-gpu-layers 99 ^
  --port "%LLAMA_PORT%" ^
  --host 0.0.0.0

pause