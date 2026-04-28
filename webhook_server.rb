require 'sinatra'
require 'json'
require 'openssl'

set :bind, '0.0.0.0'
set :port, 5000

# Use ENV or hardcoded for your secret and for target branch
WEBHOOK_SECRET = ENV['TRAINING_MATERIAL_WEBHOOK_SECRET']
TARGET_BRANCH = ENV['TARGET_BRANCH'] || 'main'


helpers do
  def verify_signature(payload_body, signature)
    expected_signature = 'sha256=' + OpenSSL::HMAC.hexdigest(OpenSSL::Digest.new('sha256'), WEBHOOK_SECRET, payload_body)
    compare_result = Rack::Utils.secure_compare(expected_signature, signature.to_s)

    compare_result
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

  # Do your git pull, etc.
  output = `cd /srv/jekyll && git checkout #{TARGET_BRANCH} && git pull 2>&1`
  status_code = $?.exitstatus

  if status_code == 0
    content_type :json
    { result: "Success!", output: output }.to_json
  else
    halt 500, { result: "Failure!", output: output }.to_json
  end
end