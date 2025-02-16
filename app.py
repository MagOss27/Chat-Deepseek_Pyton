from flask import Flask, request, render_template_string, session  # Adicione 'session'
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para a sessão (adicione no .env em produção!)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat com DeepSeek</title>
</head>
<body>
    <h1>Chat com DeepSeek</h1>
    <div id="chat">
        {% for message in session.messages %}
            <p><strong>{{ message.role }}:</strong> {{ message.content }}</p>
        {% endfor %}
    </div>
    <form method="POST">
        <input type="text" name="user_input" placeholder="Digite sua mensagem..." required>
        <button type="submit">Enviar</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def chat():
    # Inicializa a sessão se não existir
    if 'messages' not in session:
        session['messages'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek/deepseek-chat:free", "messages": [{"role": "user", "content": user_input}]}
        )

        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            # Adiciona às mensagens da sessão
            session['messages'].append({"role": "user", "content": user_input})
            session['messages'].append({"role": "assistant", "content": ai_response})
            session.modified = True  # Força atualização da sessão

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)