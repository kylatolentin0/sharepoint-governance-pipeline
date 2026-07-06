import pandas as pd
from sqlalchemy import create_engine

print("Starting ETL process...")

# --- STEP A: EXTRACT ---
# Read the raw CSV files we just made
audit_df = pd.read_csv("sharepoint_audit_events.csv")
permissions_df = pd.read_csv("site_permissions_matrix.csv")

# --- STEP B: TRANSFORM ---
# Clean dates and extract file formats
audit_df['Timestamp'] = pd.to_datetime(audit_df['Timestamp'])
audit_df['File_Extension'] = audit_df['Item_Name'].str.extract(r'(\.\w+)')

# --- STEP C: MODELING (Organizing the data into a Star Schema) ---
# Create dimension tables to organize unique users, files, and actions neatly
dim_users = pd.DataFrame({"User_ID": range(1, len(audit_df['User'].unique()) + 1), "User_Name": audit_df['User'].unique()})
dim_files = pd.DataFrame({"File_ID": range(1, len(audit_df['Item_Name'].unique()) + 1), "File_Name": audit_df['Item_Name'].unique()})
dim_operations = pd.DataFrame({"Op_ID": range(1, len(audit_df['Operation'].unique()) + 1), "Operation_Name": audit_df['Operation'].unique()})

# Connect them all together into a master activity fact table
fact_audit = audit_df.merge(dim_users, left_on="User", right_on="User_Name") \
                     .merge(dim_files, left_on="Item_Name", right_on="File_Name") \
                     .merge(dim_operations, left_on="Operation", right_on="Operation_Name") \
                     [["Timestamp", "User_ID", "File_ID", "Op_ID", "File_Extension"]]

# --- STEP D: LOAD ---
# This creates a local SQLite database file automatically in your folder
engine = create_engine("sqlite:///sharepoint_governance.db")

# Save all these organized tables into the database file
dim_users.to_sql("dim_users", engine, if_exists="replace", index=False)
dim_files.to_sql("dim_files", engine, if_exists="replace", index=False)
dim_operations.to_sql("dim_operations", engine, if_exists="replace", index=False)
fact_audit.to_sql("fact_audit_events", engine, if_exists="replace", index=False)
permissions_df.to_sql("dim_permissions", engine, if_exists="replace", index=False)

print("ETL Completed Successfully! Your database tables are loaded.")