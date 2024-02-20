using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using ShopGen.Data.Common;

namespace ShopGen.Data.Games;

public class SourcebookEntity : IIdEntity, ICreatedAtUtcEntity, IUpdatedAtUtcEntity
{
    public Guid Id { get; set; }
    public DateTime CreatedAtUtc { get; set; }
    public DateTime UpdatedAtUtc { get; set; }
    public string FullName { get; set; }
    public string Abbreviation { get; set; }
    public Guid SystemId { get; set; }
    public SystemEntity System { get; set; }

    internal sealed class SourcebookEntityConfiguration : IEntityTypeConfiguration<SourcebookEntity>
    {
        public void Configure(EntityTypeBuilder<SourcebookEntity> builder)
        {
            builder.ToTable("Sourcebooks");
            builder.HasKey(x => x.Id);
            builder.Property(x => x.CreatedAtUtc).IsRequired();
            builder.Property(x => x.UpdatedAtUtc).IsRequired();
            builder.Property(x => x.FullName).HasMaxLength(128).IsRequired();
            builder.Property(x => x.Abbreviation).HasMaxLength(8).IsRequired();
            builder.Property(x => x.SystemId).IsRequired();
        }
    }
}