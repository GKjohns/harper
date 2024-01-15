from pymongo import MongoClient
from bson import ObjectId
import datetime

def create_sample_data(db):
    # Sample users
    users = [
        {"_id": ObjectId("507f1f77bcf86cd799439011"), "name": "Alice"},
        {"_id": ObjectId("507f1f77bcf86cd799439012"), "name": "Bob"}
    ]

    # Sample conversations
    conversations = [
        {
            "_id": ObjectId("507f191e810c19729de860ea"),
            "userid": "507f1f77bcf86cd799439011",
            "messages": [
                {"timestamp": datetime.datetime(2023, 1, 1, 10, 0), "content": "Hello!", "is_chatbot": False},
                {"timestamp": datetime.datetime(2023, 1, 1, 10, 1), "content": "Hi Alice!", "is_chatbot": True},
                {"timestamp": datetime.datetime(2023, 1, 1, 10, 2), "content": "How are you?", "is_chatbot": False},
                # More messages...
            ]
        },
        {
            "_id": ObjectId("507f191e810c19729de860eb"),
            "userid": "507f1f77bcf86cd799439012",
            "messages": [
                {"timestamp": datetime.datetime(2023, 2, 5, 15, 30), "content": "What's the weather like today?", "is_chatbot": False},
                {"timestamp": datetime.datetime(2023, 2, 5, 15, 31), "content": "It's sunny and warm.", "is_chatbot": True},
                {"timestamp": datetime.datetime(2023, 2, 5, 15, 35), "content": "Great, I'll go for a walk!", "is_chatbot": False},
                # More messages...
            ]
        },
        {
            "_id": ObjectId("507f191e810c19729de860ec"),
            "userid": "507f1f77bcf86cd799439011",
            "messages": [
                {"timestamp": datetime.datetime(2023, 3, 10, 9, 0), "content": "Do you have any book recommendations?", "is_chatbot": False},
                {"timestamp": datetime.datetime(2023, 3, 10, 9, 5), "content": "Sure, I recommend 'The Great Gatsby' by F. Scott Fitzgerald.", "is_chatbot": True},
                {"timestamp": datetime.datetime(2023, 3, 10, 9, 10), "content": "Thanks, I'll check it out!", "is_chatbot": False},
                # More messages...
            ]
        },
        {
            "_id": ObjectId("507f191e810c19729de860ed"),
            "userid": "507f1f77bcf86cd799439012",
            "messages": [
                {"timestamp": datetime.datetime(2023, 4, 15, 2, 0), "content": "What should I make for dinner tonight?", "is_chatbot": False},
                {"timestamp": datetime.datetime(2023, 4, 15, 20, 2), "content": "Mmmm green beans would be good", "is_chatbot": True},
                {"timestamp": datetime.datetime(2023, 4, 15, 20, 5), "content": "Great! Thank you chatbot!", "is_chatbot": False},
                # More messages...
            ]
        },
        {
            "_id": ObjectId("507f191e810c19729de860ee"),
            "userid": "507f1f77bcf86cd799439011",
            "messages": [
                {"timestamp": datetime.datetime(2023, 5, 20, 11, 0), "content": "Can you help me with my math homework?", "is_chatbot": False},
                {"timestamp": datetime.datetime(2023, 5, 20, 11, 3), "content": "Of course, what do you need help with?", "is_chatbot": True},
                {"timestamp": datetime.datetime(2023, 5, 20, 11, 10), "content": "I'm stuck on a calculus problem.", "is_chatbot": False},
                # More messages...
            ]
        }
    ]

    # Insert sample data into the database
    db.Users.insert_many(users)
    db.Conversations.insert_many(conversations)

    print("Sample data created.")
    
def print_all_conversations(db, user_id):
    # Print all conversations for a given user
    print("Printing all conversations for user with ID", user_id)
    for conversation in db.Conversations.find({"userid": user_id}):
        # extract the messages and print them
        messages = conversation['messages']
        print("Conversation ID:", conversation['_id'])
        for message in messages:
            print(message)    
        print() 
    
    
        
def drop_test_collections(db):
    db.Users.drop()
    db.Conversations.drop()


if __name__ == '__main__':
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test_database
    drop_test_collections(db)
    create_sample_data(db)
    
    # Print all conversations for Alice
    alice_id = ObjectId("507f1f77bcf86cd799439011")
    print_all_conversations(db, alice_id)
    
    drop_test_collections(db)
    print("Test collections dropped.")
    
    
