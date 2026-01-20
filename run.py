#!/usr/bin/env python3
"""
통합 실행 스크립트 - 예제를 쉽게 실행할 수 있습니다.

사용법:
    python run.py url <URL>
    python run.py browser <URL>
    python run.py 1  # 예제 1 실행
    python run.py 2  # 예제 2 실행
"""

import sys
import subprocess

# 자주 사용하는 예제 URL
EXAMPLES = {
    '1': ('CH1/Url.py', 'http://example.org/'),
    '2': ('CH2/Browser.py', 'http://browser.engineering/examples/xiyouji.html'),
    '3': ('CH3/Browser.py', 'http://browser.engineering/text.html'),
}

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n사용 가능한 예제:")
        for key, (cmd, url) in EXAMPLES.items():
            print(f"  {key}: python run.py {cmd} {url}")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # 예제 번호로 실행
    if command in EXAMPLES:
        script_file, url = EXAMPLES[command]
        subprocess.run([sys.executable, script_file, url])
        return
    
    # 직접 명령으로 실행
    if command == 'url':
        if len(sys.argv) < 3:
            print("URL을 입력해주세요: python run.py url <URL>")
            sys.exit(1)
        subprocess.run([sys.executable, 'URL.py', sys.argv[2]])
    elif command == 'browser':
        if len(sys.argv) < 3:
            print("URL을 입력해주세요: python run.py browser <URL>")
            sys.exit(1)
        subprocess.run([sys.executable, 'Browser.py', sys.argv[2]])
    else:
        print(f"알 수 없는 명령: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()