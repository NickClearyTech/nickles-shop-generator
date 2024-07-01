# Project VPC

resource "digitalocean_vpc" "shopgen" {
    name = "shopgen-network"
    region = "nyc3"
    ip_range = "10.10.10.0/24"
    
}

# Project kubernetes cluster

resource "digitalocean_kubernetes_cluster" "shopgen-cluster" {
  name = "shopgen-cluster"
  region = "nyc3"

  version = "1.30.1-do.0"
  vpc_uuid = digitalocean_vpc.shopgen.id

  node_pool {
    name = "default-nodepool"
    node_count = 2
    size = "s-1vcpu-2gb"
  }
}

# VPC Bastion Droplet
resource "digitalocean_droplet" "bastion" {
    image = "ubuntu-24-04-x64"
    name = "shopgen-bastion"
    region = "nyc3"
    size = "s-1vcpu-1gb"
    monitoring = true
    ssh_keys = [data.digitalocean_ssh_key.primary-key.id]
}