import boto3
import json

class sns():
    client = boto3.client('sns')
    def sendtoSubscribe(self):
        TOPIC  = 'arn:aws:sns:us-west-2:572845449614:discussion'
        URL    = '<Body of Message in this example I used a url>'
        pub = self.client.publish( TopicArn = TOPIC, Message = URL )

    def subscribe1(self,email):
        TOPIC  = 'arn:aws:sns:us-west-2:572845449614:discussion'
        URL    = '<Body of Message in this example I used a url>'
        response = self.client.subscribe(
        TopicArn='arn:aws:sns:us-west-2:572845449614:discussion',
        Protocol='email',
        Endpoint=email,

        )

    def subscribe1_phone(self,phone):
        TOPIC  = 'arn:aws:sns:us-west-2:572845449614:discussion'
        URL    = '<Body of Message in this example I used a url>'
        response = self.client.subscribe(
        TopicArn='arn:aws:sns:us-west-2:572845449614:discussion',
        Protocol='sms',
        Endpoint=phone,

        )


notification = sns()
#notification.subscribe1()
#notification.sendtoSubscribe()