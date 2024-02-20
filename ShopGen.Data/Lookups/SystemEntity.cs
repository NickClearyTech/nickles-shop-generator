using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using ShopGen.Data.Common;

namespace ShopGen.Data.Games;

public sealed class SystemEntity : IIdEntity, ICreatedAtUtcEntity, IUpdatedAtUtcEntity
{
    public Guid Id { get; set; }
    public DateTime CreatedAtUtc { get; set; }
    public DateTime UpdatedAtUtc { get; set; }
    public string FullName { get; set; }
    public string AbbreviatedName { get; set; }
    public ICollection<SourcebookEntity> Books = new List<SourcebookEntity>();
    
    internal sealed class SystemEntityConfiguration : IEntityTypeConfiguration<SystemEntity>
    {
        public void Configure(EntityTypeBuilder<SystemEntity> builder)
        {
            builder.ToTable("Systems");
            builder.HasKey(x => x.Id);
            builder.Property(x => x.CreatedAtUtc).IsRequired();
            builder.Property(x => x.UpdatedAtUtc).IsRequired();
            builder.Property(x => x.FullName).HasMaxLength(64).IsRequired();
            builder.Property(x => x.AbbreviatedName).HasMaxLength(8).IsRequired();
        }
    }
}