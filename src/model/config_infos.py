class Config:
    fieldnames = []
    dateField = 'Year'
    timeField = 'Max'
    typeField = 'Type'

    def __init__(self, email, fieldnames):
        self.email = email
        for field in fieldnames:
            self.fieldnames.append(field)


class Params:
    continuumImages = 0
    aiaSixImages = 0
    aiaSevenImages = 0
    existingImages = 0
    invalidLines = 0
