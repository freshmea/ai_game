import importlib
import pkgutil
import sys

import pygame.examples
import pygame.examples.aliens


def main():
    """메인 엔트리 포인트.
    
    argv를 파싱하여 pygame.examples 폴더 내의 게임 예제를 실행하거나,
    argv가 없을 경우 사용 가능한 예제 리스트를 출력합니다.
    """
    print("Hello from ai-game!")
    if len(sys.argv) == 1:
        print("사용 가능한 예제:")
        for finder, name, ispkg in pkgutil.iter_modules(pygame.examples.__path__):
            print(" -", name)
        return
    example_name = sys.argv[1]
    module_name = "pygame.examples." + example_name
    try:
        example_module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"예제 '{example_name}'를 찾을 수 없습니다.")
        return
    if hasattr(example_module, "main"):
        example_module.main()
    else:
        print(f"예제 '{example_name}'에 main() 함수가 없습니다.")

if __name__ == "__main__":
    main()

# 2023-10-04
