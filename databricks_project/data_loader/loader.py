import pandas as pd
import os
import databricks.sql

def main():
    
    server_hostname=os.getenv("DATABRICKS_HOST"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")

    conn = databricks.sql.connect(
        server_hostname,
        http_path,
        access_token
    )
    

    query = "SELECT * FROM payroll_catalog.bronze.bronze_hrmanager limit 10"
    print(query)
    try:
   
        df = pd.read_sql(query, conn)
        print(df.head())  
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
      
        conn.close()

if __name__ == "__main__":
    main()
