# ai_game

## 프로젝트 설명
이 프로젝트는 파이썬과 Pygame을 사용하여 만든 간단한 지렁이(뱀) 게임입니다. 플레이어는 지렁이를 조종하여 음식을 먹고 점수를 올리는 것이 목표입니다.

## 파일 구조
```
ai_game/
│
├── src/
│   └── snake/
│       ├── data/
│       │   └── game_scores.db        # 게임 점수 데이터베이스
│       ├── main.py                   # 게임의 진입점
│       ├── game.py                   # 게임 로직
│       ├── snake.py                  # 지렁이(뱀) 클래스
│       ├── food.py                   # 음식 클래스
│       ├── models.py                 # 게임 점수 모델
│       ├── settings.py               # 게임 설정
│       ├── wall.py                   # 벽 클래스
│       └── ui.py                     # UI 클래스
└── README.md                         # 프로젝트 설명 파일
```

## 필요 라이브러리
- Python 3.x
- uv

## 설치 방법
1. Python 3.x를 설치합니다.
2. uv를 이용하여 Pygame 라이브러리를 설치합니다:
    ```
    uv sync
    ```

## 실행 방법
1. 프로젝트 디렉토리로 이동합니다:
    ```
    cd /c:/Users/Administrator/Documents/ai_game/
    ```
2. 게임을 실행합니다:
    ```
    uv run python src/main.py
    ```

## 게임 방법
- 방향키를 사용하여 지렁이를 조종합니다.
- 지렁이가 음식을 먹으면 길이가 길어집니다.
- 지렁이가 벽이나 자기 자신과 충돌하면 게임이 종료됩니다.

## 기술 스택
- Python 3.x
- Pygame
- sphinx
- pytest
- copilot

## 버전
- 0.0.7