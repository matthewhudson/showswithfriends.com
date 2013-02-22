from app.dal import (create_model_by_name,
	get_session)

from app.models.tables import User

user_dicts = [
	{
		"user_id" : 36,
		"lat" : 40.75,
		"lon" : -74,
		"city" : "New York",
		"state" : "NY",
		"email" : 'jack@seatgeek.com',
		"sg_access" : 255,
		"fist_name" : "Jack",
		"last_name" : "Groetzinger"
	},
	{
		"user_id" : 1662,
		"lat" : 40.75,
		"lon" : -74,
		"city" : "New York",
		"state" : "NY",
		"email" : 'erwaller@gmail.com',
		"sg_access" : 255,
		"first_name" : "Eric",
		"last_name" : "Waller"
	},
	{
		"user_id" : 2420,
		"lat" : 40.75,
		"lon" : -74,
		"city" : "New York",
		"state" : "NY",
		"email" : 'jose@seatgeek.com',
		"sg_access" : 255,
		"first_name" : "Jose",
		"last_name" : "Diaz-Gonzalez"
	},
	{
		"user_id" : 6581,
		"lat" : 40.75,
		"lon" : -74,
		"city" : "New York",
		"state" : "NY",
		"email" : 'nihar@seatgeek.com',
		"sg_access" : 128,
		"first_name" : "Nihar",
		"last_name" : "Singhal"
	},
	{
		"user_id" : 25949,
		"lat" : 40.75,
		"lon" : -74,
		"city" : "New York",
		"state" : "NY",
		"email" : 'adam@seatgeek.com',
		"sg_access" : 255,
		"first_name" : "Adam",
		"last_name" : "Cohen"
	}
]

def add_users(session):
	for user in user_dicts:
		session.merge(User(user))
	session.commit()


def main():
	session = get_session()
	try:
		session.query(User)
	except:
		create_model_by_name('User')
		create_model_by_name('UserPerformerPreference')
		create_model_by_name('UserEventAffinity')
		create_model_by_name('Friendship')

	add_users(session)

if __name__ == '__main__':
	main()