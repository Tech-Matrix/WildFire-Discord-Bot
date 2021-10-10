# WildFire-Discord Bot

Video Link: https://drive.google.com/drive/folders/1p6UIyd1uQh9eCCpmvZtZAFplHAmh-yYv

Medium Link: https://medium.com/newolf-society/wildfire-a-bot-to-keep-your-server-interactions-friendly-142b1a30114b


## Development

### Using docker
1. Requires Docker and docker-compose.
2. Create a `.env` file and add the following:
    ```bash
    BOT_TOKEN=<TOKEN>
    ```
3. Start bot and database: `docker-compose up`
4. Start only bot: `docker-compose up --no-deps ib7` **or** start only database: `docker-compose up postgres`
5. Stopping the containers: `docker-compose stop`
6. Cleanup networks, containers: `docker-compose down`
7. Clear volumes: `docker-compose down --volumes`
