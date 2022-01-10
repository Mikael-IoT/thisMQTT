import paho.mqtt.client as paho
import random
import time

CLIENT_ID = f'kyh-mqtt-{random.randint(0, 1000)}'
USERNAME = 'kyh_mikael'
PASSWORD = 'passwords'
BROKER = 's11df6c1.eu-central-1.emqx.cloud'
PORT = 15914

print('Choose a subtopic to enter:')
sub_topic = input()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT Broker')
    else:
        print(f'Failed to connect to Broker. Error code {rc}')


def connect_mqtt():
    # Create a MQTT client object
    # Every client has an id.
    print('Enter Username: ')
    userdata = input()
    client = paho.Client(CLIENT_ID, userdata=userdata)
    # Set a username and a password to connect to broker
    client.username_pw_set(USERNAME, PASSWORD)

    # When connection response is received
    # We run the on_connect function
    client.on_connect = on_connect

    # Connect to broker
    client.connect(BROKER, PORT)
    return client


def on_subscribe(client, userdata, mid, granted_qos):

    print('Username: "', userdata, '"')
    print(f'Subscribed to: "{sub_topic}"')
    #print('client:', client)
    #print('mid:', mid)
    #print('qos:', granted_qos)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    client.userdata = userdata
    print(f'new message: {userdata}: {msg.topic}: {payload}')


def subscribe(client):
    # Subscribe on topic

    client.subscribe(f'message:/{sub_topic}')
    client.on_message = on_message


def main():
    client = connect_mqtt()
    # start the paho loop that will
    # spawn a new thread and send and receive messages

    client.loop_start()
    print(f'Now entering: "{sub_topic}"')
    client.on_subscribe = on_subscribe
    subscribe(client)
    time.sleep(1)
    print(f'Successfully entered: "{sub_topic}"')

    while True:
        # Get message from input
        print('Type message >')
        message = input(str())
        # Publish to the topic temperature/room1 with temp
        client.publish(f'message:/{sub_topic}', str(message))
        # Publish message
        print(message)


    client.loop_stop()


if __name__ == '__main__':
    main()

