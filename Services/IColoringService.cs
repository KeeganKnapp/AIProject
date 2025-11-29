

using System.Net.Http.Json;

namespace MapColoringApp.Services
{
    public interface IColoringService
    {
        Task StartAsync(ColoringRequest req, CancellationToken ct = default);

	Task<ColoringResponse> RunOnceAsync(CancellationToken ct = default);
    }

    public record ColoringRequest(
        string StateId,
        int colorIndex,
        List<string> AvailableColors
    );

    public record ColoringResponse(
	string StateId,
	string Color
    );

    public class HttpColoringService(HttpClient http) : IColoringService
    {
        public async Task StartAsync(ColoringRequest req, CancellationToken ct = default)
        {
            var res = await http.PostAsJsonAsync("http://localhost:5000/api/start", req, ct);
            res.EnsureSuccessStatusCode();
            return;
        }

	public async Task<ColoringResponse> RunOnceAsync(CancellationToken ct = default)
	{
	    var res = await http.GetAsync("http://localhost:5000/api/runonce", ct);
	    res.EnsureSuccessStatusCode();
	    return await res.Content.ReadFromJsonAsync<ColoringResponse>(cancellationToken: ct);
	}
    }
}
