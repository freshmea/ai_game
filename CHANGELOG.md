# 개발 로그

## [0.0.5] - 2023-10-04
### 추가
- snake와 food 충돌 시 화면 맨 아래에 "충돌 발생" 메시지 표시 기능 추가

## [0.0.4] - 2023-10-24
### 추가
- sphinx 를 이용한 html 오류를 해결함

## [0.0.3] - 2025-1-24
### 추가
- 파이테스트 에러 해결, 패키지 절대 경로를 추가함
```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
```

## [0.0.2] - 2025-1-23
### 추가
- 게임 초기 버전 구현
- Snake, Food, Game, Settings 클래스 추가
- 게임 로직 및 화면 업데이트 기능 구현

## [0.0.1] - 2025-1-23
### pygame 기초 로직
- 게임 초기 버전 구현
- Snake, Food, Game, Settings 클래스 추가
- 게임 로직 및 화면 업데이트 기능 구현
