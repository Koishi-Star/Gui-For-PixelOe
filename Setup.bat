@echo off
cd /d "%~dp0"
REM 检查Python是否安装
python --version
if %errorlevel% NEQ 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

echo ** Python已将安装 **
timeout /t 1 /nobreak > nul

REM 创建虚拟环境
python -m venv venv

echo ** 虚拟环境创建成功（与系统Python不共用包）**
timeout /t 1 /nobreak > nul

echo ** 即将安装依赖包，预计需求1.5G磁盘空间，即将使用约1G网络下载量，请注意是否使用流量 **
echo ** 下载将在5秒后开始，不取消将视为许可 **
timeout /t 5 /nobreak

REM 进入当前目录、激活虚拟环境并安装依赖
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
venv\Scripts\python -m pip install torch torchvision

echo ** 依赖已经安装完毕。若安装失败，可尝试检查网络原因 **
timeout /t 1 /nobreak > nul

echo 安装完成，请双击RideOn.bat运行程序。此窗口已可以关闭。感谢使用。
echo setup.bat程序可以反复运行，不会导致错误。

pause
