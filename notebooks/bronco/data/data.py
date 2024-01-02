import pandas as pd
import sqlite3

QUERY_FAILED = '<query_failed>'

def upload_df_to_sql(df, table_name):
    
    conn = sqlite3.connect(':memory:')
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    return conn

def query_database(db_path, query, max_rows=15):

    try:
        with sqlite3.connect(db_path) as connection:

            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchmany(max_rows)   # limit rows
            columns = tuple([x[0] for x in cursor.description])

            return pd.DataFrame(rows, columns=columns)

    except:
        return QUERY_FAILED


def get_schema(db_path, table_name):

    command = f"PRAGMA table_info('{table_name}')"

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(command)
        rows = [row[1:3] for row in cursor.fetchall()]

    return rows

def get_table_sample(df):
    
    df = query_database(db_connection, query='SELECT * FROM {table_name} ORDER BY RANDOM()', max_rows=1000)

    column_samples = []
    for column in df.columns:
        column_sample_values = list(df[column].value_counts().keys()[:n_samples])
        sample_string = f'{column}: {column_sample_values}'
        column_samples.append(sample_string)

    return '\n'.join(column_samples)

