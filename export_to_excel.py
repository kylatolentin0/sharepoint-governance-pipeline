import pandas as pd
from sqlalchemy import create_engine

# Connect to your SQLite database file
engine = create_engine("sqlite:///sharepoint_governance.db")

# Read the tables out of the database
dim_users = pd.read_sql("SELECT * FROM dim_users", engine)
dim_files = pd.read_sql("SELECT * FROM dim_files", engine)
dim_operations = pd.read_sql("SELECT * FROM dim_operations", engine)
fact_audit = pd.read_sql("SELECT * FROM fact_audit_events", engine)
dim_permissions = pd.read_sql("SELECT * FROM dim_permissions", engine)

# Save them all into a single Excel file with separate tabs
with pd.ExcelWriter("sharepoint_data_model.xlsx") as writer:
    fact_audit.to_excel(writer, sheet_name="fact_audit_events", index=False)
    dim_users.to_excel(writer, sheet_name="dim_users", index=False)
    dim_files.to_excel(writer, sheet_name="dim_files", index=False)
    dim_operations.to_excel(writer, sheet_name="dim_operations", index=False)
    dim_permissions.to_excel(writer, sheet_name="dim_permissions", index=False)

print("Success! Your complete data model has been exported to sharepoint_data_model.xlsx")