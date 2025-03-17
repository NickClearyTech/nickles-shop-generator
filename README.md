# Nickle's Shop Generator

A simple, WIP shop generator application written in Django with DRF to allow automatically creating magic item and equipment shops to stop your players from asking "Is X in the shop" every session.

## Development - Getting Started

### Development Applications
Everything in this application is intended to run in docker, before you begin, you must install Docker, and ensure that the `docker compose` command is available.

Additionally, this application is developed to be API first, so having an API client such as Postman installed is also helpful.

### Running for the first time
Copy the existing `example.env` to `.env`, and replace the `<DJANGOSECRETKEY>` with a random string to serve as the Django secret key

Next, run `docker compose up --build`, to both build and run the application in one command.

When the `initializer` container completes, it will print a line with an admin token similar to `Token 31a7b4a12d78e128f9fde0d5e2d2f921ea95ac9b` before exiting. Save this value.

Once the initializer exits, the application is ready to run.

### Generating your first shop

#### Using Postman
In postman, import both the collection and environment located in the `postman/` directory. 

Edit the imported environment to insert your generated token (note, only the random string part is needed, the `Token` can be omitted).

Next, simply run the request under Shops > Generate Shop. This will respond with an ID of your newly generated shop:

```json
{
  "id": 1,
  "owner": null
}
```

#### Accessing the shop
In the browser, browse to `http://localhost:8000/shop/<SHOP ID>`