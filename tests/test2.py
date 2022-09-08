from eschool.eschool_server import EschoolServer
from firebase.firebase_user import FirebaseUser

username = "Matvey_gurov"
password = "d37645bd046b6b890cb4eb18b55d37027b0757c87b98ae4a5083e72b2b60aa70"
firebase_id = "dYMacoDf4ko:APA91bHPuFN-2h_Idl6vNWO_ESfv_f7R0YBN0mtRfBrnjPAF1KVSfRNE_UkAIKReLJBouRMc2x54hnZzED8dXkB-Syt9w3tZnMmU-ytrMmXAeCc9gN_5WhhEbtxZghrgX6N378U8Bj4A"
server = EschoolServer()
user: FirebaseUser = FirebaseUser(username, password, server, firebase_id)
user.state()
print(user.get_marks())
print(user.get_new_msgs())
print(user.send_msgs())
