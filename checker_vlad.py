#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import argv, exit
from hashlib import md5
from string import ascii_letters
from random import choice, randint
from urllib.request import urlopen
from urllib.parse import urlencode
from json import loads
from re import search
from faker import Factory


DEBUG = False
GENERATE = False
PORT = 3000
SALT = 'W311C0M3_T0_51B1RCTF'
TIMEOUT = 5
EXIT_CODES = {
	'Wrong args':	   111,
	'Need more args':   110,
	'Host unreachable': 104,
	'Bad answer':	   103,
	'Flag not found':   102,
	'OK':			   101,
}
COMMANDS = (
	'check',
	'get',
	'put',
)

def _encode(string: str=None) -> str:
	string = '' if string is None else string
	return md5(str(string+SALT).encode()).hexdigest()


def _random_string(length: int=None) -> str:
	length = 32 if length is None else length
	return ''.join(choice(ascii_letters) for i in range(length))


def _check(hostname: str=None) -> int:
	if not hostname:
		return EXIT_CODES['Need more args']
	else:
		try:
			response = urlopen(
				'http://{hostname}:{port}/'.format(
					hostname=hostname,
					port=PORT,
				),
				timeout=TIMEOUT,
			)
		except:
			return EXIT_CODES['Host unreachable']
		page = response.read().decode()
		if search('Runaway', page):
			return EXIT_CODES['OK']
		else:
			return EXIT_CODES['Bad answer']


def _put(hostname: str=None, flag_id: str=None, flag: str=None) -> int:
	faker = Factory.create()
	if not hostname or not flag_id or not flag:
		return EXIT_CODES['Need more args']
	else:
		query = {
			'name': flag_id,
			'email': flag_id+'@example.com',
			'address': faker.address(),
			'password': _encode(flag_id),
			'password_confirm': _encode(flag_id),
		}
		try:
			response = urlopen(
				'http://{hostname}:{port}/users?{query}'.format(
					hostname=hostname,
					port=PORT,
					query=urlencode(query),
				),
				timeout=TIMEOUT
			)
		except:
			return EXIT_CODES['Host unreachable']
		json = loads(response.read().decode())
		if json['status'] == 'OK':
			query = {
				'username': query['username'],
				'password': query['password'],
			}
			try:
				response = urlopen(
					'http://{hostname}:{port}/api/user/login?{query}'.format(
						hostname=hostname,
						port=PORT,
						query=urlencode(query),
					),
					timeout=TIMEOUT,
				)
			except:
				return EXIT_CODES['Host unreachable']
			json = loads(response.read().decode())
			if json['status'] == 'OK':
				query = {
					'username': query['username'],
					'token': json['data']['token']['token'],
					'description': _fact(),
					'case_number': flag,
				}
				try:
					response = urlopen(
						'http://{hostname}:{port}/api/fact/add?{query}'.format(
							hostname=hostname,
							port=PORT,
							query=urlencode(query),
						),
						timeout=TIMEOUT,
					)
				except:
					return EXIT_CODES['Host unreachable']
				json = loads(response.read().decode())
				if json['status'] == 'OK':
					return EXIT_CODES['OK']
				else:
					return EXIT_CODES['Bad answer']
			else:
				return EXIT_CODES['Bad answer']
		else:
			return EXIT_CODES['Bad answer']


def _get(hostname: str=None, flag_id: str=None, flag: str=None) -> int:
	if not hostname or not flag_id or not flag:
		return EXIT_CODES['Need more args']
	else:
		query = {
			'username': flag_id,
			'password': _encode(flag_id),
		}
		try:
			response = urlopen(
				'http://{hostname}:{port}/api/user/login?{query}'.format(
					hostname=hostname,
					port=PORT,
					query=urlencode(query),
				),
				timeout=TIMEOUT,
			)
		except:
			return EXIT_CODES['Host unreachable']
		json = loads(response.read().decode())
		if json['status'] == 'OK':
			query = {
				'username': query['username'],
				'token': json['data']['token']['token'],
				'object_username': query['username'],
				'limit': 1,
			}
			try:
				response = urlopen(
					'http://{hostname}:{port}/api/fact/list?{query}'.format(
						hostname=hostname,
						port=PORT,
						query=urlencode(query),
					),
					timeout=TIMEOUT,
				)
			except:
				return EXIT_CODES['Host unreachable']
			json = loads(response.read().decode())
			if json['status'] == 'OK' and \
					json['data'][0] and \
					json['data'][0]['case_number'] == flag:
				return EXIT_CODES['OK']
			else:
				return EXIT_CODES['Bad answer']
		else:
			return EXIT_CODES['Bad answer']


def main() -> int:
	(
		name,
		cmd,
		hostname,
		flag_id,
		flag,
	) = (
		None if not argv else argv.pop(0)
		for i in range(5)
	)

	if cmd:
		if cmd in COMMANDS:
			if hostname:
				if cmd != 'check':
					if flag_id and flag:
						if cmd == 'put':
							return _put(hostname, flag_id, flag)
						if cmd == 'get':
							return _get(hostname, flag_id, flag)
					else:
						return EXIT_CODES['Need more args']
				else:
					return _check(hostname)
			else:
				return EXIT_CODES['Need more args']
		else:
			return EXIT_CODES['Wrong args']
	else:
		return EXIT_CODES['Need more args']


if '__main__' == __name__:
	if DEBUG and GENERATE:
		for i in range(200):
			_put('localhost', _random_string(32), _random_string(32))
		exit(0)
	if DEBUG:
		exit_code = main()
		for key, value in EXIT_CODES.items():
			if exit_code == value:
				print(key, ': ', value, sep='')
				break
		exit(exit_code)
	else:
		exit(main())
