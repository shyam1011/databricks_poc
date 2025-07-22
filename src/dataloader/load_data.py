import pandas as pd
import os
import databricks.sql

def load_data():
    # Get environment variables
    server_hostname = os.getenv("DATABRICKS_HOST")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")

    # Debug prints
    print("Connecting to Databricks with:")
    print(f"Host: {server_hostname}")
    print(f"HTTP Path: {http_path}")

    try:
        # Establish connection
        conn = databricks.sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )

        query = "SELECT * FROM payroll_catalog.bronze.bronze_hrmanager LIMIT 10"
        print("Executing query:", query)

        # Run query
        df = pd.read_sql(query, conn)
        print("Query returned:")
        print(df.head())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Safely close connection if it exists
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    load_data()
