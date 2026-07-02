param([int]$Port = 5000)

$Root = (Get-Location).ProviderPath
$Listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse("127.0.0.1"), $Port)
$Listener.Start()

Write-Host "Serving $Root"
Write-Host "Open http://localhost:$Port/index.html"
Write-Host "Press Ctrl+C to stop."

function Send-Response($Stream, [int]$Status, [string]$StatusText, [byte[]]$Body, [string]$ContentType) {
    $Header = "HTTP/1.1 $Status $StatusText`r`nContent-Type: $ContentType`r`nContent-Length: $($Body.Length)`r`nConnection: close`r`n`r`n"
    $HeaderBytes = [System.Text.Encoding]::ASCII.GetBytes($Header)
    $Stream.Write($HeaderBytes, 0, $HeaderBytes.Length)
    $Stream.Write($Body, 0, $Body.Length)
}

while ($true) {
    $Client = $Listener.AcceptTcpClient()
    try {
        $Stream = $Client.GetStream()
        $Reader = [System.IO.StreamReader]::new($Stream)
        $RequestLine = $Reader.ReadLine()

        while (($Line = $Reader.ReadLine()) -ne "") {}

        if (-not $RequestLine) { continue }

        $UrlPath = $RequestLine.Split(" ")[1].Split("?")[0]
        $UrlPath = [System.Uri]::UnescapeDataString($UrlPath)

        if ($UrlPath -eq "/") { $UrlPath = "/index.html" }

        $RelativePath = $UrlPath.TrimStart("/").Replace("/", "\")
        $FullPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($Root, $RelativePath))

        if (-not $FullPath.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
            $Body = [System.Text.Encoding]::UTF8.GetBytes("403 Forbidden")
            Send-Response $Stream 403 "Forbidden" $Body "text/plain; charset=utf-8"
            continue
        }

        if (-not (Test-Path $FullPath -PathType Leaf)) {
            $Body = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $UrlPath")
            Send-Response $Stream 404 "Not Found" $Body "text/plain; charset=utf-8"
            continue
        }

        $Ext = [System.IO.Path]::GetExtension($FullPath).ToLowerInvariant()
        $ContentType = switch ($Ext) {
            ".html" { "text/html; charset=utf-8" }
            ".css"  { "text/css; charset=utf-8" }
            ".js"   { "application/javascript; charset=utf-8" }
            ".json" { "application/json; charset=utf-8" }
            ".png"  { "image/png" }
            ".jpg"  { "image/jpeg" }
            ".jpeg" { "image/jpeg" }
            ".svg"  { "image/svg+xml" }
            ".mp4"  { "video/mp4" }
            default { "application/octet-stream" }
        }

        $Body = [System.IO.File]::ReadAllBytes($FullPath)
        Send-Response $Stream 200 "OK" $Body $ContentType
    }
    finally {
        $Client.Close()
    }
}
