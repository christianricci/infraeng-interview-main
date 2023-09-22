resource "google_compute_instance" "vm" {
    project = var.project_id
    name = var.instance_name
    description = var.description
    machine_type = var.machine_type
    zone = var.zone
    hostname = var.hostname
	
    dynamic service_account {
        for_each = var.service_account != "" ? [1] : []
        content {
            email = var.service_account
            scopes = var.scopes
        }
    }
}
