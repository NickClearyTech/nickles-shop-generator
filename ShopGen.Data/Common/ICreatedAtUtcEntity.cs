namespace ShopGen.Data.Common;

/// <summary>
/// An interface for objects that put in the Datetime in UTC as an object is created
/// </summary>
internal interface ICreatedAtUtcEntity
{
    DateTime CreatedAtUtc { get; set; }
}