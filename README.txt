کمک‌یار نهم با GPT-5.6

1. Python را نصب کن.
2. ZIP را Extract کن.
3. داخل پوشه ترمینال باز کن.
4. اجرا کن:
   pip install -r requirements.txt

5. کلید OpenAI API را فقط روی سرور تنظیم کن، نه داخل HTML.

Windows PowerShell:
   $env:OPENAI_API_KEY="کلید-خودت"

macOS/Linux:
   export OPENAI_API_KEY="کلید-خودت"

6. سرور:
   uvicorn server:app --host 0.0.0.0 --port 8000

7. مرورگر:
   http://127.0.0.1:8000

برای استفاده از گوشی با کامپیوتر، هر دو را به یک Wi-Fi وصل کن و به IP کامپیوتر با پورت 8000 برو، مثلاً:
http://192.168.1.10:8000

کلید API را داخل HTML نگذار.
