# Uptime Robot CLI

CLI that uses [UptimeRobot REST API](https://uptimerobot.com/api/)

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
  delete-monitor      Delete a monitor
  edit-alert-contact  Edit Alert contacts
  edit-monitor        Edit a monitor
  get-alert-contacts  Get Alert contacts
  get-monitors        Get all monitors
  new-monitor         Create a monitor
```

### List

```
$ uptimerobot get-monitors
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618397 | MY Frontend      | https://origin.example.com |        300 |
| 785618398 | MY Backend       | https://api.example.com    |        300 |
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
```

### Add

```
$ uptimerobot new-monitor -u https://api.example.sg -n 'SG Backend' -i 600
785618400

$ uptimerobot list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618397 | MY Frontend      | https://origin.example.com |        300 |
| 785618398 | MY Backend       | https://api.example.com    |        300 |
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
| 785618400 | SG Backend       | https://api.example.sg     |        600 |
```

### Edit

```
$ uptimerobot edit-monitor -i 785618400 -n 'SG API'
$ uptimerobot list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618397 | MY Frontend      | https://origin.example.com |        300 |
| 785618398 | MY Backend       | https://api.example.com    |        300 |
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
| 785618400 | SG API           | https://api.example.sg     |        600 |
```

### Delete

```
$ uptimerobot delete-monitor -i 785618397
$ uptimerobot delete-monitor -i 785618398
$ uptimerobot list
|        id | friendly_name    | url                        |   interval |
|-----------|------------------|----------------------------|------------|
| 785618399 | SG Frontend      | https://origin.example.sg  |        300 |
| 785618400 | SG API           | https://api.example.sg     |        600 |
```

### Alert Contacts

```
$ uptimerobot get-alert-contacts
|      id | friendly_name    | value        |
|---------|------------------|--------------|
| 1234567 | me@example.com   | John Doe     |
| 1234568 | foo@bar.buzz     | Foo Bar      |
```
