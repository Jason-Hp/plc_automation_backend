from app.utils.supabase_client_util import get_supabase_client


class SupabaseService:
    def __init__(self):
        self.client = get_supabase_client()
        if self.client is None:
            raise RuntimeError("Supabase client is not configured.")
    
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
