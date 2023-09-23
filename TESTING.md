# Testing

I'm trying to validate the `output.tf`, to do this I simulated it by adding a temporary variable in `input.tf` as follows:

```
variable "console_test" {
    type = map(object({
        name = string
        hostname = string
        network_interface = list(object({
            network_ip = string
            name = string
        }))
    }))
    default = {
        vm1 = {
            "name" = "myhost-1",
            "hostname" = "myhost-1.asx.com.au",
            "network_interface" = [
                {
                    "network_ip" = "10.0.0.1",
                    "name" = "eth0"
                },
                {
                    "network_ip" = "192.168.1.1",
                    "name" = "eth1"
                }            
            ]        
        },
        vm2 = {
            "name" = "myhost-2",
            "hostname" = "myhost-2.asx.com.au",
            "network_interface" = [
                {
                    "network_ip" = "10.0.0.1",
                    "name" = "eth0"
                },
                {
                    "network_ip" = "192.168.1.1",
                    "name" = "eth1"
                }            
            ]        
        }
    }
}
```

Then, I used `"terraform console"` and tried to generate the output as per below:

Host list Output:
```
> { for key in var.console_test : key.name => key.hostname }
{
  "myhost-1" = "myhost-1.asx.com.au"
  "myhost-2" = "myhost-2.asx.com.au"
}
```
IP addresses list output:
```
> { for key in var.console_test : key.hostname => [ for item in key.network_interface : { (item.name) = item.network_ip } ] }
{
  "myhost-1.asx.com.au" = [
    {
      "eth0" = "10.0.0.1"
    },
    {
      "eth1" = "192.168.1.1"
    },
  ]
  "myhost-2.asx.com.au" = [
    {
      "eth0" = "10.0.0.1"
    },
    {
      "eth1" = "192.168.1.1"
    },
  ]
}
```