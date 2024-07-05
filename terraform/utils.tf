# Retrieves the IP address of the executor
data "http" "myip" {
  url = "https://ipv4.icanhazip.com"
}