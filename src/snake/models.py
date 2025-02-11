"""
SQLModel을 사용한 게임 점수 모델 정의
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class GameScore(SQLModel, table=True):
    """게임 점수를 저장하는 모델"""
    id: Optional[int] = Field(default=None, primary_key=True)
    player_initials: str = Field(max_length=3)
    score: int
    play_time: float
    played_at: datetime = Field(default_factory=datetime.now)

# DB 엔진 설정
engine = create_engine("sqlite:///game_scores.db", echo=False)

def create_db_and_tables():
    """데이터베이스와 테이블을 생성합니다."""
    SQLModel.metadata.create_all(engine)

def save_score(player_initials: str, score: int, play_time: float):
    """
    게임 점수를 저장합니다.
    
    매개변수:
    player_initials (str): 플레이어 이니셜
    score (int): 획득 점수
    play_time (float): 플레이 시간
    """
    with Session(engine) as session:
        game_score = GameScore(
            player_initials=player_initials,
            score=score,
            play_time=play_time
        )
        session.add(game_score)
        session.commit()

def get_high_scores(limit: int = 5) -> list[GameScore]:
    """
    상위 점수를 가져옵니다.
    
    매개변수:
    limit (int): 가져올 기록 수
    
    반환값:
    list[GameScore]: 상위 점수 목록
    """
    with Session(engine) as session:
        statement = select(GameScore).order_by(GameScore.score.desc()).limit(limit)
        return session.exec(statement).all()

# 2023-10-24