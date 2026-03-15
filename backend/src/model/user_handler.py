from sqlalchemy.orm import Session
from table import User 
from sqlalchemy.sql import func
from table.user import User, GenderEnum

def create_user(
    db: Session, 
    username: str, 
    password: str, 
    full_name: str, 
    email: str, 
    birth_date, 
    gender: str, 
    social_provider: str = "local",
    social_id: str = None,
    phone_number: str = None,
    telecom_provider: str = None
):
    try:
        gender_enum = GenderEnum(gender)
    except ValueError:
        # 혹시 '남'/'녀'가 아닌 값이 들어올 경우를 대비한 기본값 또는 에러 처리
        raise ValueError("성별은 '남' 또는 '녀'여야 합니다.")

    # 2. 유저 객체 생성 (id는 자동 생성되므로 제외)
    db_user = User(
        username=username,
        hashed_password=f"hash_{password}", # 실무에선 비밀번호 암호화 필수
        full_name=full_name,
        email=email,
        birth_date=birth_date,
        gender=gender_enum,
        social_provider=social_provider,
        social_id=social_id,
        phone_number=phone_number,
        is_verified=True,  # 테스트를 위해 기본 true 설정
        telecom_provider=telecom_provider
    )
    
    db.add(db_user)
    db.commit()      # DB에 확정 저장
    db.refresh(db_user) # DB에서 생성된 id, created_at 등을 다시 불러옴
    
    return db_user

# 로그인 로직 -> username 기반 조회
# 수정/삭제/히스토리 연동 -> id 기반 조회 사용
# [READ] 통합 조회 함수
def get_user(db: Session, user_id: int = None, username: str = None):
    """
    SQL: SELECT * FROM users WHERE id = :user_id LIMIT 1;
    """
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    """
    SQL: SELECT * FROM users WHERE username = :username LIMIT 1;
    """
    if username:
        return db.query(User).filter(User.username == username).first()
    return None

# [UPDATE] 회원 정보 수정
def update_user_info(db: Session, user_id: int, update_data: dict):
    """
    SQL: UPDATE users SET full_name = '...', email = '...' WHERE id = :user_pk;
    """
    # 1. 수정할 대상을 PK로 조회
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user:
        # 2. update_data에 담긴 키(컬럼명)와 값을 반복하며 업데이트
        for key, value in update_data.items():
            # 모델에 해당 컬럼명(username, full_name 등)이 존재하는지 확인
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        
        # 3. 변경사항 저장
        db.commit()
        # 4. 수정된 데이터로 파이썬 객체 동기화
        db.refresh(db_user)
        return db_user
    return None

# [DELETE] 회원 탈퇴 (물리적 삭제)
def delete_user(db: Session, user_id: int):
    """
    SQL: DELETE FROM users WHERE id = :user_pk;
    """
    # 1. 삭제할 유저 조회
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user:
        # 2. 세션에서 삭제 대상으로 등록
        db.delete(db_user)
        # 3. DB에 삭제 명령 반영 (실제 데이터 소멸)
        db.commit()
        return True
    return False