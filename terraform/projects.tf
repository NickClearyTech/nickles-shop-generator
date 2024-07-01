resource "digitalocean_project" "shop-gen-production" {
  name        = "shop-gen-production"
  description = "Contains production shop gen resources"
  purpose     = "Web Application"
  environment = "Production"
}

resource "digitalocean_project_resources" "shopgen-production-resources" {
    project = digitalocean_project.shop-gen-production.id
    resources = [
        digitalocean_database_cluster.production-postgres.urn,
        digitalocean_kubernetes_cluster.shopgen-cluster.urn,
        digitalocean_droplet.bastion.urn,
        digitalocean_loadbalancer.shopgen.urn
    ]
  
}