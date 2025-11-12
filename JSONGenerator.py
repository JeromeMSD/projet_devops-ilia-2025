from datetime import datetime

def IncidentCreate(name, URL, impact):
        JSONObject = 
        {
    "page":{
        "id":"yh6f0r4529hb",
        "name":name
        "url": URL,
        "updated_at": datetime.now()
    },
    "incidents": [
        {
        "created_at": "2014-05-14T14:22:39.441-06:00",
        "id": "cp306tmzcl0y",
        "impact": impact,
        ],
        }
    ]
    }

    return JSONObject

