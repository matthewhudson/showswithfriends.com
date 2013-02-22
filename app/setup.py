from app.dal import (create_model_by_name,
	get_session)

from app.models.tables import (User,
	UserPerformerPreference,
	UserEventAffinity,
	Friendship)

from app.helpers import (add_affinity,
	add_friendships)

import json

def add_users(session):
	f = open('app/static/users.json', 'r')
	user_dicts = json.loads(f.read())
	for user in user_dicts:
		if user["first_name"]:
			session.merge(User(user))
	session.commit()

def add_preferences(session):
	pref_file = open('app/static/upp.json','r')
	user = session.query(User)
	active_user = None
	for line in pref_file:
		sg_id, performer_id = map(int,line.split(','))
		if not active_user:
			print sg_id
			active_user = user.filter(User.sg_id == sg_id).first()
		if active_user.sg_id != sg_id:
			print sg_id
			active_user = user.filter(User.sg_id == sg_id).first()
		try:
			upp = UserPerformerPreference(user_id=active_user.id, performer_id=performer_id)
		except:
			print active_user
		session.merge(upp)
	session.commit()

def main():
	session = get_session()
	try:
		u = session.query(User)
	except:
		create_model_by_name('User')
		create_model_by_name('UserPerformerPreference')
		create_model_by_name('UserEventAffinity')
		create_model_by_name('Friendship')
	u = session.query(User)
	if u.count() == 0:
		add_users(session)
	upp = session.query(UserPerformerPreference)
	if upp.count() == 0:
		add_preferences(session)
	users = session.query(User)
	for user in users:
		add_affinity(session, user)
	f = session.query(Friendship)
	if f.count() == 0:
		add_friendships(session, users)


if __name__ == '__main__':
	main()