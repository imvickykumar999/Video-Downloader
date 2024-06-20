># `Social Media Video Downloader`
>
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/251d4a04-aced-4652-8fde-41e4db0aa4e5)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/18431549-25d1-4c88-8762-4a0b2827c0d2)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/62b2ce53-7b13-4e17-b240-113ce2e52896)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/9940d5dc-a58e-4f3a-97e3-3dc9811d2f3a)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/79bb85ec-8f71-41ca-843b-4dd556dc229d)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/65359794-6aec-49c0-9a4e-f7ddc94a710b)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/ebfb9d2a-2877-4533-8e4e-370f51a5dc4d)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/32370e8a-ec35-4a8c-90ab-983d0f99b23f)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/9f54b14d-67b5-4651-aba5-7c2e376af8b9)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/1ef95e25-98f8-45c3-a338-58697cc4b0f4)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/bf7ac822-dbc3-4b7a-b36c-8905cd5ac94d)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/8e1bc2f7-e140-4207-8ed1-f171b4f5a1d4)
>![image](https://github.com/imvickykumar999/Video-Downloader/assets/50515418/868ea206-3508-4728-a68e-7d9862713473)

<br>

To configure `ALLOWED_HOSTS` correctly, you should include the following:

1. The local IP address (`192.168.0.18`).
2. `localhost` and `127.0.0.1` for local development.
3. The hostname if you plan to access the server using a hostname.
4. Optionally, `0.0.0.0` to allow all hosts (use with caution in development).

### Example Configuration

Here is an example of a comprehensive `ALLOWED_HOSTS` configuration for development:

**settings.py**:

```python
ALLOWED_HOSTS = [
    '192.168.0.18',  # Local network IP
    'localhost',     # Localhost access
    '127.0.0.1',     # Loopback address
    '0.0.0.0',       # Allows access from any host (useful for development, but use with caution)
]
```

### Running the Server

Ensure you run the server with the command:

```sh
python3 manage.py runserver 0.0.0.0:8000
```

### Accessing the Server

With the above configuration, you should be able to access the Django application using any of the following URLs:

1. From the same machine:
   - `http://localhost:8000`
   - `http://127.0.0.1:8000`

2. From other devices on the same local network:
   - `http://192.168.0.18:8000`

3. Optionally, if you have configured a hostname or a domain name, ensure it resolves to the correct IP address and add it to `ALLOWED_HOSTS`.

### Example

Assuming your local network IP is `192.168.0.18` and you want to access the Django server from another device on the same network, you can:

1. Run the server with:
   ```sh
   python3 manage.py runserver 0.0.0.0:8000
   ```

2. Open a web browser on another device and navigate to:
   ```sh
   http://192.168.0.18:8000
   ```

By following these steps, you should be able to access your Django application from different hosts in your development environment.
