# Topic1
python crawler.py hashtag -t 인스타툰 -n 20 -o ./output/p1_all_1 --fetch_details
sleep 10
python crawler.py hashtag -t 인스타툰추천 -n 20 -o ./output/p1_all_2 --fetch_details
sleep 10
python crawler.py hashtag -t 인스타툰연재 -n 20 -o ./output/p1_all_3 --fetch_details
sleep 10
python crawler.py hashtag -t 인스타툰그램 -n 20 -o ./output/p1_all_4 --fetch_details
sleep 10
python crawler.py hashtag -t 일상툰 -n 20 -o ./output/p1_all_5 --fetch_details
sleep 10
python crawler.py hashtag -t 공감툰 -n 20 -o ./output/p1_all_6 --fetch_details
sleep 10
python crawler.py hashtag -t 생활툰 -n 20 -o ./output/p1_all_7 --fetch_details
sleep 10
python crawler.py hashtag -t 컷툰 -n 20 -o ./output/p1_all_8 --fetch_details
sleep 10
python crawler.py hashtag -t 일상만화 -n 20 -o ./output/p1_all_9 --fetch_details
sleep 10
python crawler.py hashtag -t 만화일기 -n 20 -o ./output/p1_all_10 --fetch_details
sleep 10
python crawler.py hashtag -t 그림일기 -n 20 -o ./output/p1_all_11 --fetch_details
sleep 10
python crawler.py hashtag -t 네컷만화 -n 20 -o ./output/p1_all_12 --fetch_details
sleep 10

#Topic2
#커플툰 #연애툰 #결혼툰 #신혼툰 #부부툰 #육아툰 #가족툰
python crawler.py hashtag -t 커플툰 -n 20 -o ./output/p2_love_1 --fetch_details
sleep 10
python crawler.py hashtag -t 연애툰 -n 20 -o ./output/p2_love_2 --fetch_details
sleep 10
python crawler.py hashtag -t 결혼툰 -n 20 -o ./output/p2_love_3 --fetch_details
sleep 10
python crawler.py hashtag -t 신혼툰 -n 20 -o ./output/p2_love_4 --fetch_details
sleep 10
python crawler.py hashtag -t 부부툰 -n 20 -o ./output/p2_love_5 --fetch_details
sleep 10
python crawler.py hashtag -t 육아툰 -n 20 -o ./output/p2_love_6 --fetch_details
sleep 10
python crawler.py hashtag -t 가족툰 -n 20 -o ./output/p2_love_7 --fetch_details
sleep 10

#Topic3
#(특정 캐릭터 이름) #고양이툰 #강아지툰 #동물툰
python crawler.py hashtag -t 고양이툰 -n 20 -o ./output/p3_character_1 --fetch_details
sleep 10
python crawler.py hashtag -t 강아지툰 -n 20 -o ./output/p3_character_2 --fetch_details
sleep 10
python crawler.py hashtag -t 동물툰 -n 20 -o ./output/p3_character_3 --fetch_details
sleep 10

#Topic4
#요리툰  #운동툰 #다이어트툰 #채식툰
python crawler.py hashtag -t 요리툰 -n 20 -o ./output/p4_hobby_1 --fetch_details
sleep 10
python crawler.py hashtag -t 운동툰 -n 20 -o ./output/p4_hobby_2 --fetch_details
sleep 10
python crawler.py hashtag -t 다이어트툰 -n 20 -o ./output/p4_hobby_3 --fetch_details
sleep 10
python crawler.py hashtag -t 채식툰 -n 20 -o ./output/p4_hobby_4 --fetch_details
sleep 10

#Topic5
#학생툰, 직장인툰, 직업툰, 알바툰, 약사툰, 널스툰, 카페툰 ...
python crawler.py hashtag -t 학생툰 -n 20 -o ./output/p5_job_1 --fetch_details
sleep 10
python crawler.py hashtag -t 직장인툰 -n 20 -o ./output/p5_job_2 --fetch_details
sleep 10
python crawler.py hashtag -t 직업툰 -n 20 -o ./output/p5_job_3 --fetch_details
sleep 10
python crawler.py hashtag -t 알바툰 -n 20 -o ./output/p5_job_4 --fetch_details
sleep 10
# python crawler.py hashtag -t 약사툰 -n 20 -o ./output/p5_job --fetch_details
# python crawler.py hashtag -t 널스툰 -n 20 -o ./output/p5_job --fetch_details
# python crawler.py hashtag -t 카페툰 -n 20 -o ./output/p5_job --fetch_details

#Topic6
#에세이툰 #감성툰 #힐링툰 #위로툰
python crawler.py hashtag -t 에세이툰 -n 20 -o ./output/p6_emotion_1 --fetch_details
sleep 10
python crawler.py hashtag -t 감성툰 -n 20 -o ./output/p6_emotion_2 --fetch_details
sleep 10
python crawler.py hashtag -t 힐링툰 -n 20 -o ./output/p6_emotion_3 --fetch_details
sleep 10
python crawler.py hashtag -t 위로툰 -n 20 -o ./output/p6_emotion_4 --fetch_details
sleep 10

#Run
python data_preprocess.py