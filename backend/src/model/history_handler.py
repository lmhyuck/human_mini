from sqlalchemy.orm import Session
from table import SearchHistory
from sqlalchemy.sql import func

def insert_search_query(db: Session, user_id: int, query: str):
    """
    특정 유저의 검색 기록을 생성
    [SQL]: INSERT INTO search_histories (user_id, search_query, created_at) VALUES (...)
    """
    db_history = SearchHistory(
        user_id=user_id,
        search_query=query
    )
    
    db.add(db_history)
    db.commit()      # DB에 반영
    db.refresh(db_history)
    return db_history

# [READ] 특정 유저의 '삭제되지 않은' 검색 기록 전체 조회
def get_user_search_histories(db: Session, user_id: int):
    """
    특정 유저(PK)의 기록 중 del_yn이 'N'인 것만 최신순으로 가져오기
    [실행되는 SQL]
    SELECT * FROM search_histories 
    WHERE user_id = :user_id AND del_yn = 'N' 
    ORDER BY created_at DESC;
    """
    return db.query(SearchHistory).filter(
        SearchHistory.user_id == user_id,
        SearchHistory.del_yn == "N"
    ).order_by(SearchHistory.created_at.desc()).all()

# [DELETE] 검색 기록 '소프트 삭제' (단일 항목)
def soft_delete_history(db: Session, history_id: int):
    """
    사용자가 기록을 지워도 DB에는 남겨두되, 서비스상에서는 안 보이게 처리
    [실행되는 SQL]
    1. 대상 조회: SELECT * FROM search_histories WHERE id = :history_id LIMIT 1;
    2. 소프트 삭제 실행: 
    UPDATE search_histories 
    SET del_yn = 'Y', deleted_at = NOW() 
    WHERE id = :history_id;
    """
    db_history = db.query(SearchHistory).filter(SearchHistory.id == history_id).first()
    if db_history:
        db_history.del_yn = "Y"           # 삭제 여부 플래그 변경
        db_history.deleted_at = func.now() # 삭제 시점 기록
        db.commit() # 이 시점에 UPDATE 쿼리가 실행됩니다.
        return True
    return False

# [DELETE] 특정 유저의 히스토리 전체 '소프트 삭제' (일괄 처리)
def soft_delete_all_user_history(db: Session, user_id: int):
    """
    설명: 유저가 '검색 기록 전체 삭제' 버튼을 눌렀을 때 사용
    [실행되는 SQL]
    UPDATE search_histories 
    SET del_yn = 'Y', deleted_at = NOW() 
    WHERE user_id = :user_id AND del_yn = 'N';
    """
    db.query(SearchHistory).filter(
        SearchHistory.user_id == user_id,
        SearchHistory.del_yn == "N"
    ).update({
        "del_yn": "Y",
        "deleted_at": func.now()
    }, synchronize_session=False) # 대량 업데이트 성능 최적화
    db.commit()
    return True