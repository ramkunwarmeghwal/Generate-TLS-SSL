from flask import Flask, request, render_template
import subprocess
import os
#import time

app = Flask(__name__)

# Function to create NGINX configuration file
def create_nginx_config(subdomain):
    nginx_config = f"""
    server {{
       server_name {subdomain};
       error_log /var/log/nginx/{subdomain}.log error;
       listen 443 ssl; # managed by Certbot
       ssl_certificate /etc/letsencrypt/live/{subdomain}/fullchain.pem; # managed by Certbot
       ssl_certificate_key /etc/letsencrypt/live/{subdomain}/privkey.pem; # managed by Certbot
       location / {{
        # Return a simple HTML message with the correct Content-Type
        add_header Content-Type text/html;
        return 200 '<html><body><h1>SSL Certificate Successfully Generated</h1></body></html>';
       }}
    }}
    """

    # Path to save the file
    file_path = f"/etc/nginx/sites-enabled/{subdomain}"

    try:
        # Create and write to the file
        with open(file_path, "w") as file:
            file.write(nginx_config)
        print(f"NGINX config created at: {file_path}")
        return True
    except Exception as e:
        print(f"Error creating NGINX config: {e}")
        return False

# Read contents of a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Generate SSL using Certbot with user-provided domain and email
def generate_ssl(domain, email):
    try:
        # Run the certbot command to generate the certificate for the input domain and email
        subprocess.run([
            "sudo", "certbot", "certonly", "--nginx", "-d", domain,
            "--non-interactive", "--agree-tos", "--email", email
        ], check=True)

        # After generating SSL, create the NGINX config
        success = create_nginx_config(domain)

        # Read certificate and private key files
        cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
        key_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"
        cert_content = read_file(cert_path)
        key_content = read_file(key_path)

        # Restart Nginx after the certificate is successfully generated
#        restart_nginx()

        return success, cert_content, key_content

    except subprocess.CalledProcessError as e:
        print(f"Error generating SSL certificate: {e}")
        return False, None, None

# Function to restart Nginx service
def restart_nginx():
    try:
        time.sleep(10)
        subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)
        print("Nginx restarted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Nginx: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain')
        email = request.form.get('email')
        if domain and email:
            success, cert_content, key_content = generate_ssl(domain, email)
            if success:
                return render_template('index.html', cert_content=cert_content, key_content=key_content)
            else:
                return "Failed to generate SSL certificate or NGINX config."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
