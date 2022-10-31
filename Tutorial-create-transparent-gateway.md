
### Prepare input parameters for appConfig.xml 

1. Update each parameters in XML

2. List of parameters:


### Variables for appConfig.xml

| XML variable name  | Status                     | Description                                                                                                                                                                                                          |
|------------------------------------------------------------------------------------------------------------------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| server1                     | :heavy_check_mark:         | XML group of variables for 1st node of host                                     |
.....


```hcl

```



### Script: [main1.ps1](https://github.com/philipcaffeine/stackhciauto/blob/main/deployment/_main1.ps1)

- script: main1.ps1
- purpose: 

```hcl
    prepare each server before cluster creation 
    Step 1:load parameters from appConfig.xml

    For server 1:
    Step 1.2: Join the domain and add domain accounts
    Step 1.3: Install roles and features

    For server 2:
    Step 1.2: Join the domain and add domain accounts
    Step 1.3: Install roles and features
```
