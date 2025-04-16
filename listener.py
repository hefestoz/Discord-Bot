from flask import Flask, request
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
listenerToken = os.getenv("LISTENER_TOKEN") 

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_file():
    print("📦 Ejecutando el archivo .bat...")
    token = request.headers.get('Authorization')

    # Basic security
    if token != "listenerToken":
        return "Unauthorized", 401

    
    ruta = r'"C:\Users\User\Desktop\1.21.4 Paper\iniciar-servidor.bat"'
    subprocess.Popen([
    "powershell", 
    "-Command", 
    "Start-Process 'C:\\Users\\User\\Desktop\\1.21.4 Paper\\iniciar-servidor.bat'"
], shell=True)


    return "✅ File executed!", 200

if __name__ == '__main__':
    app.run(port=5000)
