from repository.database import Database
from model.user_model import User, UserInfo

QUERY_SELECT_ONE_USER = """
            SELECT 
                *
            FROM \"user\" 
            WHERE email = %s
            LIMIT 1
        """

class UserRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()
    
    def get_query_by_email(self, email: str) -> User:
        self.cursor.execute(QUERY_SELECT_ONE_USER, [email])
        obj = self.cursor.fetchone()
        
        if obj is None:
            return None

        user = User(
                id=obj[0],
                email=obj[1],
                password=obj[2],
                full_name=obj[3],
                created_at=str(obj[4]),
                updated_at=str(obj[5]),
                disabled=obj[6])
        return user

    def get_query_by_email(self, email: str) -> UserInfo:
        self.cursor.execute(QUERY_SELECT_ONE_USER, [email])
        obj = self.cursor.fetchone()
        
        if obj is None:
            return None

        user = User(
            id=obj[0],
            email=obj[1],
            password=obj[2],
            full_name=obj[3],
            created_at=str(obj[4]),
            updated_at=str(obj[5]),
            disabled=obj[6])
        return user