namespace ShopGen.Data.Common;

/// <summary>
/// An interface for objects with a Guid ID field
/// </summary>
public interface IIdEntity
{
    Guid Id { get; set; }
}