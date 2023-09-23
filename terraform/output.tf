# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance
output "vm_hostnames" {
    description = "list of VM hostnames as a map"
    value = {
        for vm in google_compute_instance.vm :
        vm.name => vm.hostname
    }
}

output "vm_ip_addresses" {
    description = "list of VM IP addresses"
    value = {
        for vm in google_compute_instance.vm :
            vm.hostname => {
                ip_addresses = [
                for item in vm.network_interface :
                {
                    name = item.name
                    ip_address = item.network_ip
                }
            ]
        }
    }
}
