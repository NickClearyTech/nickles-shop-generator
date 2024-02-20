using Microsoft.EntityFrameworkCore;
using ShopGen.Data;
using ShopGen.Utils;
using MudBlazor.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
string connectionString = GetConnectionString.GetPostgresConnectionString();
builder.Services.AddDbContext<ShopGenContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddHealthChecks();

// Confnigure redis backplane for signalR
builder.Services.AddSignalR().AddStackExchangeRedis(GetConnectionString.GetRedisConnectionString());

builder.Services.AddDatabaseDeveloperPageExceptionFilter();
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

// Register mudblazor
builder.Services.AddMudServices();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseMigrationsEndPoint();
}
else
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();