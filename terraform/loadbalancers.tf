# Shop gen lets encrypt certificate
resource "digitalocean_certificate" "shopgen-cert" {
    name = "shopgen-certificate"
    type = "lets_encrypt"
    domains = ["nicklesshopgen.com"]
}

resource "digitalocean_loadbalancer" "shopgen" {
    name = "shopgen-balancer-1"
    region = "nyc3"
    redirect_http_to_https = true

    vpc_uuid = digitalocean_vpc.shopgen.id

    forwarding_rule {
      entry_port = 443
      entry_protocol = "https"

      target_port = 443
      target_protocol = "https"

      certificate_name = digitalocean_certificate.shopgen-cert.name
    }

    droplet_tag = "k8s:worker"
}