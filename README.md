# freemobile_selfsms

Send SMS to yourself (useful only for subscribers of the french mobile operator "Free")

# config

Initialize configuration `cp sms.py.conf.dist ~/sms.py.conf`

Modify configuration and set `user` and `password` in the `auth` section

# usage

Whatever you pipe to the python script will be send to your mobile phone

Example 1:

	echo "test" | ./sms.py


Example 2:

	./sms.py
	my text
	test
	CTRL-D

You will receive the provided text in an SMS

*Note: the text is trimmed from whitespaces at start and end of input*
