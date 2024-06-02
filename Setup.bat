@echo off
REM 检查Python是否安装
python --version
if %errorlevel% NEQ 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

echo ** Python已将安装**
timeout /t 5 /nobreak > nul

REM 创建虚拟环境
python -m venv venv

echo ** 虚拟环境创建成功（与系统Python不共用包）**
timeout /t 5 /nobreak > nul

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate
pip install -r requirements.txt

echo ** 依赖已经安装完毕。若安装失败，可尝试检查网络原因 **
timeout /t 5 /nobreak > nul

echo 安装完成，请双击RideOn.bat运行程序。此窗口已可以关闭。感谢使用。

pause
