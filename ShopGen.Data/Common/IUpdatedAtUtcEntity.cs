namespace ShopGen.Data.Common;

/// <summary>
/// An interface for objects which have an updated at field
/// </summary>
public interface IUpdatedAtUtcEntity
{
    DateTime UpdatedAtUtc { get; set; }
}