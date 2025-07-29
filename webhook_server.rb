require 'sinatra'
require 'json'
require 'openssl'

set :bind, '0.0.0.0'
set :port, 5000

# Use ENV or hardcoded for your secret
WEBHOOK_SECRET = ENV['WEBHOOK_SECRET'] || 'your_github_webhook_secret'

helpers do
  def verify_signature(payload_body, signature)
    return false unless signature
    signature = signature.gsub('sha256=', '')
    digest    = OpenSSL::HMAC.hexdigest(OpenSSL::Digest.new('sha256'), WEBHOOK_SECRET, payload_body)
    Rack::Utils.secure_compare(digest, signature)
  end
end

post '/webhook' do
  request.body.rewind
  payload_body = request.body.read
  signature = request.env['HTTP_X_HUB_SIGNATURE_256']
  event     = request.env['HTTP_X_GITHUB_EVENT']

  halt 401, "Signatures didn't match!" unless verify_signature(payload_body, signature)
  halt 400, "Unsupported event" unless event == "push"

  # Trigger your desired script or command here -- e.g. git pull
  output = `cd /srv/jekyll && git pull 2>&1`
  status_code = $?.exitstatus

  if status_code == 0
    content_type :json
    {result: "Success!", output: output}.to_json
  else
    halt 500, {result: "Failure!", output: output}.to_json
  end
end

get '/' do
  "Webhook endpoint is running!"
end


# need to adjust this webhook endpoint, so it should work fine actually