import threading


class EmailThreading(threading.Thread):
    def __init__(self, email, *args, **kwargs):
        self.email = email
        super().__init__(*args, **kwargs)

    def run(self):
        self.email.send(fail_silently=True)