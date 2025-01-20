from src.PythonParser import PythonParser
from src.MatlabParser import MatlabParser

import os

class ParserFactory:
    @staticmethod
    def get_parser(language, source):
        # 파일 리스트 반환
        files = ParserFactory.get_files_for_language(language, source)

        # 파일 리스트 출력
        print(f"Found {len(files)} {language} file(s) in {source}: {files}")

        # 각 파일에 맞는 파서 객체 생성
        parser_objects = []
        
        for file in files:
            if language == 'python':
                parser_objects.append(PythonParser(file))  # Python 파일에 대해 PythonParser 객체 생성
            elif language == 'matlab':
                parser_objects.append(MatlabParser(file))  # MATLAB 파일에 대해 MatlabParser 객체 생성
            else:
                raise ValueError(f"Unsupported language: {language}")
        
        # 생성된 파서 객체 리스트 반환
        return parser_objects
    @staticmethod
    def get_files_for_language(language, source):
        """
        주어진 경로(source)에서 언어별 파일을 필터링하여 리스트로 반환합니다.
        하위 디렉토리도 포함하여 파일을 검색합니다.
        """
        if not os.path.exists(source):
            raise ValueError(f"Source path {source} does not exist.")
        
        filtered_files = []

        # os.walk()로 하위 경로까지 검색
        for root, dirs, files in os.walk(source):
            # 파일 필터링: 확장자가 python이면 .py, matlab이면 .m 파일만 선택
            if language == 'python':
                filtered_files.extend([os.path.join(root, f) for f in files if f.endswith('.py')])
            elif language == 'matlab':
                filtered_files.extend([os.path.join(root, f) for f in files if f.endswith('.m')])
            else:
                raise ValueError(f"Unsupported language: {language}")

        return filtered_files