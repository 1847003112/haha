@echo off
setlocal
cd /d "%~dp0"

echo 停止中间件容器（MySQL / etcd / MinIO / Milvus），保留数据...
docker compose down

echo.
echo 中间件已停止。
echo 后端和前端请分别在其窗口内按 Ctrl+C，或直接关闭窗口。
echo.
echo 如需连同数据一起删除（谨慎！）：docker compose down -v
pause
