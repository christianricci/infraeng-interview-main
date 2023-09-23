# Christian Ricci - 22/Sep/2023
# Google compute terraform doc - https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance

resource "google_compute_instance" "vm" {
    for_each = var.instances
    project = var.project_id
    name = var.instances[each.key].instance_name
    description = var.instances[each.key].description
    machine_type = var.instances[each.key].machine_type
    zone = var.instances[each.key].zone
    hostname = "${var.instances[each.key].instance_name}-${var.instances[each.key].zone}.asx.com.au"

    /* Christian Ricci - 22/Sep/2023
       Description: This code will act as a for loop and allow terraform to create as many service_account blocks 
       as specified by the inputs.tf variable in this case var.service_account. 

       According to the GCP api https://cloud.google.com/compute/docs/reference/rest/v1/instances service_account is a list 
       of map(email, scopes). The input variable is a string not a list of maps or a single map.

       I believe the intention here is to either define a single service account or nothing. This is done by using the inline
       condition where on true an array with content int=1 is defined, on false an empty array is defined. The array content
       is not referenced, but instead is used to permit the service_account block to be created or not.
    */
    dynamic service_account {
        for_each = var.service_account != "" ? [1] : []
        content {
            email = var.service_account
            scopes = var.scopes
        }
    }
}
