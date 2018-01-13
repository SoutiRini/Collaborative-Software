import os
import mailbox
import csv

projects = "/Volumes/GoogleDrive/Team Drives/Reflection Distributed Development/data/dev-ml/"

with open('dev-ml.csv', 'w') as f:
    writer = csv.writer(f)
    for project in os.listdir(projects):
        for mbox in os.listdir(os.path.join(projects, project)):
            mb = mailbox.mbox(os.path.join(projects, project, mbox))
            writer.writerow(['project', 'from', 'date', 'subject', 'content'])
            for message in mb:
                if message.is_multipart():
                    content = ''.join(str(part.get_payload(decode = True)) for part in message.get_payload())
                else:
                    content = message.get_payload(decode = True)
                subject = message['subject']
                sender = message['from']
                date = message['date']
                writer.writerow(['project', sender, date, subject, content])
