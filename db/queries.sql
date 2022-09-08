-- select msg, username, school, time from stat s INNER JOIN users u on u.firebase_id = s.firebase_id order by time
--select clazz, count(firebase_id) from users group by clazz order by count(firebase_id) desc
-- select * from users where lastentry >= '2019-12-13' and ver !='1.5.1
-- select * from push where (success like '%"failure":1%') and (push not like '%определяемым%') order by dt DESC
-- select * from users where clazz = 'None'
-- select subject, markvalid, teachfio, username, clazz, school, lastentry, markdate, userid from marks  INNER JOIN users u on marks.userid = u.firebase_id
-- select * from push where firebase_id = 'dbCj2CzDtwI:APA91bHzeZPUWOEQurGkrrMs5FGxMW2h9x0M2Ej8kga5CzqrgWYMPfZcuXmpIwXkkLU1OtLfAi9Nd78-I-MU_xb4dWk19FHPmo6dzBca_t2ubvym-1ecuOs9KU2FHCv26LxVw0y5p1VY'
-- select * from marks
-- select * from

--SELECT * FROM users order by lastentry desc
select count(*) from marks
