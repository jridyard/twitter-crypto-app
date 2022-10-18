from datetime import datetime
from app import db
from app.home.imports import *

def removeOldTempKeys( purchaser ):
    print("Checking temp key history")

    for temp_key in purchaser.temp_keys:
        print("Temp Key Being Checked For Removal: " + temp_key.key)
        print(temp_key.dateUsed)
        if temp_key.dateUsed:
            duration = datetime.utcnow() - temp_key.dateUsed
            duration_in_s = duration.total_seconds()
            if duration_in_s > 90:
                print("Deleting temp key: " + temp_key.key)
                db.session.delete(temp_key)
    
    db.session.commit()

    return "Completed Process Of Removing Dated Keys"


def checkIfStillValid( temp_key ):

    last_used = temp_key.dateUsed

    if last_used == None:
        temp_key.dateUsed = datetime.utcnow()
        db.session.commit()
        return {
            'key_valid_check': True,
            'create_new_key': True
        }

    duration = datetime.utcnow() - temp_key.dateUsed
    duration_in_s = duration.total_seconds()

    if duration_in_s < 90:
        print(duration_in_s)
        print("Temp key " + temp_key.key + " still valid.")
        return {
            'key_valid_check': True,
            'create_new_key': False
        }

    return {
            'key_valid_check': False,
            'create_new_key': False
        }




def tryTempKey( temp_key ):

    temp_key_storage = TempKeys.query.filter( TempKeys.key == temp_key ).first()

    if temp_key_storage:
        purchaser = temp_key_storage.purchaser

        was_temp_key_valid_recently = checkIfStillValid( temp_key_storage )

        removeOldTempKeys( temp_key_storage.purchaser ) ### THIS function only runs for one purpose: delete old, no longer potentially valid temp keys.

        if was_temp_key_valid_recently['key_valid_check'] == True:

            if was_temp_key_valid_recently['create_new_key'] == True:
                new_key = createCode()
                purchaser.api_access_code = new_key
                temp_key = TempKeys(
                    key = new_key,
                    purchasers_id = purchaser.id
                )
                db.session.add(temp_key)
                db.session.commit()
                return {
                    'message': 'Temp key used from temp key history, new key created',
                    'new_key': new_key
                }
            
            # create_new_key = False
            return {
                'message': 'Temp key used from temp key history, first used within last 90s, therefore still valid.',
                # 'key_used': temp_key
            }

        # key_valid_check = False
        return {
            'message': 'Temp key was used too long ago.',
        }

    # temp_key_storage = Null
    return {
        'message': 'This temp key does not exist or was used too long ago.'
    }
    
    # new_key = createCode()

    # passed_temp_key = TempKeys.query.filter( TempKeys.key == temp_key ).first()
    # passed_temp_key.dateUsed = datetime.utcnow()
    
    # purchaser.api_access_code = new_key
    # temp_key = TempKeys(
    #     key = new_key,
    #     purchasers_id = purchaser.id
    # )
    # db.session.add(temp_key)
    # db.session.commit()
    
    # return {
    #     'message': 'Key was valid.'
    #     'new_key': new_key
    # }