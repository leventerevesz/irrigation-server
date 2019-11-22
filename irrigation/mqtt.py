import paho.mqtt.client as mqtt
#from weather.management.commands.tankmqtt import save_tanklevel

def on_connect(client, userdata, rc):
    client.subscribe("/tanklevel")

def on_message(client, userdata, msg):
    #if (msg.topic == "/tanklevel"):
    #    save_tanklevel(msg)
    pass

client = mqtt.Client(client_id="Django")
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)