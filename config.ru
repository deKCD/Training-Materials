require "rack/static"

static = Rack::Builder.new do
  use Rack::Static,
    urls: [""],
    root: "_site",
    index: "index.html",
    header_rules: [
      [:all, { "cache-control" => "public, max-age=300" }]
    ]

  run ->(env) {
    not_found = File.join("_site", "404.html")
    if File.exist?(not_found)
      [404, { "content-type" => "text/html" }, [File.read(not_found)]]
    else
      [404, { "content-type" => "text/plain" }, ["Not found"]]
    end
  }
end

map "/training" do
  run static
end
