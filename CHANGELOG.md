# 개발 로그

## [0.0.3] - 2023-10-XX
### 추가
- 파이테스트 에러 해결, 패키지 절대 경로를 추가함
```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
```

## [0.0.2] - 2023-10-XX
### 추가
- 게임 초기 버전 구현
- Snake, Food, Game, Settings 클래스 추가
- 게임 로직 및 화면 업데이트 기능 구현


## [0.0.1] - 2023-10-XX
### pygame 기초 로직
- 게임 초기 버전 구현
- Snake, Food, Game, Settings 클래스 추가
- 게임 로직 및 화면 업데이트 기능 구현
