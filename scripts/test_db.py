from httpx import RequestError
from postgrest.exceptions import APIError
from supabase import SupabaseException

from ethico.database import create_supabase_client

try:
    client = create_supabase_client()

    response = client.table("conversations").select("*").limit(1).execute()

    print("Database connection successful!")
    print(response.data)

except (ValueError, SupabaseException) as e:
    print("Supabase configuration error:", e)

except APIError as e:
    print("Database query failed:", e)

except RequestError as e:
    print("Database connection failed:", e)
