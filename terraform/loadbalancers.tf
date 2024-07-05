# Shop gen lets encrypt certificate
resource "digitalocean_certificate" "shopgen-cert" {
    name = "shopgen-certificate"
    type = "lets_encrypt"
    domains = ["nicklesshopgen.com"]
}

data "digitalocean_loadbalancer" "shopgen-production" {
  name = "ab2ea106b39024a8fb3bbd8178754d66"
}
