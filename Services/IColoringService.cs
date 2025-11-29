

using System.Net.Http.Json;

namespace MapColoringApp.Services
{
    public interface IColoringService
    {
        Task StartAsync(ColoringRequest req, CancellationToken ct = default);
    }

    public record ColoringRequest(
        string StateId,
        int colorIndex,
        List<string> AvailableColors
    );

    public class HttpColoringService(HttpClient http) : IColoringService
    {
        public async Task StartAsync(ColoringRequest req, CancellationToken ct = default)
        {
            var res = await http.PostAsJsonAsync("http://localhost:5000/api/start", req, ct);
            res.EnsureSuccessStatusCode();
            return;
        }
    }
}
