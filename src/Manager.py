import argparse
import importlib.util
import os

class Manager:
    def __init__(self, command, language):
        self.command = command
        self.source = os.path.join(os.path.abspath("./"), "src")
        self.input = os.path.join(os.path.abspath("./"), "code")
        self.output = os.path.join(os.path.abspath("./"), "output")
        self.code = os.path.join(os.path.abspath("./"), "code")
        self.language = language
        
    def execute_command(self, command):
        # 명령어 처리 로직
        print(f"Executing command: {command}")
        print(f"Source file: {self.source}")
        print(f"Output file: {self.output}")
        print(f"Language: {self.language}")

        # self.source 경로의 파일에서 함수 import 및 실행
        self.import_and_execute(self.source, command)

    def import_and_execute(self, source_path, command):
        module_name = command 
        file_path = os.path.join(source_path, "process", f"{command}.py")

        if not os.path.exists(file_path):
            print(f"Error: {file_path} does not exist.")
            return

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            print(f"Failed to load module: {file_path}")
            return

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 동적으로 import한 모듈에서 명령어에 해당하는 함수 호출
        if hasattr(module, command):
            command_function = getattr(module, command)
            command_function(self,self.code, self.language)  # 각 함수에 맞는 인자 전달
        else:
            print(f"Command '{command}' not found in {file_path}.")