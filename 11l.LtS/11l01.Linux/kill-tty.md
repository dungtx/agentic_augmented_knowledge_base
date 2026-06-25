## Get current processes running on tty
`ps -t tty<no>`

## Get status via systemd
`systemctl status getty@tty<no>`

## Stop via systemd
`sudo systemctl disable getty@tty<no>`

## Kill the tty
`pkill -t tty<no>`