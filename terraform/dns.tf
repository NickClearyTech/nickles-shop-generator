resource "digitalocean_domain" "nicklesshopgen"{
    name = "nicklesshopgen.com"
}

resource "digitalocean_record" "shopgen" {
  domain = digitalocean_domain.nicklesshopgen.id
  type   = "A"
  name   = "@"
  value  = data.digitalocean_loadbalancer.shopgen-production.ip
  ttl = 1800
}