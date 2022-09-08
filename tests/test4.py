import requests

data = {
"firebase_id": "dYMacoDf4ko:APA91bHPuFN-2h_Idl6vNWO_ESfv_f7R0YBN0mtRfBrnjPAF1KVSfRNE_UkAIKReLJBouRMc2x54hnZzED8dXkB-Syt9w3tZnMmU-ytrMmXAeCc9gN_5WhhEbtxZghrgX6N378U8Bj4A",
"event": "feedback",
"msg": "test123"
}
# data = {
#     "login": "Matvey_gurov",
#     "password": "d37645bd046b6b890cb4eb18b55d37027b0757c87b98ae4a5083e72b2b60aa70",
#     "firebase_id": "dYMacoDf4ko:APA91bHPuFN-2h_Idl6vNWO_ESfv_f7R0YBN0mtRfBrnjPAF1KVSfRNE_UkAIKReLJBouRMc2x54hnZzED8dXkB-Syt9w3tZnMmU-ytrMmXAeCc9gN_5WhhEbtxZghrgX6N378U8Bj4A",
#     "ver": "test"
# }
r = requests.post('http://127.0.0.1:5000/new_event', data=data)
print(r.status_code)
print(r.text)
