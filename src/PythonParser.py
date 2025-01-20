import ast

class PythonParser:
    def __init__(self, source):
        self.source = source
        self.data = self.parse()

    def parse(self):
        with open(self.source, 'r', encoding='utf-8') as file:
            source_code = file.read()

        tree = ast.parse(source_code)

        # 데이터 저장 변수
        classes = []
        inheritance = []
        methods = []
        attributes = []
        associations = []
        dependencies = []

        # AST를 순회하며 클래스, 속성, 메서드, 관계 추출
        for node in ast.walk(tree):
            # 클래스 정의 (Class Definition)
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                classes.append(class_name)

                # 상속 관계 추출 (Inheritance)
                if node.bases:
                    parent_classes = [base.id for base in node.bases]
                    inheritance.append((class_name, parent_classes))

                # 클래스 내부 속성 추출 (Attributes)
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        # self.<attribute> 형식의 속성 추출
                        if isinstance(item.targets[0], ast.Attribute) and isinstance(item.targets[0].value, ast.Name) and item.targets[0].value.id == 'self':
                            attribute_name = item.targets[0].attr
                            attributes.append(attribute_name)

                # 클래스 내부 메서드 추출 (Methods)
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = item.name
                        method_params = [arg.arg for arg in item.args.args if arg.arg != 'self']
                        methods.append((method_name, method_params))

            # 의존 관계 (Imports)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    dependencies.append(alias.name)

            # 연관 관계 (Associations)
            elif isinstance(node, ast.Assign):
                # self.<attribute> = OtherClass()와 같은 연관 관계 추출
                if isinstance(node.targets[0], ast.Attribute) and isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        assoc_class = node.value.func.id
                        attribute_name = node.targets[0].attr
                        associations.append((attribute_name, assoc_class))

        # UML 데이터 생성 (간단히 텍스트로 표현)
        uml_data = f"Classes: {', '.join(classes)}\n"
        uml_data += f"Inheritance: {', '.join([f'{cls} inherits {', '.join(bases)}' for cls, bases in inheritance])}\n"
        uml_data += f"Methods: {', '.join([f'{method}({', '.join(params)})' for method, params in methods])}\n"
        uml_data += f"Attributes: {', '.join(attributes)}\n"
        uml_data += f"Associations: {', '.join([f'{attr} -> {assoc}' for attr, assoc in associations])}\n"
        uml_data += f"Dependencies: {', '.join(dependencies)}\n"

        return uml_data

    def getData(self):
        return self.data

