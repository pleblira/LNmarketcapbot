import ssl
import time
from nostr import RelayManager
from nostr import Event
from nostr import PrivateKey, PublicKey
import os
from dotenv import load_dotenv, find_dotenv
import sys

sys.path.append("nostr")

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

private_key = PrivateKey.from_nsec(os.environ.get("PRIVATE_KEY"))
public_key = os.environ.get("PUBLIC_KEY")

def post_note(content):
    relay_manager = RelayManager()
    with open('relay_list.txt', 'r') as f:
        for line in f:
            relay_manager.add_relay(line.strip())
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    # event = Event(private_key.public_key.hex(), "Hey there " + str(random.randint(3, 9000)), tags=tags)
    event = Event(private_key.public_key.hex(), content)
    # event = Event(private_key.public_key.hex(), "Hey there " + str(random.randint(3, 9000)))
    print(f"event content to be posted is {event.content}")
    print(f"event id to be posted is {event.id}")

    private_key.sign_event(event)

    relay_manager.publish_event(event)
    print("note sent")
    time.sleep(1)

    relay_manager.close_connections()

if __name__ == "__main__":
    post_note(PrivateKey.from_nsec("nsec1kenpmwxye80zh93ugfq0jyq73hepnk3fhj5rytv8drs4sdsycumq5pg8uz"), "test 123", tags=[["e", "262556c024988d7e76d143533d10c09834d20b69a0595800a713c2684c3be988"]])