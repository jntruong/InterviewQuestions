import json
from datetime import datetime

def calculate_time(start,end):
    start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    hours = (end_time - start_time).total_seconds() / 3600
    return hours

def calculate_wages(result, emp, duration, rate, benRate):
    #if regular work hours still less than 40hrs
    if result[emp]['regular'] + duration <= 40:
        result[emp]['regular'] += duration
        result[emp]['wageTotal'] += duration * rate
    #if work hours > 40hrs but regular work at begin less than 40hrs
    elif result[emp]['regular'] < 40 and result[emp]['regular'] + duration > 40 :
        overtime = duration - (40 - result[emp]['regular'])
        result[emp]['wageTotal'] += (40 - result[emp]['regular']) * rate + overtime * rate * 1.5
        result[emp]['regular'] = 40.0000
        result[emp]['overtime'] += overtime
    #if overtime less than 48hrs
    elif result[emp]['regular'] + result[emp]['overtime'] + duration <= 48:
        result[emp]['overtime'] += duration
        result[emp]['wageTotal'] += duration * rate * 1.5
    else:
        doubletime = duration - (48 - result[emp]['regular'] - result[emp]['overtime'])
        result[emp]['wageTotal'] += (48 - result[emp]['regular'] - result[emp]['overtime']) * rate * 1.5 + doubletime * rate * 2
        result[emp]['overtime'] = 48 - result[emp]['regular']
        result[emp]['doubletime'] += doubletime

    result[emp]['benefitTotal'] += duration * benRate

    return result

def getResult(json_data):
    jdata = json.loads(json.dumps(json_data))
    result={}
    for emp in jdata['employeeData']:
        name = emp['employee']
        result[name]={
            "employee": name,
            "regular": 0.0000,
            "overtime": 0.0000,
            "doubletime": 0.0000,
            "wageTotal": 0.0000,
            "benefitTotal": 0.0000
        }
        
        #get data and calculate for each TimePunch
        for tp in emp['timePunch']:
            job = tp['job']
            
            # get rate & benefit of today job working on
            for today_job in jdata['jobMeta']:
                if job == today_job['job']:
                    rate = today_job['rate']
                    benefitsrate = today_job['benefitsRate']
                    break
                else:
                    continue
            
            # calculate today work hours
            duration = calculate_time(tp['start'],tp['end'])
            
            # adding data into calculation
            calculate_wages(result,name,duration,rate,benefitsrate)
    return result

# Your JSON data
data = {
  "jobMeta": [
    {
      "job": "Hospital - Painter",
      "rate": 31.25,
      "benefitsRate": 1
    },
    {
      "job": "Hospital - Laborer",
      "rate": 20.0,
      "benefitsRate": 0.5
    },
    {
      "job": "Shop - Laborer",
      "rate": 16.25,
      "benefitsRate": 1.25
    }
  ],
  "employeeData": [
    {
      "employee": "Mike",
      "timePunch": [
        {
          "job": "Hospital - Laborer",
          "start": "2022-02-18 09:00:01",
          "end": "2022-02-18 11:28:54"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-18 12:29:33",
          "end": "2022-02-18 14:00:59"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-19 08:16:51",
          "end": "2022-02-19 10:00:11"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-19 11:11:06",
          "end": "2022-02-19 12:00:14"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-19 13:22:13",
          "end": "2022-02-19 17:16:32"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-20 06:50:12",
          "end": "2022-02-20 11:21:11"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-20 13:01:11",
          "end": "2022-02-20 17:52:45"
        },
        {
          "job": "Hospital - Laborer",
          "start": "2022-02-21 07:08:11",
          "end": "2022-02-21 12:22:33"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-21 13:15:10",
          "end": "2022-02-21 17:58:06"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-22 07:11:59",
          "end": "2022-02-22 11:00:01"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-22 12:16:54",
          "end": "2022-02-22 17:59:03"
        }
      ]
    },
    {
      "employee": "Steve",
      "timePunch": [
        {
          "job": "Hospital - Painter",
          "start": "2022-02-18 06:02:35",
          "end": "2022-02-18 11:28:54"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-18 12:31:06",
          "end": "2022-02-18 15:00:11"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-19 07:03:41",
          "end": "2022-02-19 10:00:45"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-19 10:24:58",
          "end": "2022-02-19 12:00:19"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-19 13:22:13",
          "end": "2022-02-19 17:16:32"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-20 05:56:00",
          "end": "2022-02-20 11:33:23"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-20 12:18:45",
          "end": "2022-02-20 17:48:41"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-21 06:02:28",
          "end": "2022-02-21 12:22:19"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-21 13:04:01",
          "end": "2022-02-21 17:52:06"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-22 06:00:58",
          "end": "2022-02-22 11:02:55"
        },
        {
          "job": "Hospital - Painter",
          "start": "2022-02-22 12:18:04",
          "end": "2022-02-22 17:48:41"
        }
      ]
    },
    {
      "employee": "Alex",
      "timePunch": [
        {
          "job": "Shop - Laborer",
          "start": "2022-02-18 06:05:55",
          "end": "2022-02-18 11:18:14"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-18 11:30:09",
          "end": "2022-02-18 14:00:01"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-19 07:18:22",
          "end": "2022-02-19 11:07:45"
        },
        {
          "job": "Hospital - Laborer",
          "start": "2022-02-19 12:04:18",
          "end": "2022-02-19 14:00:19"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-20 06:06:00",
          "end": "2022-02-20 10:13:23"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-20 12:18:45",
          "end": "2022-02-20 16:58:21"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-21 06:08:08",
          "end": "2022-02-21 12:20:55"
        },
        {
          "job": "Shop - Laborer",
          "start": "2022-02-21 12:54:30",
          "end": "2022-02-21 16:45:20"
        },
        {
          "job": "Hospital - Laborer",
          "start": "2022-02-22 06:09:14",
          "end": "2022-02-22 11:30:11"
        },
        {
          "job": "Hospital - Laborer",
          "start": "2022-02-22 12:00:29",
          "end": "2022-02-22 17:59:55"
        }
      ]
    }
  ]
}

print(json.dumps(getResult(data),indent=2))
