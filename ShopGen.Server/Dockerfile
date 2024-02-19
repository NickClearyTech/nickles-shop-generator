FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ShopGen.Data ShopGen.Data
COPY ShopGen.Server ShopGen.Server

RUN dotnet publish "ShopGen.Server/ShopGen.Server.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
# Copy files from previous stage
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "ShopGen.Server.dll"]