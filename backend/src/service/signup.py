
import bcrypt
from sqlalchemy import text
from util.database import engine


 # 클라이언트가 입력한 데이터 삽입 / register_user() 함수에서 가공 후 삽입
def save_user_to_db(
    username: str, 
    hashed_password: str, 
    full_name: str, 
    email: str, 
    gender: str,
    birth_date = None,           # NULL 허용
    phone_number = None,         # NULL 허용
    telecom_provider = None      # NULL 허용
    ):
    # 멀티라인 방식으로 쿼리 작성
    query = text("""
        INSERT INTO users (
            username, hashed_password, full_name, email, gender,
            birth_date, phone_number, telecom_provider,
            social_provider, is_verified
        )
        VALUES (
            :username, :hashed_password, :full_name, :email, :gender,
            :birth_date, :phone_number, :telecom_provider,
            :social_provider, :is_verified
        )
    """)
    with engine.begin() as conn:
        conn.execute(query, {
            "username": username,
            "hashed_password": hashed_password,
            "full_name": full_name,
            "email": email,
            "gender": gender,
            "birth_date": birth_date,            # None이면 NULL로 들어감
            "phone_number": phone_number,        # None이면 NULL로 들어감
            "telecom_provider": telecom_provider, # None이면 NULL로 들어감
            "social_provider": "local",          # 기본값 고정
            "is_verified": False                 # 기본값 고정
        })
            

# 회원 등록  
async def register_user(
    username: str,
    password: str,
    full_name: str,
    email: str,
    gender: str,
    birth_date=None,
    phone_number=None,
    telecom_provider=None
):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_str = hashed.decode('utf-8')
    save_user_to_db(
        username=username,
        hashed_password=hashed_str,
        full_name=full_name,
        email=email,
        gender=gender,
        birth_date=birth_date,
        phone_number=phone_number,
        telecom_provider=telecom_provider
    )        