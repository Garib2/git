def CreateParser(self, source, language):
    from src.ParserFactory import ParserFactory
    from src.UMLGenerator import UMLGenerator
    data=ParserFactory.get_parser(language,source)
    Data=[]
    for i in data:
        Data.append(UMLGenerator(i.getData()))
    return Data