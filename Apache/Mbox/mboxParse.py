import mailbox
import csv
import sys
import os

subject_file =[]
body_file = []

data = []

mboxFile = sys.argv[1]
outFolder = sys.argv[2]
mbox = mailbox.mbox(mboxFile)
outFile = os.path.join(outFolder, os.path.splitext(os.path.basename(mboxFile))[0] + '.csv')

for message in mbox:
    print(message['Subject'])
    sub = message['Subject']

    if message.is_multipart():
        content = ''.join([str(part.get_payload(decode=True)) for part in message.get_payload()])
    else:
        content = str(message.get_payload(decode=True))

    subject_file.append(sub)
    body_file.append(content)
    data.append([sub, content])


with open(outFile, 'w') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    # wr.writerow(subject_file)
    # wr.writerow(body_file)
    [wr.writerow(row) for row in data]

# def showMbox(mboxPath):
#     box = mailbox.mbox(mboxPath)
#     for msg in box:
#         print(msg['Subject'])
#
#         showPayload(msg)
#
#         print ()
#         print ('**********************************')
#         print ()
#
# def showPayload(msg):
#     payload = msg.get_payload()
#
#     if msg.is_multipart():
#         div = ''
#         for subMsg in payload:
#             print(div)
#             showPayload(subMsg)
#             div = '------------------------------'
#     else:
#         # print(msg.get_content_type())
#         print(payload[:200])
#
# if __name__ == '__main__':
#     showMbox('201203.mbox')