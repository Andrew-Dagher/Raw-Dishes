
from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
import database
import auth
import uuid
import Back_end_ai as ai
from Back_end_ai import AITrain
from writeToCSV import writeToOutput
app = Flask(__name__)

app.config["SECRET_KEY"] = 'bbb07774f2284417a9303684df7c1470'


def Start():
    AITrain()


def transfer_data(func):
    
    @wraps(func)
    def SendDataToAI():
        field1 = request.args.get('field1')
        field2 = request.args.get('field2')
        field3 = request.args.get('field3')
        field4 = request.args.get('field4')
        field5 = request.args.get('field5')
        field6 = request.args.get('field6')
        field7 = request.args.get('field7')
        field8 = request.args.get('field8')
        fieldList = [field1,field2,field3,field4,field5,field6,field7,field8]
        database.AddInputRow(field1,field2,field3,field4,field5,field6,field7,field8) #store the inputs to the database
        # store to csv
        writeToOutput(fieldList)
        ai.AIReturn()

        # here to add more answerfields
    return SendDataToAI




@app.route('/sendDataManual')
@transfer_data
def transferData():
    pass

@app.route('/sendDataFacial')
def transferDataFacial():
    pass


def Debug():
    # gender: 0,1
    # mood: 0,1,2
    # dollarinos: 0,1,2
    # last_meal: 0,1,2
    # surprise: 0,1
    # age: 18 to 70
    # origin: 0, 1
    # romantic: 0,1,2
 
    dataTest = [0,1,1,0,1,18,0,2]
    writeToOutput(dataTest)
    result = ai.AIReturn()
    print(result)
    print(database.toJson(dataTest))
    database.AddAIRow(database.toJson(dataTest), result)

Start()

x = input("start?")
Debug()


if __name__ == "__main__":
    app.run(debug=False)