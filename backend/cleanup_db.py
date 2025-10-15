"""
Utility script to clear all data from 'transactions' and 'test_runs' tables.
Uses the existing Supabase client from db.py.
"""

from db import supabase

def clear_table(table_name):
    try:
        records = supabase.table(table_name).select("id").execute().data
        if not records:
            print(f"⚠️ Table '{table_name}' already empty.")
            return

        ids = [r["id"] for r in records]
        print(f"🧹 Deleting {len(ids)} rows from '{table_name}'...")

        for record_id in ids:
            supabase.table(table_name).delete().eq("id", record_id).execute()

        print(f"✅ Cleared table '{table_name}' successfully.\n")

    except Exception as e:
        print(f"❌ Error clearing '{table_name}': {e}")

def truncate_tables():
    clear_table("transactions")
    clear_table("test_runs")

if __name__ == "__main__":
    truncate_tables()
