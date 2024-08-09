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
    node_count = 1
    size = "s-2vcpu-4gb"
  }
}

resource "digitalocean_kubernetes_node_pool" "extra-node" {
  cluster_id = digitalocean_kubernetes_cluster.shopgen-cluster.id

  name       = "extra-node"
  size       = "s-1vcpu-2gb"
  node_count = 1
}