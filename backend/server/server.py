from flask import Flask, request, jsonify
import datetime


app = Flask(__name__)

@app.route('/sendMessage', methods=['POST'])
def send_message():

    data = request.json
    user_message = data['user_message']
    
    # Process the message through your chatbot model
    bot_response = test_response(user_message)
    
    return jsonify(botResponse=bot_response)


def test_response(user_message):
    time_now = datetime.datetime.now().strftime('%H:%M:%S')
    return f'Got your message at {time_now}! Here it is backwards: {user_message[::-1]}'


if __name__ == '__main__':
    app.run(debug=True)
