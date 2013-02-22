from app.dal import create_model_by_name

def main():
	create_model_by_name('User')
	create_model_by_name('UserPerformerPreference')
	create_model_by_name('UserEventAffinity')
	create_model_by_name('Friendship')

if __name__ == '__main__':
	main()