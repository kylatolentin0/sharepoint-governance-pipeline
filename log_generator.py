import pandas as pd
from faker import Faker
import random

fake = Faker()

users = [fake.user_name() for _ in range(10)]
files = ["Project_Plan.docx", "Financial_Q4.xlsx", "Passwords.txt", "Architecture_Diagram.pdf", "HR_Policy.pdf"]
operations = ["FileDownloaded", "FileModified", "PermissionInheritanceBroken", "FileSharedExternal"]

audit_data = []
for _ in range(100):
    audit_data.append({
        "Timestamp": fake.date_time_this_month(),
        "User": random.choice(users),
        "Operation": random.choice(operations),
        "Item_Name": random.choice(files)
    })
pd.DataFrame(audit_data).to_csv("sharepoint_audit_events.csv", index=False)

permissions_data = []
for f in files:
    permissions_data.append({
        "Folder_Name": f,
        "Group_Name": "External Users" if f == "Passwords.txt" else "Members",
        "Permission_Level": "Read" if f == "Passwords.txt" else "Full Control"
    })
pd.DataFrame(permissions_data).to_csv("site_permissions_matrix.csv", index=False)

print("Raw CSV files generated successfully!")