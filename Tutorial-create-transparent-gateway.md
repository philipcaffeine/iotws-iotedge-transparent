
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
sudo apt-get update
sudo apt-get install aziot-edge
```


#### Prepare and Install IoT Edge Cont’ 

Create IOT Edge device on IoT Hub, get connection string 

Sample as below: 

```hcl
HostName=phil-ws-iothub-01.azure-devices.net;DeviceId=phil-edge01;SharedAccessKey=xxxx
```


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

Have the following files ready:

Root CA certificate
Device CA certificate
Device CA private key

Move cert files to VM	

####  How to Make Direct Link of OneDrive Files | Mars Translation
https://www.marstranslation.com/blog/how-to-make-direct-link-of-onedrive-files

Onedrive >> embed  >> get and change URL. Make changes in the URL. Just replace 'embed' with   'download'. After making changes, you URL will be look like below,

For example: 

```hcl
mkdir keys_certs

wget -O azure-iot-test-only.root.ca.cert.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21337877&authkey=AOeLedZOLpAbtWQ"

---IoT Edge 01

wget -O iot-edge-device-edgeca-phil-edge01.key.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21337878&authkey=AJo39JBqR5XTGeg"

wget -O iot-edge-device-edgeca-phil-edge01-full-chain.cert.pem --no-check-certificate "https://onedrive.live.com/download?cid=584B560B6F9BE190&resid=584B560B6F9BE190%21337879&authkey=AJfhz-2Y51iBhK4"

```


####  Grant inbound access from leaf device to IoT Edge

```hcl
Add inbound firewall rule of IOT Edge VM 

Port	Protocol

8883	MQTT/ MQTT+WS

5671	AMQP / AMQP+WS

443	    HTTPS
```


###　3. Configure IoT Edge – config.toml


On your IoT Edge device, 
Backup file

```hcl
```

Copy template file 

```hcl
cp /etc/aziot/config.toml.edge.template /etc/aziot/config.toml
```

```hcl
vi ./config.toml

hostname = "phil-edge01.southeastasia.cloudapp.azure.com"　# need to set for certificate generation, cannot mismatch 
```

Find the trust_bundle_cert parameter. Uncomment this line and provide the file URI to the root CA certificate file on your device.

```hcl
trust_bundle_cert = "file:///home/philadmin/keys_certs/azure-iot-test-only.root.ca.cert.pem"
```


Find the [edge_ca] section of the file. Uncomment the three lines in this section and provide the file URIs to your certificate and key files as values for the following properties:
cert: device CA certificate
pk: device CA private key

```hcl
[edge_ca]
cert = "file:///home/philadmin/keys_certs/iot-edge-device-edgeca-phil-edge01-full-chain.cert.pem"      # file URI
pk = "file:///home/philadmin/keys_certs/iot-edge-device-edgeca-phil-edge01.key.pem"              # file URI, or...

```

Add provision section config.toml 

```hcl
[provisioning]
source = "manual"
connection_string = "HostName=xxx.azure-devices.net;DeviceId=phil-edge01;SharedAccessKey=xxxxxx" 
```

```hcl
sudo iotedge config apply

iotedge logs -f edgeAgent
```

Note:  sudo iotedge system stop && sudo docker rm -f $(docker ps -aq) && sudo iotedge config apply　# use this command, if to change hostname


<6> 2022-10-31 05:41:51.695 +00:00 [INF] - Initializing Edge Agent.
<6> 2022-10-31 05:41:51.798 +00:00 [INF] - Version - 1.4.2.61356014 (bb9a26162c4c88b3ef9a50d33632ab78bd4247d6)
<6> 2022-10-31 05:41:51.798 +00:00 [INF] -
        █████╗ ███████╗██╗   ██╗██████╗ ███████╗
       ██╔══██╗╚══███╔╝██║   ██║██╔══██╗██╔════╝
       ███████║  ███╔╝ ██║   ██║██████╔╝█████╗
       ██╔══██║ ███╔╝  ██║   ██║██╔══██╗██╔══╝
       ██║  ██║███████╗╚██████╔╝██║  ██║███████╗
       ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

 ██╗ ██████╗ ████████╗    ███████╗██████╗  ██████╗ ███████╗
 ██║██╔═══██╗╚══██╔══╝    ██╔════╝██╔══██╗██╔════╝ ██╔════╝
 ██║██║   ██║   ██║       █████╗  ██║  ██║██║  ███╗█████╗
 ██║██║   ██║   ██║       ██╔══╝  ██║  ██║██║   ██║██╔══╝
 ██║╚██████╔╝   ██║       ███████╗██████╔╝╚██████╔╝███████╗
 ╚═╝ ╚═════╝    ╚═╝       ╚══════╝╚═════╝  ╚═════╝ ╚══════╝

<6> 2022-10-31 05:41:51.800 +00:00 [INF] - ModuleUpdateMode: NonBlocking
<6> 2022-10-31 05:41:51.828 +00:00 [INF] - Experimental features configuration: {"Enabled":false,"DisableCloudSubscriptions":false}
<6> 2022-10-31 05:41:51.935 +00:00 [INF] - Installing certificates [CN=iot-edge-1027.ca:11/26/2022 06:49:54],[CN=Azure_IoT_Hub_Intermediate_Cert_Test_Only:11/26/2022 06:49:31],[CN=Azure_IoT_Hub_CA_Cert_Test_Only:11/26/2022 06:49:30],[CN=Azure_IoT_Hub_CA_Cert_Test_Only:11/26/2022 06:49:30] to Root
<6> 2022-10-31 05:41:52.042 +00:00 [INF] - Starting metrics listener on Host: *, Port: 9600, Suffix: metrics
<6> 2022-10-31 05:41:52.051 +00:00 [INF] - Updating performance metrics every 05m:00s
<6> 2022-10-31 05:41:52.054 +00:00 [INF] - Started operation Get system resources





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


