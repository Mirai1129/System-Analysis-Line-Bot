import datetime

profile = [
    {
        "name": "陳小豬",
        "password": "lmo1234",
        "age": 69,
        "address": "台北市中山區南京東路三段219號",
        "phone_number": "0912345678",
        "patient_id": "A10001"
    },
    {
        "name": "王小明",
        "password": "wsm2024",
        "age": 55,
        "address": "高雄市鼓山區龍德路12號",
        "phone_number": "0987654321",
        "patient_id": "A10002"
    },
    {
        "name": "李大華",
        "password": "ldh5678",
        "age": 43,
        "address": "台南市安平區健康路45號",
        "phone_number": "0977123456",
        "patient_id": "A10003"
    }
]

status = [
    {
        "patient_id": "A10001",
        "height": 150.69,
        "weight": 69,
        "blood_oxygen": 95.0,
        "blood_sugar": 110.0,
        "diastolic_pressure": 80.0,
        "systolic_pressure": 120.0,
        "blood_lipids": 200.0,
        "heart_rate": 72
    },
    {
        "patient_id": "A10002",
        "height": 160.0,
        "weight": 75,
        "blood_oxygen": 93.0,
        "blood_sugar": 105.0,
        "diastolic_pressure": 85.0,
        "systolic_pressure": 125.0,
        "blood_lipids": 180.0,
        "heart_rate": 78
    },
    {
        "patient_id": "A10003",
        "height": 170.5,
        "weight": 80,
        "blood_oxygen": 92.0,
        "blood_sugar": 100.0,
        "diastolic_pressure": 90.0,
        "systolic_pressure": 130.0,
        "blood_lipids": 190.0,
        "heart_rate": 80
    }
]

observe_list = [
    {
        "location": "屏東榮民醫院室外活動場",
        "observe_id": "OB10001",
        "observed_time": datetime.datetime(2024, 6, 4, 10, 42, tzinfo=datetime.timezone.utc),
        "patient_id": "A10001"
    },
    {
        "location": "高雄醫學大學附設中和紀念醫院",
        "observe_id": "OB10002",
        "observed_time": datetime.datetime(2024, 6, 5, 8, 30, tzinfo=datetime.timezone.utc),
        "patient_id": "A10002"
    },
    {
        "location": "台北市立聯合醫院和平院區",
        "observe_id": "OB10003",
        "observed_time": datetime.datetime(2024, 6, 6, 14, 15, tzinfo=datetime.timezone.utc),
        "patient_id": "A10003"
    }
]
exercise = [
    {
        "type": "健走",
        "duration_minutes": 30,
        "observe_id": "OB10001",
        "patient_id": "A10001"
    },
    {
        "type": "跑步",
        "duration_minutes": 45,
        "observe_id": "OB10002",
        "patient_id": "A10002"
    },
    {
        "type": "游泳",
        "duration_minutes": 60,
        "observe_id": "OB10003",
        "patient_id": "A10003"
    }
]

body_health = [
    {
        "blood_lipids": 156.69,
        "blood_oxygen": 90.69,
        "blood_sugar": 205.69,
        "consume_calories": 569.69,
        "diastolic_pressure": 50.69,
        "heart_rate": 147.69,
        "observe_id": "OB10001",
        "patient_id": "A10001",
        "systolic_pressure": 134.69
    },
    {
        "blood_lipids": 180.0,
        "blood_oxygen": 95.0,
        "blood_sugar": 210.0,
        "consume_calories": 600.0,
        "diastolic_pressure": 55.0,
        "heart_rate": 140.0,
        "observe_id": "OB10002",
        "patient_id": "A10002",
        "systolic_pressure": 140.0
    },
    {
        "blood_lipids": 200.0,
        "blood_oxygen": 92.0,
        "blood_sugar": 220.0,
        "consume_calories": 550.0,
        "diastolic_pressure": 60.0,
        "heart_rate": 150.0,
        "observe_id": "OB10003",
        "patient_id": "A10003",
        "systolic_pressure": 130.0
    }
]
