@echo off
REM ���Python�Ƿ�װ
python --version
if %errorlevel% NEQ 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

echo ** Python�ѽ���װ**
timeout /t 5 /nobreak > nul

REM �������⻷��
python -m venv venv

echo ** ���⻷�������ɹ�����ϵͳPython�����ð���**
timeout /t 5 /nobreak > nul

REM �������⻷������װ����
call venv\Scripts\activate
pip install -r requirements.txt

echo ** �����Ѿ���װ��ϡ�����װʧ�ܣ��ɳ��Լ������ԭ�� **
timeout /t 5 /nobreak > nul

echo ��װ��ɣ���˫��RideOn.bat���г��򡣴˴����ѿ��Թرա���лʹ�á�

pause
