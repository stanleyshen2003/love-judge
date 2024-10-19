from .court import Court
 


class HttpInterface:
    def __init__(self, project):
        self.court = Court(project=project)

    def post(self, data):
        sender = data['sender']
        message = data['messages']
        records = self.court.message_in(user=sender, message=message)
        print(records)
        return {"messages": records, "type": sender}
        

    def get(self, data):
        sender = data['sender']
        if sender == 'boy':
            records = self.court.boy.filtered_records
        else:
            records = self.court.girl.filtered_records
        return {"messages": records, "type": sender}