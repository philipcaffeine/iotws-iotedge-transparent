
### Tutorial Create transparent gateway

1. Configure IoT Edge as Transparent Gateway 
2. List of parameters:


###　1. Configure IoT Edge as Transparent Gateway 

A Linux or Windows device with IoT Edge installed. - If you do not have a device ready, you can create one in an Azure virtual machine. Follow the steps in Deploy your first IoT Edge module to a virtual Linux device to create an IoT Hub, create a virtual machine, and configure the IoT Edge runtime.

Ubuntu 20

#### Create a linux VM on Azure, Ubuntu 20, set bastion net

```hcl
```

```hcl
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

sudo apt-get update
sudo apt-get install moby-engine
```

```hcl
vi /etc/docker/daemon.json

{
      "log-driver": "local"
}

```

```hcl
sudo apt-get update
sudo apt-get install aziot-edge
```


#### Prepare and Install IoT Edge Cont’ 

Create IOT Edge device on IoT Hub, get connection string 
HostName=phil-ws-iothub01.azure-devices.net;DeviceId=phil-iotedge01;SharedAccessKey=98HanxyPyJM1AjpubxAIj+xccoP8ZJjGuyGuQm+scX4=

HostName=phil-ws-iothub01.azure-devices.net;DeviceId=phil-iotedge02;SharedAccessKey=lnewRjJ7B2LtSf3ZdOIPE5arY/55hIZXkYLQVpMcTfo=

**** IMPORTANT ****
DO NOT START NEW IOTEDGE until you modify all cert path in config.toml, or the new iot edge will wrongly generate wrong server certificate 


** below commands used after all steps after this deck ***


```hcl
sudo iotedge system status

sudo iotedge system logs

sudo iotedge check
```


###　2. Set up the device CA certificate

https://learn.microsoft.com/en-us/azure/iot-edge/how-to-create-test-certificates?view=iotedge-2020-11&tabs=windows

Move cert files to VM	

####  How to Make Direct Link of OneDrive Files | Mars Translation

Onedrive >> embed  >> get and change URL
Make changes in the URL. Just replace 'embed' with   'download'. After making changes, you URL will be look like below,

For example: 
mkdir keys_certs

wget -O azure-iot-test-only.root.ca.cert.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21330311&authkey=AKAW5MB_AIjallk"

---IoT Edge 01
wget -O iot-edge-device-edgeca-phil-iotedge01.key.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21329422&authkey=AEeTFCzlfv-oVl0"

wget -O iot-edge-device-edgeca-phil-iotedge01-full-chain.cert.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21329423&authkey=AF-GVM7cZ7Fy52U"

--- IoT Edge 02 
wget -O iot-edge-device-edgeca-phil-iotedge02.key.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21329435&authkey=AKOkHHWLu0UjCrQ" 

wget -O iot-edge-device-edgeca-phil-iotedge02-full-chain.cert.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21329437&authkey=AKyEs-B0A0vNG6E"


####  Grant inbound access from leaf device to IoT Edge

Add inbound firewall rule of IOT Edge VM 

Port	Protocol

8883	MQTT/ MQTT+WS

5671	AMQP / AMQP+WS

443	HTTPS


###　3. Configure IoT Edge – config.toml


On your IoT Edge device, 
Backup file
cp /etc/aziot/config.toml /etc/aziot/config.toml.back
Copy template file 
cp ./config.toml.edge.template ./config.toml

vi ./config.toml
hostname = “phil-iotedge01.southeastasia.cloudapp.azure.com”　# need to set for certificate generation, cannot mismatch 
Find the trust_bundle_cert parameter. Uncomment this line and provide the file URI to the root CA certificate file on your device.
trust_bundle_cert = "file:///home/philadmin/keys_certs/azure-iot-test-only.root.ca.cert.pem"

Find the [edge_ca] section of the file. Uncomment the three lines in this section and provide the file URIs to your certificate and key files as values for the following properties:
cert: device CA certificate
pk: device CA private key
[edge_ca]
cert = "file:///home/philadmin/keys_certs/iot-edge-device-edgeca-phil-iotedge01-full-chain.cert.pem"      # file URI
pk = "file:///home/philadmin/keys_certs/iot-edge-device-edgeca-phil-iotedge01.key.pem"              # file URI, or...

Add provision section config.toml 
[provisioning]
source = "manual"
connection_string = "HostName=phil-ws-iothub01.azure-devices.net;DeviceId=phil-iotedge02;SharedAccessKey=lnewRjJ7B2LtSf3ZdOIPE5arY/55hIZXkYLQVpMcTfo=" 

sudo iotedge config apply

Note:  sudo iotedge system stop && sudo docker rm -f $(docker ps -aq) && sudo iotedge config apply　# use this command, if to change hostname

### 4. Config IoT Edge – create hub route

In the Azure portal, navigate to your IoT hub.Go to IoT Edge and select your IoT Edge device that you want to use as a gateway.
Select Set Modules.

On the Modules page, you can add any modules you want to deploy to the gateway device. For the purposes of this article we're focused on configuring and deploying the edgeHub module, which doesn't need to be explicitly set on this page.

Select Next: Routes.

On the Routes page, make sure that there is a route to handle messages coming from downstream devices. For example:

A route that sends all messages, whether from a module or from a downstream device, to IoT Hub:

Name: allMessagesToHub
Value: FROM /messages/* INTO $upstream
A route that sends all messages from all downstream devices to IoT Hub:

Name: allDownstreamToHub
Value: FROM /messages/* WHERE NOT IS_DEFINED ($connectionModuleId) INTO $upstream

### 5. Prepare downstream device – authentication to hub

Create a new leaf device in your IoT Hub, select it’s parent device (the IoT Edge), and copy the connection string 


