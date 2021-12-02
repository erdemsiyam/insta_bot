Requestler [
	
	// Başlangıç
	from instabot import Bot
	bot = Bot()
	USERNAME = "egonomi_coh_eyi"
	PASSWORD = "lordkont81"
	USERNAME2 = 'loudwhisper666'
	PASSWORD2 = "lordkont81"
	
	bot.login(username=USERNAME, password=PASSWORD)
	
	// Kendi Kullanıcı Id mizi çekme
	try:
		user_id = bot.get_user_id_from_username(USERNAME)
	except Exception as e:
		bot.logger.error(e)
	
	// Takip Edenler By UserId
	data = bot.api.get_total_followers_or_followings(user_id=user_id)
	[
		{
			"pk": 37751567301,
			"username": "bengu_glroglu",
			"full_name": "Bengü 🍁",
			"is_private": true,
			"profile_pic_url": "https://instagram.fist4-1.fna.fbcdn.net/v/t51.2885-19/s150x150/158038096_154049206571956_2045446868790495403_n.jpg?tp=1&_nc_ht=instagram.fist4-1.fna.fbcdn.net&_nc_ohc=fGwe6TBYztUAX869GbB&edm=APQMUHMBAAAA&ccb=7-4&oh=e245eeeec0eb7567bab427d58cb6d29e&oe=60E1444E&_nc_sid=e5d0a6",
			"profile_pic_id": "2525405431066291916_37751567301",
			"is_verified": false,
			"follow_friction_type": 0,
			"has_anonymous_profile_picture": false,
			"account_badges": [],
			"latest_reel_media": 0,
			"story_reel_media_ids": []
		},
		{
			"pk": 27040539695,
			"username": "cigdemaydogdu77",
			"full_name": "cigdem_aydogdu77",
			"is_private": true,
			"profile_pic_url": "https://instagram.fohs1-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fohs1-1.fna.fbcdn.net&_nc_ohc=xnNK3l77n2YAX8oQiBF&edm=ABmJApABAAAA&ccb=7-4&oh=3c4a4fe7e71c2ff32643f748cd1e2226&oe=60E070CF&_nc_sid=6136e7&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4",
			"is_verified": false,
			"follow_friction_type": 0,
			"has_anonymous_profile_picture": true,
			"account_badges": [],
			"latest_reel_media": 0,
			"story_reel_media_ids": []
		},
		{
			"pk": 5786290253,
			"username": "omerrxd_",
			"full_name": "Ömer Karagöz",
			"is_private": true,
			"profile_pic_url": "https://instagram.fohs1-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fohs1-1.fna.fbcdn.net&_nc_ohc=xnNK3l77n2YAX8oQiBF&edm=ABmJApABAAAA&ccb=7-4&oh=3c4a4fe7e71c2ff32643f748cd1e2226&oe=60E070CF&_nc_sid=6136e7&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4",
			"is_verified": false,
			"follow_friction_type": 0,
			"has_anonymous_profile_picture": true,
			"account_badges": [],
			"latest_reel_media": 0,
			"story_reel_media_ids": []
		}
	]
	
	// Username in ID karşılığı 
	bot.get_user_id_from_username('loudwhisper') // 1580873724
	
	// ID nin username karşılığı
	bot.get_username_from_user_id(1580873724) // loudwhisper
	
	// X username kullanıcı bilgileri
	bot.get_user_info('loudwhisper')
	
	// X username yi takip edenler
	bot.get_user_followers(ID) // ['1723703964',...]
	bot.get_user_followers(username)
	
	// X username in takip ettikleri
	bot.get_user_following(ID)
	bot.get_user_following(username)
	[
		'267235346',
		'1337980423',
		'256834429',
		'35942958',
		'250128381',
		'290282816',
		'26393455',
		'583121025',
		'214827333',
		'175334934',
		'33562772',
		'392580955',
		'20405196',
		'293947766',
		'1811651'
	]
	
	// Takip At
	bot.follow(ID)
	bot.follow(username)

	// Takip Bırak
	bot.unfollow(ID)
	bot.unfollow(username)
	
	// Foto indir
	// Foto yükle
	
	// Video indir
	// Video yükle
	
	// Hikaye indir
	// Hikaye yükle
	
	
]