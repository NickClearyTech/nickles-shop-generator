namespace ShopGen.Utils;

public static class GetConnectionString
{
    public static string GetPostgresConnectionString()
    {
        return
            $"Host={Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "postgres"};Database={Environment.GetEnvironmentVariable("POSTGRES_DATABASE") ?? "postgres"};Username={Environment.GetEnvironmentVariable("POSTGRES_USERNAME") ?? "postgres"};Password={Environment.GetEnvironmentVariable("POSTGRES_PASSWORD")}";
    }

    public static string GetRedisConnectionString()
    {
        return
            $"{Environment.GetEnvironmentVariable("REDIS_HOST") ?? "redis"}:{Environment.GetEnvironmentVariable("REDIS_PORT") ?? "6379"},password={Environment.GetEnvironmentVariable("REDIS_PASSWORD") ?? "redis"}";
    }
}