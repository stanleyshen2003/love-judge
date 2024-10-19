from .court import Court
 


class HttpInterface:
    def __init__(self, project):
        self.court = Court(project=project)

    def post(self, data):
        sender = data['sender']
        message = data['message']
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
    
    def get_lawyer(self, user):
        if user == 'boy':
            return self.court.boy.lawyer_records
        else:
            return self.court.girl.lawyer_records
    
    def post_lawyer(self, data):
        sender = data['sender']
        message = data['message']
        
        if sender == 'boy':
            return self.court.boy.ask_lawyer(message)
        else:
            return self.court.girl.ask_lawyer(message)