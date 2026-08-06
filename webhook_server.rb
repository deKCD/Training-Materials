require 'sinatra'
require 'json'
require 'openssl'
require 'net/http'
require 'uri'

set :bind, '0.0.0.0'
set :port, 5000

# Use ENV or hardcoded for your secret and for target branch
WEBHOOK_SECRET = ENV['TRAINING_MATERIAL_WEBHOOK_SECRET']
TARGET_BRANCH = ENV['TARGET_BRANCH'] || 'main'
KUMA_PUSH_URL = ENV['KUMA_PUSH_URL']


helpers do
  def verify_signature(payload_body, signature)
    expected_signature = 'sha256=' + OpenSSL::HMAC.hexdigest(OpenSSL::Digest.new('sha256'), WEBHOOK_SECRET, payload_body)
    compare_result = Rack::Utils.secure_compare(expected_signature, signature.to_s)

    compare_result
  end

  def notify_kuma(status:, msg:, ping: nil)
    return if KUMA_PUSH_URL.nil? || KUMA_PUSH_URL.empty?
    uri = URI(KUMA_PUSH_URL)
    params = { status: status, msg: msg }
    params[:ping] = ping if ping
    # Preserve any query params already on the push URL, but drop the ones we're setting
    # so pasting Kuma's full example URL (which includes status=up&msg=OK&ping=) still works.
    existing = URI.decode_www_form(uri.query || '').reject { |k, _| %w[status msg ping].include?(k) }
    uri.query = URI.encode_www_form(existing + params.to_a)
    Net::HTTP.get_response(uri)
  rescue => e
    warn "Kuma notify failed: #{e.class}: #{e.message}"
  end
end

post '/webhook' do
  request.body.rewind
  payload_body = request.body.read
  signature = request.env['HTTP_X_HUB_SIGNATURE_256']
  event     = request.env['HTTP_X_GITHUB_EVENT']

  halt 401, "Signatures didn't match!" unless verify_signature(payload_body, signature)

  payload = JSON.parse(payload_body)
  case event
  when "push"
    branch_ref = payload['ref']
    halt 400, "Not the #{TARGET_BRANCH} branch" unless branch_ref == "refs/heads/#{TARGET_BRANCH}"
  when "pull_request"
    action = payload['action']
    merged = payload['pull_request'] && payload['pull_request']['merged']
    base_branch = payload['pull_request'] && payload['pull_request']['base']['ref']
    unless action == "closed" && merged && base_branch == TARGET_BRANCH
      halt 400, "Not a merged PR to #{TARGET_BRANCH}"
    end
  else
    halt 400, "Unsupported event"
  end

  # Pull latest and rebuild the static site so Rack serves fresh content.
  started = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  output = `cd /srv/jekyll && git checkout #{TARGET_BRANCH} && git pull && JEKYLL_ENV=production bundle exec jekyll build 2>&1`
  status_code = $?.exitstatus
  elapsed_ms = ((Process.clock_gettime(Process::CLOCK_MONOTONIC) - started) * 1000).round

  if status_code == 0
    notify_kuma(status: 'up', msg: 'OK', ping: elapsed_ms)
    content_type :json
    { result: "Success!", output: output }.to_json
  else
    tail = output.to_s.lines.last(5).join.strip
    notify_kuma(status: 'down', msg: "build failed: #{tail[0, 200]}")
    halt 500, { result: "Failure!", output: output }.to_json
  end
end
