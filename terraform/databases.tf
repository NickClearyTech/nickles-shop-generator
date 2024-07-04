# Project database cluster

resource "digitalocean_database_cluster" "production-postgres" {
    name = "production-postgres"
    engine = "pg"
    version = "15"
    size = "db-s-1vcpu-1gb"
    region = "nyc3"
    node_count = 1
    private_network_uuid = digitalocean_vpc.shopgen.id
}

# Allow access to the database cluster

resource "digitalocean_database_firewall" "shopgen_database_access" {
    cluster_id = digitalocean_database_cluster.production-postgres.id

    rule {
        type = "k8s"
        value = digitalocean_kubernetes_cluster.shopgen-cluster.id
    }

    # rule {
    #     type = "droplet"
    #     value = digitalocean_droplet.bastion.id
    # }
}       

# Create shopgen production database
resource "digitalocean_database_db" "shopgen-production" {
    cluster_id = digitalocean_database_cluster.production-postgres.id
    name = "shopgen"
}