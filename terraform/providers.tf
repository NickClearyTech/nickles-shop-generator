terraform {
    cloud {
        organization = "NickClearyTech"
        workspaces {
            name = "NicklesShopGen"
        }
    }
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}