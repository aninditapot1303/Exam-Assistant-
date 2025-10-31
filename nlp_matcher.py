import json

def load_exam_data():
    try:
        with open('exams.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_message_type(query):
    query = query.lower().strip()
    
    greetings = ['hi', 'hello', 'hey', 'hola', 'greetings']
    goodbyes = ['goodbye', 'bye', 'see you', 'see ya', 'cya', 'good bye']
    thank_yous = ['thank you', 'thanks', 'thank u', 'thankyou', 'thank you so much', 'tysm']
    
    if query in greetings:
        return "GREETING"
    elif query in goodbyes:
        return "GOODBYE"
    elif any(thank in query for thank in thank_yous):
        return "THANK_YOU"
    return None

def extract_query_intent(query):
    query = query.upper()
    
    # Define intent patterns
    intent_patterns = {
        'VENUE': ['WHERE', 'VENUE', 'ROOM', 'LOCATION', 'PLACE'],
        'DURATION': ['HOW LONG', 'DURATION', 'TIME DURATION'],
        'TOPICS': ['TOPICS', 'SYLLABUS', 'PORTIONS', 'WHAT TO STUDY'],
        'PROFESSOR': ['PROFESSOR', 'PROF', 'TEACHER', 'WHO'],
        'INSTRUCTIONS': ['INSTRUCTIONS', 'RULES', 'WHAT TO BRING'],
        'MARKS': ['MARKS', 'MAXIMUM MARKS', 'TOTAL MARKS', 'MAX MARKS']
    }
    
    # Check for specific intents
    for intent, keywords in intent_patterns.items():
        if any(keyword in query for keyword in keywords):
            return intent
            
    return 'SCHEDULE'  # Default intent

def extract_subject(query):
    # Convert query to uppercase for better matching
    query = query.upper()
    
    # List of common subject names and their variations
    subject_keywords = {
        'DBMS': ['DBMS', 'DATABASE', 'DB'],
        'OS': ['OS', 'OPERATING SYSTEM', 'OPERATING SYSTEMS'],
        'DSA': ['DSA', 'DATA STRUCTURES', 'ALGORITHMS'],
        'PYTHON': ['PYTHON', 'PYTHON PROGRAMMING'],
        'JAVA': ['JAVA', 'JAVA PROGRAMMING']
    }
    
    # Check for each subject and its variations in the query
    for subject, keywords in subject_keywords.items():
        if any(keyword in query for keyword in keywords):
            return subject
            
    return None

def find_exam_schedule(subject, intent='SCHEDULE'):
    if isinstance(subject, tuple):
        subject, intent = subject

    if subject in ["GREETING", "GOODBYE", "THANK_YOU"]:
        if subject == "GREETING":
            return "Hello! 👋 How can I help you today? You can ask me about your exam schedules, venues, topics, and more!"
        elif subject == "GOODBYE":
            return "Goodbye! 👋 Good luck with your exams! Feel free to come back if you need any more information!"
        elif subject == "THANK_YOU":
            responses = [
                "You're welcome! 😊 Let me know if you need anything else!",
                "Anytime! 👍 Don't hesitate to ask more questions!",
                "My pleasure! 🌟 Good luck with your studies!"
            ]
            import random
            return random.choice(responses)

    exam_data = load_exam_data()
    
    if subject not in exam_data:
        return f"Sorry, I couldn't find any exam information for {subject}"
        
    exam_info = exam_data[subject]
    
    # Format response based on intent
    if intent == 'SCHEDULE':
        # Return only date and time for 'when' queries — do not include venue or other details
        return f"Your {subject} exam is scheduled for {exam_info['date']} at {exam_info['time']}"
    elif intent == 'VENUE':
        return f"The {subject} exam will be held in {exam_info['venue']}"
    elif intent == 'DURATION':
        return f"The {subject} exam duration is {exam_info['duration']}"
    elif intent == 'TOPICS':
        topics = ", ".join(exam_info['topics'])
        return f"The {subject} exam will cover: {topics}"
    elif intent == 'PROFESSOR':
        return f"The {subject} exam will be conducted by {exam_info['professor']}"
    elif intent == 'INSTRUCTIONS':
        instructions = "\\n".join([f"• {inst}" for inst in exam_info['instructions']])
        return f"Instructions for {subject} exam:\\n{instructions}"
    elif intent == 'MARKS':
        return f"The {subject} exam is for {exam_info['max_marks']} marks"
    
    return f"Sorry, I couldn't understand what specific information you need about the {subject} exam"