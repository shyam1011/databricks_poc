import pandas as pd
import databricks.sql

def main():

    conn = databricks.sql.connect(
        server_hostname="adb-4477823463141297.17.azuredatabricks.net",
        http_path="/sql/1.0/warehouses/7ae128948e05b24a",
        access_token="dapi0fc93bcea9f033b5e119ade8f485b834-3"
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
