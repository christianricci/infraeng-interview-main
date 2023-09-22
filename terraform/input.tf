variable "project_id" {
    type = string
}

variable "instances" {
  type = map(object({
    machine_type = string
	zone  = string
	description = string
   }))
}

variable "service_account" {
    type = string
    default = ""
}

variable "scopes" {
    type = list(string)
    default = []
}
