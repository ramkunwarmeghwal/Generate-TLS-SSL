# Generate TLS/SSL Certifiate for subdomain Using UI

<b>Prerequisites: </b>
- Install Nginx
- Map your system's public IP to a DNS record (such as Route 53, GoDaddy, Cloudflare, etc.) with subdomain.

<b> Running the Application</b>
python3 application.py

Alternatively, to run the application in the background, use the following command:
nohup python3 application.py &

<b>Now Open your application in browser</b>
http://<IP-ADDRESS>:5000/
![Image](https://github.com/user-attachments/assets/76a6aa58-cb7d-4ebb-acb9-66ea159d2a98)

Now, you can generate a TLS/SSL certificate for your subdomain (e.g., rk.read-me.link).
- Ensure that the subdomain is correctly mapped to our system's public IP
- we will need to provide details such as the subdomain and your email address during the certificate generation process.
![Image](https://github.com/user-attachments/assets/3013fb0f-45c1-4634-ba06-026aacf08650)

![Image](https://github.com/user-attachments/assets/dea37923-4ac4-4cde-800e-f5b9f5cf6603)
Once you've generated your SSL certificate, we can use the fullchain and privkey files to secure your subdomain application
![Image](https://github.com/user-attachments/assets/46a9466b-d70c-48b0-a989-4bd958a6035f)




