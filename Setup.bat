@echo off
cd /d "%~dp0"
REM ���Python�Ƿ�װ
python --version
if %errorlevel% NEQ 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

echo ** Python�ѽ���װ **
timeout /t 1 /nobreak > nul

REM �������⻷��
python -m venv venv

echo ** ���⻷�������ɹ�����ϵͳPython�����ð���**
timeout /t 1 /nobreak > nul

echo ** ������װ��������Ԥ������1.5G���̿ռ䣬����ʹ��Լ1G��������������ע���Ƿ�ʹ������ **
echo ** ���ؽ���5���ʼ����ȡ������Ϊ��� **
timeout /t 5 /nobreak

REM ���뵱ǰĿ¼���������⻷������װ����
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
venv\Scripts\python -m pip install torch torchvision

echo ** �����Ѿ���װ��ϡ�����װʧ�ܣ��ɳ��Լ������ԭ�� **
timeout /t 1 /nobreak > nul

echo ��װ��ɣ���˫��RideOn.bat���г��򡣴˴����ѿ��Թرա���лʹ�á�
echo setup.bat������Է������У����ᵼ�´���

pause
