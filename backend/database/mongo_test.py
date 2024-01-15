from pymongo import MongoClient
from bson import ObjectId
import sys
from dummy_data_playground import create_sample_data, drop_test_collections
# from dummy_data_playground import create_sample_data, drop_test_collections
import datetime

if __name__ == '__main__':

    # # Example usage
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test_database  # Replace 'test_database' with the name of your database
    drop_test_collections(db)    # Drop test collections if they exist
    create_sample_data(db)    # Create sample data
    