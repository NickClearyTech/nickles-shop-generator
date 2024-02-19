using Microsoft.EntityFrameworkCore;
namespace ShopGen.Data;

public sealed class ShopGenContext : DbContext
{
    public ShopGenContext(DbContextOptions<ShopGenContext> options) : base(options)
    {
        
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ShopGenContext).Assembly);
    }
}