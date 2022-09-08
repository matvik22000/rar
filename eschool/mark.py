class Mark:
    def __init__(self, arr: dict):
        self.markDate: str = str(arr["markDate"])
        self.markId: str = str(arr["markId"])
        self.markVal: str = str(arr["markVal"])
        self.mktWt: str = str(arr["mktWt"])
        self.subject: str = str(arr["subject"])
        self.teachFio: str = str(arr["teachFio"])
        self.isUpdated: str = str(arr["isUpdated"])
        self.unitId: str = str(arr["unitId"])
        self.startDate: str = str(arr["startDt"])
        self.lessonId: str = str(arr["lessonId"])

    def __repr__(self):
        return str(f'mark:{self.markVal} coef:{self.mktWt} subject: "{self.subject}"')


