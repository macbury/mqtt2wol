import os
import os.path
import logging
import sys
import time
import paho.mqtt.client as mqtt
import wakeonlan
from ruamel.yaml import YAML

CONFIG_PATH = os.path.join('./config.yaml')
config = YAML(typ='safe').load(open(CONFIG_PATH))

logging.basicConfig(
  level=logging.INFO,
  format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger('mqtt2rf')

def prepare_client():
  mqtt_config = config['mqtt']
  client = mqtt.Client()

  client.enable_logger(logger)
  client.username_pw_set(mqtt_config['username'], mqtt_config['password'])

  def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_config['command_topic'])

  def on_message(client, userdata, msg):
    logger.info("Got mac address")
    logger.info(msg.payload)
    mac_address = msg.payload.decode('utf-8')
    wakeonlan.send_magic_packet(mac_address)

  client.on_connect = on_connect
  client.on_message = on_message

  logger.info("Connecting to: " + mqtt_config['host'] + " at " + str(mqtt_config['port']))
  client.connect(mqtt_config['host'], mqtt_config['port'], 60)
  logger.info("Starting mqtt loop...")

  client.loop_start()
  return client

def main():
  logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
  )

  try:
    prepare_client()
    while True:
      time.sleep(0.1)
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()
