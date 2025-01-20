import re

class MatlabParser:
    def __init__(self, source):
        self.source = source
        self.data = self.parse()

    def parse(self):
        with open(self.source, 'r', encoding='latin-1') as file:
            source_code = file.read()

        # 데이터 저장 변수
        classes = []
        inheritance = []
        methods = []
        attributes = []
        associations = []
        dependencies = []

        # MATLAB 클래스 정의 정규식
        class_pattern = r'classdef\s+(\w+)\s*(?:<\s*(\w+))?'  # 클래스와 상속 처리
        attribute_pattern = r'\s*(\w+)\s*=\s*.*'  # 속성 추출 (단순히 '=' 사용)
        dependency_pattern = r'addpath\(.*\)'  # 의존 관계 (addpath로 라이브러리 추가하는 경우)
        association_pattern = r'self\.(\w+)\s*=\s*(\w+)\(\)'  # 연관 관계 추출 (self.<attribute> = OtherClass())

        # 클래스 정의 추출
        class_matches = re.findall(class_pattern, source_code)
        for class_match in class_matches:
            class_name = class_match[0]
            parent_class = class_match[1] if class_match[1] else None
            classes.append(class_name)
            if parent_class:
                inheritance.append((class_name, parent_class))

        # 메서드 정의 추출
        method_matches = self.extract_methods(source_code)

        for method in method_matches:
            method_name = method
            methods.append(method_name)  # 메서드 이름 전체를 추가

        # 속성 정의 추출
        attribute_matches = re.findall(attribute_pattern, source_code)
        for attribute in attribute_matches:
            attributes.append(attribute)

        # 의존 관계 추출 (addpath 사용)
        dependency_matches = re.findall(dependency_pattern, source_code)
        for dependency in dependency_matches:
            dependencies.append(dependency)

        # 연관 관계 추출 (self.<attribute> = OtherClass() 형태)
        association_matches = re.findall(association_pattern, source_code)
        for assoc in association_matches:
            attribute_name, assoc_class = assoc
            associations.append((attribute_name, assoc_class))

        # UML 데이터 생성 (간단히 텍스트로 표현)
        uml_data = f"Classes: {', '.join(classes)}\n"
        uml_data += f"Inheritance: {', '.join([f'{cls} inherits {parent}' for cls, parent in inheritance])}\n"
        uml_data += f"Methods: {', '.join(methods)}\n"  # 메서드 이름 전체를 출력
        uml_data += f"Attributes: {', '.join(attributes)}\n"
        uml_data += f"Associations: {', '.join([f'{attr} -> {assoc}' for attr, assoc in associations])}\n"
        uml_data += f"Dependencies: {', '.join(dependencies)}\n"

        return uml_data

    def getData(self):
        return self.data
    def extract_methods(self,code):
        methods = []
        lines = code.splitlines()
        
        for line in lines:
            # Trim whitespace and check if the line starts with "function"
            line = line.strip()
            if line.startswith("function"):
                # Extract the method signature, excluding the 'function' keyword
                parts = line.split("function")[1].strip()

                # Separate method name and arguments
                if "(" in parts and ")" in parts:
                    method_name = parts.split("(")[0].strip()
                    arguments = parts.split("(")[1].split(")")[0].strip()
                    
                    # Format method with arguments
                    formatted_method = f"{method_name}({arguments})" if arguments else f"{method_name}()"
                    methods.append(formatted_method)
        
        return methods