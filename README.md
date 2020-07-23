# Uptime Robot CLI

## Install

```
pip install -r requirements.txt
```

## Usage

First, export `UPTIMEROBOT_API_KEY` with proper API key. For example,

```
export UPTIMEROBOT_API_KEY=u12345678-7d4c23d189a04051b88a565f7
```

Then use the CLI like this.

```
Usage: uptimerobot.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a monitor
  delete  Delete a monitor
  edit    Edit a monitor
  list    List all monitors
```

### List

```
$ urctl list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618397 | MY Frontend      | https://origin.example.com |        300 |
| 785618398 | MY Backend       | https://api.example.com    |        300 |
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
```

### Add

```
$ urctl add -u https://api.example.sg -n 'SG Backend' -i 600
785618400

$ urctl list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618397 | MY Frontend      | https://origin.example.com |        300 |
| 785618398 | MY Backend       | https://api.example.com    |        300 |
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
| 785618400 | SG Backend       | https://api.example.sg     |        600 |
```

### Edit

```
$ urctl edit -i 785618400 -n 'SG API'
$ urctl list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618397 | MY Frontend      | https://origin.example.com |        300 |
| 785618398 | MY Backend       | https://api.example.com    |        300 |
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
| 785618400 | SG API           | https://api.example.sg     |        600 |
```

### Delete

```
$ urctl delete -i 785618397
$ urctl delete -i 785618398
$ urctl list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
| 785618400 | SG API           | https://api.example.sg     |        600 |
```
