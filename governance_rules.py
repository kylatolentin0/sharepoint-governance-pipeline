import pandas as pd
from sqlalchemy import create_engine

print("Running Security Analytics Engine...")

# Connect to the local database file we created in the last step
engine = create_engine("sqlite:///sharepoint_governance.db")

print("-" * 50)

# --- RULE 1: STRUCTURAL VULNERABILITY DETECTOR ---
# Check if the "Passwords.txt" file is exposed to "External Users"
query_perm = """
    SELECT Folder_Name, Group_Name, Permission_Level 
    FROM dim_permissions 
    WHERE Folder_Name = 'Passwords.txt' AND Group_Name = 'External Users'
"""
risk_perms = pd.read_sql(query_perm, engine)

if not risk_perms.empty:
    print("🚨 ALERT [RULE 1]: High Risk Permission Found!")
    print("   -> 'Passwords.txt' folder has broken inheritance and allows External Users Read access.")
else:
    print("✅ Rule 1 Clear: No exposed password files detected.")

print("-" * 50)

# --- RULE 2: ANOMALOUS USER BEHAVIOR DETECTOR ---
# Find any user who has downloaded more than 2 files from the system
query_audit = """
    SELECT u.User_Name, COUNT(f.File_ID) as Download_Count 
    FROM fact_audit_events f
    JOIN dim_users u ON f.User_ID = u.User_ID
    JOIN dim_operations o ON f.Op_ID = o.Op_ID
    WHERE o.Operation_Name = 'FileDownloaded'
    GROUP BY u.User_Name
    HAVING Download_Count > 2
"""
mass_downloads = pd.read_sql(query_audit, engine)

if not mass_downloads.empty:
    print("🚨 ALERT [RULE 2]: Potential Mass Download Activity Detected!")
    print("   The following users are flag-triggered for high volume downloads:")
    print(mass_downloads.to_string(index=False))
else:
    print("✅ Rule 2 Clear: No anomalous mass download patterns detected.")

print("-" * 50)
print("Security Analysis Complete.")