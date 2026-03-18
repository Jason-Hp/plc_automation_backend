from supabase import create_client
from app.config import settings


class SupabaseService:
    def __init__(self):
        self.client = create_client(settings.supabase_url, settings.supabase_key)
    
    def create_user(self, email: str, password: str, user_role: str):
        """
        Create a new user in Supabase with user_role in app_metadata.
        
        Args:
            email: User email address
            password: User password
            user_role: User role (e.g., 'admin' or 'user')
            
        Returns:
            Response from Supabase auth API
            
        Raises:
            Exception: If user creation fails
        """
        try:
            response = self.client.auth.admin.create_user(
                email=email,
                password=password,
                user_metadata={"email": email},  # Optional: user-visible metadata
                app_metadata={"user_role": user_role}  # Admin-only metadata
            )
            return response
        except Exception as exc:
            raise Exception(f"Failed to create user: {str(exc)}") from exc
