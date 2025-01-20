
class UMLGenerator:
    def __init__(self, uml_data):
        self.uml_data = uml_data
        self.classes = []
        self.inheritance = []
        self.methods = []
        self.attributes = []
        self.associations = []
        self.dependencies = []
        self.parse_uml_data()

    def parse_uml_data(self):
        """
        주어진 UML 데이터를 파싱하여 클래스를 구성하는 요소들로 나눕니다.
        """
        lines = self.uml_data.split("\n")
        
        for line in lines:
            # Classes
            if line.startswith("Classes:"):
                self.classes = line[len("Classes: "):].split(", ")
            # Inheritance
            elif line.startswith("Inheritance:"):
                inheritance_data = line[len("Inheritance: "):]
                self.inheritance = [tuple(i.split(" inherits ")) for i in inheritance_data.split(", ")]
            # Methods
            elif line.startswith("Methods:"):
                methods_data = line[len("Methods: "):]
                self.methods = [tuple(m.split("(")) for m in methods_data.split(", ")]
            # Attributes
            elif line.startswith("Attributes:"):
                self.attributes = line[len("Attributes: "):].split(", ")
            # Associations
            elif line.startswith("Associations:"):
                associations_data = line[len("Associations: "):]
                self.associations = [tuple(a.split(" -> ")) for a in associations_data.split(", ")]
            # Dependencies
            elif line.startswith("Dependencies:"):
                self.dependencies = line[len("Dependencies: "):].split(", ")

    def generate_plantuml(self):
        """
        UML 데이터를 기반으로 PlantUML 코드 생성
        """
        uml_code = "@startuml\n"

        # 1. 클래스 정의
        for cls in self.classes:
            uml_code += f"class {cls} {{}}\n"
        
        # 2. 상속 관계
        for class_name, parents in self.inheritance:
            for parent in parents:
                uml_code += f"{class_name} <|-- {parent}\n"

        # 3. 속성 정의
        for cls in self.classes:
            for attribute in self.attributes:
                uml_code += f"class {cls} {{\n"
                uml_code += f"  +{attribute}\n"
                uml_code += f"}}\n"

        # 4. 메서드 정의
        for method_name, params in self.methods:
            for cls in self.classes:
                param_str = ", ".join(params.split(","))
                uml_code += f"class {cls} {{\n"
                uml_code += f"  +{method_name}({param_str})\n"
                uml_code += f"}}\n"

        # 5. 연관 관계 (Associations)
        for attr, assoc_class in self.associations:
            uml_code += f"{attr} --> {assoc_class}\n"

        # 6. 의존 관계 (Dependencies)
        for dep in self.dependencies:
            uml_code += f"..> {dep}\n"

        uml_code += "@enduml\n"
        
        return uml_code

