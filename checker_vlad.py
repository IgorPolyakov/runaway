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


DEBUG = False
PORT = 9999
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
PERSONS = [
	'Kutuzov',
			'Marilyn Monroe',
			'Abraham Lincoln',
			'Mother Teresa',
			'John F. Kennedy',
			'Martin Luther King',
			'Nelson Mandela',
			'WinstonChurchill',
			'Bill Gates',
			'Muhammad Ali',
			'Mahatma Gandhi',
			'Margaret Thatcher',
			'Christopher Columbus',
			'George Orwell',
			'Charles Darwin',
			'Elvis Presley',
			'Albert Einstein',
			'Paul McCartney',
			'Queen Elizabeth II',
			'Queen Victoria',
			'Anna Akhmatova',
			'Sandra Bullock',
			'Vincent van Gogh',
			'Bill Gates',
			'Selena Gomez',
			'Celine Dion',
			'Kylie Minogue',
			'Elvis Presley',
			'Freddie Mercury',
			'Justin Timberlake',
			'Robbie Williams',
			'Thomas Alva Edison',
			'Viktor Tsoi',
			'Michail Sholokhov',
			'William Shakespeare',
			'Yuri Shevchuk',
			'Arnold Schwarzenegger',
			'Sharapova, Maria',
			'Alfred Hitchcock',
			'Uma Thurman',
			'John Travolta',
			'Alla Pugacheva',
			'Brad Pitt',
			'Till Lindemann',
			'Richard Z. Kruspe',
			'Paul H. Landers',
			'Oliver "Ollie" Riedel',
			'Christian "Flake" Lorenz',
			'Christoph "Doom" Schneider',
			'Jimmy Page',
			'John Bonham',
			'Robert Plant',
			'John Paul Jones',
			'Axl Rose',
			'Angus Young',
			'Stevie Young',
			'Chris Slade',
			'Steven Tyler',
			'Joe Perry',
			'Tom Hamilton',
			'Joey Kramer',
			'Brad Whitford',
			'Slash',
			'Duff McKagan',
			'Dizzy Reed',
			'Richard Fortus',
			'Frank Ferrer',
			'Melissa Reese',
			'Steve Harris',
			'Dave Murray',
			'Adrian Smith',
			'Bruce Dickinson',
			'Nicko McBrain',
			'Janick Gers',
			'Brian May',
			'Roger Taylor',
			'Freddie Mercury',
			'John Deacon',
			'Mike Grose',
			'Doug Bogie',
			'Barry Mitchell',
			'John Lennon',
			'Paul McCartney',
			'Ringo Starr',
			'George Harrison',
			'Stuart Sutcliffe',
			'Pete Best',
			'Mick Jagger',
			'Keith Richards',
			'Ronnie Wood',
			'David Gilmour',
			'Roger Waters',
			'Syd Barrett',
			'Richard Wright',
			'Nick Mason',
			'Jon Bon Jovi',
			'Tico Torres',
			'David Bryan',
			'Hugh McDonald',
			'Richie Sambora',
			'Alec John Such',
			'Dave Sabo',
			'Kurt Cobain',
			'Dave Grohl',
			'Krist Novoselic',
			'Pat Smear',
			'Ian Gillan',
			'Ian Paice',
			'Roger Glover',
			'Steve Morse',
			'Victor Minin',
			'One person',
]
DATA = [
	[
		PERSONS,
		[
			' was born',
			' got married',
			' bought a horse',
			' bought a house',
			' saw a Ursa Major Constellation',
			' bought his first slave',
			' watched first episode of "Big Bang Theory"',
			' saw the end of the world',
			' broke free from jail',
			' had 3 takos',
			' washed hair with mayonnaise',
			' saw Britney Spears sing live',
			' shaved eyebrows off',
			' dropped phone in the toilet',
			' had a threesome in a bathtub',
			' ate a moldy jogurt',
			' lost virginity',
			' rode a ostrich',
			' wrote a loveletter to the president',
			' found a sock under the bed',
			' tried Mexican food and shit pants',
			' got pig-drunk at a kid\'s party',
			' stalked a clown',
			' read "1984" and didn\'t like it',
			' hacked FBI server',
			' pooped in a library',
			' tried smoking pot',
			' harrased a police officer',
			' hugged koala',
			' robbed a bank with a squirt gun',
			' smuggled heroin and sanctioned cheese',
			' dyed dog\'s hair pink',
			' enjoyed "Desperate Housewives"',
			' ran from furious religious fanatics',
			' betrayed a friend for an ice-cream',
			' licked an oldman',
			' hit a woman with the car',
			' hated the taste of failure',
			' bought a bouncing ball',
			' was a fan of curling',
			' couldn\'t open a jar of pickles',
			' asked mom\'s permission to hang out with friends',
			' thought cats were devil\'s children',
			' farted',
			' cried when Mufasa died',
			' cried when his favourite pizza place closed',
		],
		[
			' in ',
		],
		[lambda: str(randint(1, 2016))],
		['.',],
	],
	[
		PERSONS,
		[
			' tried to ride a bike without legs',
			' tried to ride a bike without hands',
			' tried to ride a bike without brains',
			' tried to hook a hooker',
			' tried to perform a strip dance',
			' tried to understand zebras',
			' tried talking to a girl',
			' tried to pass probability theory exam',
			' tried to win SibirCTF',
			' tried to find the second sock',
			' really wanted to be able to want to be able to',
		],
		[
			' and failed',
			' and cried',
			' and exploded',
			' and set everything on fire',
			' and made his parents disappointed',
			' and knew the essence of being',
			' and save the Universe',
			' and destroy the Universe',
			' and become the secret agent',
			' and become the president',
			' and couldn\'t',
		],
		[' in the age of ',],
		[lambda: str(randint(1, 100))],
		['.'],
	],
	[
		[
			'Chapelnik',
			'Stupidity',
			'Laziness',
			'Left sock',
			'Tea-bag cup',
			'Figured grass',
			'Clown nose',
			'Harry Potter',
			'Eyebrow tweezing',
			'Shaved cat',
			'Portable Chin Rest',
			'Control Alt Delete Wand',
			'Baby Mop',
			'Car Exhaust Grill',
			'Head Mounted Toilet Paper Dispenser',
			'Two Person Sweatshirt',
			'Lipstick Assistant',
			'Shoe Umbrella',
			'Swiss Army Shovel',
			'Noodle Fan',
			'Snowball Maker',
			'Subway Sleep Guard',
			'Total Body Umbrella',
			'Diet Water',
			'DVD Rewinder',
			'Attack-defence CTF',
			'Jeopardy',
			'V. V. Jirinovskiy',
			'Recursive watering can',
			'High-heels flipper',
			'Alcohol fire extinguisher',
			'Massacres',
		],
		[' was invented by ',],
		PERSONS,
		[
			' by order of the Ministry of Defence.',
			' in order to rule the world.',
			' in order to fix consequences of last invention.',
			' after the death.',
			' after the date with Lenin.',
			' after the second Apocalypse.',
			' and Jason Stathem.',
			' after knife felt through leg.',
			' after visit to the end of the world.',
			' after years of surviving on the uninhabited island.',
			' after IBM breakdown.',
			' after recognition of independence screech-owl\'s.',
			' after SibirCTF 2015',
			' after first scoreboard blackout.',
			' after trying to organize an attack-defence game.',
			' after hacking the Pentagon.',
			' after drinking away.',
			' to cheat a headmaster.',
			' in order to money laundering.',
			' in order to become kawaii japanese schoolgirl.',
		],
	],
]


def _encode(string: str=None) -> str:
	string = '' if string is None else string
	return md5(str(string+SALT).encode()).hexdigest()


def _random_string(length: int=None) -> str:
	length = 32 if length is None else length
	return ''.join(choice(ascii_letters) for i in range(length))


def _fact() -> str:
	table = choice(DATA)
	res = list()
	for column in table:
		res.append(
			choice(
				column
			) if not isinstance(
				column[0],
				type(lambda: True)
			) else column[0]()
		)
	return ''.join(res)


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
		if search('Welcome', page):
			return EXIT_CODES['OK']
		else:
			return EXIT_CODES['Bad answer']


def _put(hostname: str=None, flag_id: str=None, flag: str=None) -> int:
	if not hostname or not flag_id or not flag:
		return EXIT_CODES['Need more args']
	else:
		query = {
			'username': flag_id,
			'email': '{}@{}.{}'.format(
				_random_string(16),
				_random_string(16),
				_random_string(2),
			),
			'first_name': _random_string(8),
			'last_name': _random_string(16),
			'address': _random_string(32),
			'cin': flag,
			'password': _encode(flag_id),
		}
		try:
			response = urlopen(
				'http://{hostname}:{port}/api/user/add?{query}'.format(
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
	# if DEBUG:
	# 	for i in range(200):
	# 		_put('localhost', _random_string(32), _random_string(32))
	# 	exit(0)
	if DEBUG:
		exit_code = main()
		for key, value in EXIT_CODES.items():
			if exit_code == value:
				print(key, ': ', value, sep='')
				break
		exit(exit_code)
	else:
		exit(main())
