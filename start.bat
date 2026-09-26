@echo off
setlocal
cd /d "%~dp0"

echo ==============================================
echo   RAG 知识库 - 一键启动
echo ==============================================
echo.

REM ---- 1. 检查并启动 Docker ----
docker info >nul 2>&1
if not errorlevel 1 goto docker_ready
echo [提示] Docker 引擎未运行。
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    echo 正在启动 Docker Desktop，请稍候...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
) else (
    echo 请手动启动 Docker Desktop。
)
echo 等待 Docker 引擎就绪（最多 120 秒）...
set /a _d=0
:wait_docker
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if not errorlevel 1 goto docker_ready
set /a _d+=1
if %_d% lss 24 goto wait_docker
echo [错误] Docker 未能就绪，请手动打开 Docker Desktop 后重试本脚本。
pause
exit /b 1
:docker_ready

REM ---- 2. 启动中间件 ----
echo [1/3] 启动中间件 MySQL / etcd / MinIO / Milvus ...
docker compose up -d
if errorlevel 1 (
    echo [错误] 容器启动失败，请检查 Docker 状态。
    pause
    exit /b 1
)

echo 等待 Milvus 就绪（最多约 90 秒）...
set /a _n=0
:wait_milvus
curl.exe -sf --max-time 3 http://localhost:9091/healthz >nul 2>&1
if not errorlevel 1 goto milvus_ok
timeout /t 5 /nobreak >nul
set /a _n+=1
if %_n% lss 18 goto wait_milvus
echo [警告] Milvus 未在 90 秒内就绪，后端可能启动失败。
:milvus_ok

REM ---- 3. 启动后端 ----
echo [2/3] 启动后端（端口 8000）...
start "RAG-后端" cmd /k "python app.py"

REM ---- 4. 启动前端 ----
echo [3/3] 启动前端（端口 5173）...
start "RAG-前端" cmd /k "cd frontend && npm run dev"

echo.
echo ==============================================
echo   启动完成！
echo   后端加载模型约需 10-30 秒，之后浏览器打开：
echo   http://localhost:5173
echo   登录账号：admin    密码：admin123
echo ==============================================
echo.
echo 提示：后端和前端各自在独立窗口中运行，关闭窗口即停止对应服务。
pause
