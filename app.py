
from flask import Flask, jsonify, request, render_template
import queue
import random
import time
from flask_cors import CORS
from vertex import multiturn_generate_content

app = Flask(__name__)
CORS(app)

prompt = queue.Queue()
chat_history = []

def exponential_backoff_retry(func, max_retries=6, initial_wait=1, max_wait=256):
    retries = 0
    wait_time = initial_wait

    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                raise e
            print(f'Retry {retries}/{max_retries}. Waiting {wait_time} seconds...')
            time.sleep(wait_time)
            wait_time = min(wait_time * 4, max_wait)
    raise Exception('Max retries exceeded')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    global chat_history
    data = request.get_json()
    user_message = data.get('userMessage', '')
    print(user_message)
    
    if not prompt:
        return jsonify({'reply': "no message received."}), 400
    try:
        prompt.put(user_message)
        print(f'added user message: {user_message}')

        response = None
        while response is None:
            time.sleep(1)
            if not prompt.empty():
                prompt_queue = prompt.get()
                try: 
                    response = exponential_backoff_retry(
                        lambda: multiturn_generate_content(prompt_queue, chat_history)
                    )
                    print(response)
                    print(f"Chat history: {chat_history}")
                except Exception as e:
                    print(f'Exception in response {str(e)}')
                    return jsonify({'exception': f'Exception {e}'}), 500                


            return jsonify({'reply': response})
                  
    except Exception as e:
        print(f'exception in response {str(e)}')
        return jsonify({'exception': f'Exception {e}'}), 500        


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8080, debug=True)
