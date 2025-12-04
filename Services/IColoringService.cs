

using System.Net.Http.Json;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace MapColoringApp.Services
{
    public interface IColoringService
    {
        Task StartAsync(ColoringRequest req, CancellationToken ct = default);

	Task<ColoringResponse> RunOnceAsync(CancellationToken ct = default);
    }

    public record ColoringRequest {
        public List<string> StateIds { get; init; }
        public List<int> SelectedColors { get; init; }
        public List<string> Colors  { get; init; }
	public string Map { get; init; }
    }

    public record ColoringResponse {
	public string StateId { get; init; }
	public string Color { get; init; }
	public Dictionary<string, List<string>> Domains { get; init; }
	public Dictionary<string, string> ColoredStates { get; init; }
	public Dictionary<string, List<string>> UsedColors { get; init; }
    };

    public class HttpColoringService(HttpClient http) : IColoringService
    {
        public async Task StartAsync(ColoringRequest req, CancellationToken ct = default)
        {
		var json = JsonSerializer.Serialize(req);
		var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
		var res = await http.PostAsync("http://localhost:5000/api/start", content, ct);
		res.EnsureSuccessStatusCode();
        }

	public async Task<ColoringResponse> RunOnceAsync(CancellationToken ct = default)
	{
		var res =  await http.GetFromJsonAsync<ColoringResponse>("http://localhost:5000/api/runonce", ct);
		Console.WriteLine($"Received response: {JsonSerializer.Serialize(res)}");
		return res!;
	}
    }
}
