# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import uuid
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message, X509
import asyncio

messages_to_send = 100

async def main():
    hostname = "phil-edge01.southeastasia.cloudapp.azure.com"
    # The device that has been created on the portal using X509 CA signing or Self signing capabilities
    device_id = "phil-leaf01"

    x509 = X509(
        cert_file= "C:\\Users\\yec\\OneDrive\\dev_cloud\\vs_code\\_common_iot\\01-device_sdk\\_keys_and_certs\\self-signed-iotedge-20221031\\certs\\iot-device-phil-leaf01-full-chain.cert.pem",
        key_file= "C:\\Users\\yec\\OneDrive\\dev_cloud\\vs_code\\_common_iot\\01-device_sdk\\_keys_and_certs\\self-signed-iotedge-20221031\\private\\iot-device-phil-leaf01.key.pem",
        pass_phrase=""
    )

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_x509_certificate(
        hostname=hostname, device_id=device_id, x509=x509
    )

    # Connect the client.
    await device_client.connect()

    async def send_test_message(i):
        print("sending message #" + str(i))
        msg = Message("test wind speed " + str(i))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-1234"
        msg.custom_properties["tornado-warning"] = "yes"
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        await device_client.send_message(msg)
        print("done sending message #" + str(i))

    # send `messages_to_send` messages in parallel
    await asyncio.gather(*[send_test_message(i) for i in range(1, messages_to_send + 1)])

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()