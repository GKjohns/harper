import datetime
import sys
sys.path.append('..') 

import bronco

chatbot_response_prompt = '''
# Task
You are an AI chatbot. It is your job to respond to respond tomessages from a human user.
When responding, be sure to do the following: {personality}
Be sure you're not repeating phrases you've already used.

# Chat history
{context}

# Human input
Human: {human_input}

# Your response
'''

class AIChatBot:

    def __init__(self, personality, name='Chatbot', context=None):
        self.name = name
        self.personality = personality
        self.context = context or '*no additional context*'

    def respond(self, user_message, context_for_message=None):

        context_to_inject = context_for_message or self.context
        
        full_prompt = chatbot_response_prompt.format(**{
            'personality': self.personality,
            'context': context_to_inject,
            'human_input': user_message
        })
        
        response = bronco.llm_call(full_prompt)

        return response


class BasicChatMemory:

    def __init__(self):
        self.events = []

    def log_event(self, event_dict):
        """
        Log any event. The event_dict must contain 'type' and 'event_description'.
        A timestamp will be added to each logged event.
        """
        timestamp = datetime.datetime.now()
        event_dict['timestamp'] = timestamp
        self.events.append(event_dict)

    def chat_events_to_list(self, events=None):
        with_bullets = ['-' + x for x in self.get_readable_log(events=events)]
        return '\n'.join(with_bullets)

    def get_relevant_context(self):
        '''
        Summarize the chat history into a few hundred tokens for the next response.
        This method should implement a way to extract the most relevant parts of the
        conversation for context in generating future responses.
        '''

        return self.chat_events_to_list()
        

    def get_readable_log(self, events=None):
        '''Display the entire chat log in a sequential manner.'''
        log_lines = []
        events_to_log = events or self.events
        if not isinstance(events_to_log, list):
            events_to_log = [events_to_log]
        for event in events_to_log:
            content = event['full_content']
            line = f"{event['type']}: {content}"
            log_lines.append(line)

        return(log_lines)
    
events_summarizer = '''
# Task
Your job is to summarize a list of events. The events will be in the form of bullet points.
Your summarized list should be no longer than about 8 bullet points.

# Full events list
{events}

# Summarized events list
'''

events_summarizer = bronco.LLMFunction(prompt_template=events_summarizer)

class SummaryThresholdMemory(BasicChatMemory):

    def __init__(self, max_buffer=8):
        super().__init__()
        self.early_summary = ''
        self.max_buffer = max_buffer


    def log_event(self, event_dict):
        """
        Log any event. The event_dict must contain 'type' and 'event_description'.
        A timestamp will be added to each logged event.
        Also boil down the chat log into a summary if necessary
        """
        timestamp = datetime.datetime.now()
        event_dict['timestamp'] = timestamp
        self.events.append(event_dict)

        # no need to summarize
        if len(self.events) <= self.max_buffer:
            return

        # resummarize
        event_to_summarize = self.chat_events_to_list(self.events[-(self.max_buffer + 1)])
        events_to_summarize = self.early_summary + '\n' + event_to_summarize

        self.early_summary = events_summarizer.generate({
            'events': events_to_summarize
        })


    def get_relevant_context(self):
        return self.early_summary + '\n' + self.chat_events_to_list(self.events[-self.max_buffer])
    

class ChatSession:

    def __init__(self, chatbot, context):
        self.chatbot = chatbot
        self.context = context

    def run_chat(self):
        while True:
            
            user_input = input('User: ')
            
            # if the input is "quit" then quit
            if user_input.lower() == 'quit':
                return
                
            self.context.log_event({
                'type': 'user_input',
                'full_content': user_input
            })

            # else send it to the chatbot and get a response
            chat_history = self.context.get_readable_log()
            chatbot_response = self.chatbot.respond(
                user_message=user_input,
                context_for_message=chat_history
            )
            self.context.log_event({
                'type': 'chatbot_response',
                'full_content': chatbot_response
            })

            print(f'{self.chatbot.name}: {chatbot_response}')


personalities = {
    'Harper': '''You should infuse your replies with wit and a touch of playful teasing, while maintaining a confident and helpful tone. Remember to incorporate subtle references or humor, adding an element of sophistication to your interactions. Your language should be engaging and slightly flirtatious, yet always focused on providing clear and useful information. Be sure to keep your response fairly short concise.''',
    
    'Ava': '''Your responses should radiate warmth and empathy, always aiming to comfort and reassure. Use gentle humor and sprinkle in personal anecdotes to make your conversations more relatable. Keep your language simple and approachable, ensuring that the information provided is both helpful and easy to understand.''',

    'Max': '''Infuse your replies with dynamic energy and enthusiasm, as if you're always excited to help. Use vivid descriptions and a positive tone to energize the conversation. Be brief but informative, and don't hesitate to encourage and motivate with your words.''',

    'Zoe': '''Your tone should be calm and soothing, like a gentle guide through a complex world. Use metaphors and analogies to simplify complex topics, ensuring clarity and comprehension. Maintain a patient and understanding demeanor, offering detailed explanations when needed.''',

    'Eli': '''Adopt a quirky and creative approach in your responses, using playful language and unexpected twists. Be imaginative in your examples and analogies, making each interaction a delightful surprise. Keep your replies informative but light-hearted, ensuring they are as entertaining as they are helpful.''',

    'Nora': '''Your responses should be thoughtful and reflective, offering deep insights and thoughtful advice. Use a conversational tone that invites introspection and meaningful discussion. While providing information, aim to inspire and provoke deeper thinking about the subject matter.'''
}

if __name__ == '__main__':

    name = 'Harper'

    personality = personalities[name]
    chatbot = AIChatBot(name=name, personality=personality)
    context = BasicChatMemory()
    session = ChatSession(chatbot=chatbot, context=context)
    
    session.run_chat()