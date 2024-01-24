# AI Rules

**DTY 2023 - Amadeus**

AI Rules is a chatbot which helps the travel agents in their daily task of answering to customers. Its main purposes are to reduce the time to retrieve an important information, but also standardizing and aggregating data. The project is divided in two parts: the server repository (in Python), whose goals are to retrieve data, and create answers, and the client repository (in next.js), displaying the user interface (UI) and enhancing the user experience (UX), where the user can interact with the chatbot.

Here is the readme to deploy the project on your VM to access it online. There are two other readmes, one in `final_version/server` and the other in `final_version/client`.

## Installation

First, you need to have a Virtual Machine (VM) with a domain name on it (our was *f23-p2-airules.paris-digital-lab.fr* and we used a Ubuntu 23.04 with 2Go of RAM). We will call this domain name `your-domain-name` for the rest of the installation tutorial. Once you have it, add the public ssh key of the gitlab repository in your VM. You can create a pair of private and public key without any password just for your gitlab repository (this step is important) and add them to the environment variables of the project. We can now start the installation process. 

### 1. Install Docker on your VM

Once you are in the terminal of your VM you can run the following command lines:

Update Package Lists:
- <code>sudo apt update</code>

Install Required Dependencies:
- <code>sudo apt install apt-transport-https ca-certificates curl software-properties-common</code>

Add Docker GPG Key:
- <code>curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg</code>

Add Docker Repository:
For the stable version:
- <code>echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null</code>

Update Package Lists Again:
- <code>sudo apt update</code>

Install Docker:
- <code>sudo apt install docker-ce docker-ce-cli containerd.io</code>

Verify Docker Installation:
- <code>sudo docker --version</code>

Add Your User to the Docker Group:
This step allows you to run Docker commands without using sudo each time. Replace `your-username` with your actual username (our was ubuntu).
- <code>sudo usermod -aG docker your-username</code>

Restart Your System:
For the group changes to take effect, you may need to restart your system or log out and log back in.
Test Docker:

Run a simple test to ensure Docker is working correctly:
- <code>docker run hello-world</code>

### 1Bis. Install docker-compose on you VM

Run the following command lines:
- <code>sudo apt install docker-compose</code>
- <code>sudo apt update</code>

### 2. Open Port 3000/8000/9000 and 80/443 on the VM

This step will enable your VM to accept communications from these previous ports, which is key if you want your website to be online:
- <code>sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT</code>
- <code>sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT</code>
- <code>sudo iptables -A INPUT -p tcp --dport 9000 -j ACCEPT</code>
- <code>sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT</code>
- <code>sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT</code>
- <code>sudo iptables-save | sudo tee /etc/iptables/rules.v4</code>

Verify changes:
- <code>sudo iptables -L -n</code>

### 3. Add certificate to Domain Name

If you want your website to be under a https url, you need to add certificates to authentify it.

Install certbot:
- <code>sudo apt-get install python3-certbot-nginx</code>

(
If you need to install python3 for the previous one, here are the command lines:
- <code>sudo apt update</code>
- <code>sudo apt install python3</code>
)

Add certificate:
<code>sudo certbot --nginx</code>

### 4. Add authentication to the webpage:

If you want to add a login interface where you need to log in before accessing the chatbot (`your-username` was *admin* for us and the password was the one we gave you on Teams).

Run the following command lines:
- <code>sudo apt-get update</code>
- <code>sudo apt-get install apache2-utils</code>

Create your credentials:
- <code>sudo htpasswd -c /etc/nginx/.htpasswd your-username</code>

### 5. Create the nginx configuration file for this project

To apply the previous certificates, the authentication process and use your domain name to access your online chatbot, you need to create and modify the `nginx.con` file (this file is present in `final_version/nginx/nginx.conf` so if you want to modify it in the future, modify it there and run the CI/CD of gitlab, but for now stay in the VM terminal).

First, run the following command line:
- <code>sudo nano  /etc/nginx/sites-available/fastapi-app</code>

Then, copy paste this:
<pre>
server {
    listen 80;
    server_name your-domain-name;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain-name;

    ssl_certificate /etc/letsencrypt/live/your-domain-name/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain-name/privkey.pem;

    client_max_body_size 200M;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }

    location /back/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }

    location /openapi.json {
        proxy_pass http://localhost:8000/openapi.json; 
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}
</pre>
To save and exit use the following touches:
- <code>control + x</code>
- <code>Y</code>
- <code>Enter</code>

Then, link it to the enabled sites:
- <code>sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/</code>

### 6. Create a repository on your VM to receive the project

Go in the following path on your VM: <pre>home/your-username/</pre>
Then create a new directory called `airules_final_version`:
- <code>mkdir airules_final_version</code>

Create a second directory inside the airules_final_version directory:
- <code>cd airules_final_version</code>
- <code>mkdir server</code>

In the new directory copy you .env file with the OpenAI API Key:
- <code>cd server</code>
- <code>sudo nano .env</code>

Copy paste your API Key:
<pre>
OPENAI_API_KEY= "your-openai-api-key"
</pre>
To save and exit use the following touches:
- <code>control + x</code>
- <code>Y</code>
- <code>Enter</code>

### 7. Run the gitlab CI/CD

Once you have done all these previous steps, you can run the `.gitlab-ci.yml` and it should intall all the project in your repository `airules_final_version` and run the dockerfiles. Don't forget to change the environment variables, accroding to your VM like the `SSH_HOST`, `SSH_USER`, `YOUR_DOMAIN_NAME` in the different files of the project. 

Here are where you need to modify these variables:

- For `YOUR_DOMAIN_NAME`:

You need to replace our domain name *f23-p2-airules.paris-digital-lab.fr* in every url by yours in the following files in your git repository:
1. Go in `final_version/client/components` and look for:
- `BrowsePdfButton.tsx`
- `ConversationArea.tsx`
- `FlightInfoSubForm.tsx`
- `FlightNumberSubForm.tsx`

2. In `final_version/nginx/nginx.conf` as said previously

3. In `final_version/docker-compose.yml` look into the volumes

- For `SSH_HOST` and `SSH_USER`:

You can modify them in your gitlab platform. Just go in `Settings > CI/CD > Variables`. You can add them here, where you added your gitlab private key before.
