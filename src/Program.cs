using Dapper;
using HtmlAgilityPack;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SQLite;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace RegionCodeSpider
{
    class Program
    {
        static IHttpClientFactory _httpClientFactory;
        static ILogger _logger;
        static IDbConnection _dbConnection;

        static async Task Main(string[] args)
        {
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

            var sereviceProvider = new ServiceCollection()
                .AddHttpClient()
                .BuildServiceProvider();
            _httpClientFactory = sereviceProvider.GetRequiredService<IHttpClientFactory>();
            _dbConnection = new SQLiteConnection("Data Source=database.db");

            if (!File.Exists("database.db"))
            {
                SQLiteConnection.CreateFile("database.db");
                await _dbConnection.ExecuteAsync("create table region(code text, name text,url text, type text)");
            }

            _logger = new LoggerConfiguration()
                .WriteTo.RollingFile("logs/{Date}.log")
                .CreateLogger();

            var indexUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html";
            var provinces = await GetProvincesAsync(indexUrl);
            foreach (var province in provinces)
            {
                //if (string.Compare(province.Code, "51") < 0)
                //{
                //    Console.WriteLine($"{province.Code}【{province.Name}】跳过");
                //    continue;
                //}
                Console.WriteLine($"[{DateTime.Now.ToString("HH:mm:ss")}]【省】{province.Code} {province.Name} {province.Type} {province.Url}");
                await SaveRegionAsync(province);
                var cities = await GetCitiesAsync(province.Url);
                foreach (var city in cities)
                {
                    Console.WriteLine($"[{DateTime.Now.ToString("HH:mm:ss")}]【市】{city.Code} {city.Name} {city.Type} {city.Url}");
                    await SaveRegionAsync(city);
                    var counties = await GetCountiesAsync(city.Url);
                    foreach (var county in counties)
                    {
                        Console.WriteLine($"[{DateTime.Now.ToString("HH:mm:ss")}]【县】{county.Code} {county.Name} {county.Type} {county.Url}");
                        await SaveRegionAsync(county);
                        var towns = await GetTownsAsync(county.Url);
                        foreach (var town in towns)
                        {
                            Console.WriteLine($"[{DateTime.Now.ToString("HH:mm:ss")}]【乡】{town.Code} {town.Name} {town.Type} {town.Url}");
                            await SaveRegionAsync(town);
                            var villages = await GetVillagesAsync(town.Url);
                            foreach (var village in villages)
                            {
                                Console.WriteLine($"[{DateTime.Now.ToString("HH:mm:ss")}]【村】{village.Code} {village.Name} {village.Type} {village.Url}");
                                await SaveRegionAsync(village);
                            }
                        }
                    }
                }
            }

            Console.WriteLine("获取完成");
            Console.ReadLine();
        }

        /// <summary>
        /// 取得省数据
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        static async Task<IEnumerable<Region>> GetProvincesAsync(string url)
        {
            using var httpClient = _httpClientFactory.CreateClient();
            var stream = await httpClient.GetStreamAsync(url);

            var doc = new HtmlDocument();
            doc.Load(stream, Encoding.GetEncoding("GB2312"));

            var trs = doc.DocumentNode.SelectNodes("//tr").Where(d => d.HasClass("provincetr"));

            var list = new List<Region>();

            var baseUrl = url.Substring(0, url.LastIndexOf("/"));
            foreach (var tr in trs)
            {
                var provinces = tr.SelectNodes("td/a");
                foreach (var province in provinces)
                {
                    var href = province.GetAttributeValue("href", "");
                    list.Add(new Region()
                    {
                        Code = href.Replace(".html", ""),
                        Name = province.InnerText,
                        Url = $"{baseUrl}/{href}"
                    });
                }
            }
            return list;
        }

        /// <summary>
        /// 取得市数据
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        static async Task<IEnumerable<Region>> GetCitiesAsync(string url)
        {
            return await GetRegionsAsync(url, "citytr");
        }

        /// <summary>
        /// 获取县数据
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        static async Task<IEnumerable<Region>> GetCountiesAsync(string url)
        {
            return await GetRegionsAsync(url, "countytr");
        }

        /// <summary>
        /// 获得镇数据
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        static async Task<IEnumerable<Region>> GetTownsAsync(string url)
        {
            return await GetRegionsAsync(url, "towntr");
        }

        /// <summary>
        /// 取得村数据
        /// </summary>
        /// <param name="url"></param>
        /// <returns></returns>
        static async Task<IEnumerable<Region>> GetVillagesAsync(string url)
        {
            return await GetRegionsAsync(url, "villagetr");
        }

        /// <summary>
        /// 取得市、县、乡、村数据
        /// </summary>
        /// <param name="url"></param>
        /// <param name="className"></param>
        /// <returns></returns>
        private static async Task<IEnumerable<Region>> GetRegionsAsync(string url, string className)
        {
            if (string.IsNullOrWhiteSpace(url))
            {
                return Array.Empty<Region>();
            }

            var error = 0;

            while (error < 5)
            {
                try
                {
                    using var httpClient = _httpClientFactory.CreateClient();
                    var stream = await httpClient.GetStreamAsync(url);
                    var doc = new HtmlDocument();
                    doc.Load(stream, Encoding.GetEncoding("GB2312"));
                    var trs = doc.DocumentNode.SelectNodes("//tr").Where(d => d.HasClass(className)).ToArray();
                    var list = new List<Region>();
                    var baseUrl = url.Substring(0, url.LastIndexOf("/"));
                    foreach (var tr in trs)
                    {
                        var tds = tr.SelectNodes("td");
                        var href = tds[0].SelectSingleNode("a")?.GetAttributeValue("href", "");
                        var region = new Region();
                        region.Code = tds[0].InnerText;
                        if (className == "villagetr")
                        {
                            region.Type = tds[1].InnerText;
                            region.Name = tds[2].InnerText;
                        }
                        else
                        {
                            region.Name = tds[1].InnerText;
                            region.Url = string.IsNullOrEmpty(href) ? "" : $"{baseUrl}/{href}";
                        }
                        list.Add(region);
                    }
                    return list;
                }
                catch (Exception ex)
                {
                    error++;
                    _logger.Error(ex, "抓取错误");
                }
            }
            return Array.Empty<Region>();
        }

        private static async Task<int> SaveRegionAsync(Region region)
        {
            return await _dbConnection.ExecuteAsync("insert into region(code, name, url, type) values(@code, @name, @url, @type)", region);
        }
    }


    public class Region
    {
        public string Code { get; set; }
        public string Name { get; set; }
        public string Url { get; set; }
        public string Type { get; set; }
    }
}
