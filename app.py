from flask import Flask, render_template, request, session
from nlp_matcher import extract_subject, find_exam_schedule, extract_query_intent, get_message_type
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    # Completely clear the session
    session.clear()
    # Force session modification
    session.modified = True
    return {'status': 'success', 'redirect': True}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize fresh chat history if it doesn't exist or is empty
    if 'chat_history' not in session or not session['chat_history']:
        session['chat_history'] = [{
            'user_message': None,
            'bot_message': "Hello! 👋 How can I help you today?",
            'timestamp': datetime.now().strftime("%H:%M")
        }]
        # initialize last_subject to None
        session['last_subject'] = None
        session.modified = True

    if request.method == 'POST':
        query = request.form.get('query', '')
        # detect message type (greeting/thanks/goodbye)
        msg_type = get_message_type(query)
        intent = extract_query_intent(query)
        subject = extract_subject(query)

        if msg_type:
            # handle greetings / thank you / goodbye
            response = find_exam_schedule(msg_type)
        else:
            if subject:
                # remember this subject for follow-ups
                session['last_subject'] = subject
                response = find_exam_schedule(subject, intent)
            else:
                # no subject specified -> fallback to last remembered subject
                last = session.get('last_subject')
                if last:
                    response = find_exam_schedule(last, intent)
                else:
                    response = "Please specify the subject (e.g., 'DBMS' or 'OS') so I can fetch details."
            
        # Add the new conversation to history
        timestamp = datetime.now().strftime("%H:%M")
        session['chat_history'].append({
            'user_message': query,
            'bot_message': response,
            'timestamp': timestamp
        })
        session.modified = True  # Ensure session is saved

    return render_template('index.html', chat_history=session['chat_history'])

if __name__ == '__main__':
    app.run(debug=True)