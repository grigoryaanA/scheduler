import json


def create_schedule(data):
    """
    :param data: timetable data to work with
    :return: returns scheduled data to write in output json file
    """

    schedule = {}
    for teacher in data["teachers"]:
        schedule[teacher["name"] + " " + teacher["surname"]] = {"weekday": {}, "free_time": 0}
        for subject in data["subjects"]:
            for cls in data["classes"]:
                if subject["name"] in cls["taught_subjects"]:
                        if subject["name"] in teacher["profession"]:
                            schedule[teacher["name"] + " " + teacher["surname"]]["weekday"][cls["name"]] = {
                                "subject": subject["name"],
                                "start_time": None,
                                "end_time": None,
                                "range_of_maximum_number_of_weekly_lessons": cls[
                                    "range_of_maximum_number_of_weekly_lessons"]
                            }
                            schedule[teacher["name"] + " " + teacher["surname"]]["free_time"] += cls[
                                "range_of_maximum_number_of_weekly_lessons"]
    for teacher, value in schedule.items():
        for cls, cls_value in value["weekday"].items():
            if cls_value["start_time"] is None:
                cls_value["start_time"] = find_free_time(teacher, cls, schedule)
                if cls_value["start_time"] is None:
                    print(f"Hours needed for {cls} with {teacher}")
                    print("Do you want to change settings? y/n")
                    response = input("")
                    if response.lower() == 'y':
                        change_settings(cls, schedule)
                        cls_value["start_time"] = find_free_time(teacher, cls, schedule)
                    else:
                        print("class is not scheduled! ")
                        return
                cls_value["end_time"] = cls_value["start_time"] + cls_value["range_of_maximum_number_of_weekly_lessons"]
    return schedule


def find_free_time(teacher, cls, schedule):
    """

    :param teacher: teacher for who we have to find free time
    :param cls: class where we need to add lesson
    :param schedule: schedule data to deal with
    :return: hour for scheduling or None if not hour available
    """
    for hour in range(8, 22):
        for weekday in range(5):
            if all(schedule[teacher]["weekday"][other_cls]["start_time"] != hour or
                   schedule[teacher]["weekday"][other_cls]["start_time"] + schedule[teacher]["weekday"][other_cls][
                       "range_of_maximum_number_of_weekly_lessons"] <= hour for other_cls in
                   schedule[teacher]["weekday"]):
                return hour
    return None

def change_settings(cls, schedule):
    """

    :param cls: class which needs setting changes
    :param schedule: schedule data
    :return: None
    """
    for teacher, value in schedule.items():
        for cls_name, cls_value in value["weekday"].items():
            if cls_name == cls:
                cls_value["range_of_maximum_number_of_weekly_lessons"] = int(input("Enter new range: "))


def parse_json(filename):
    """

    :param filename: filename to parse
    :return: parsed json data
    """
    pass
    with open(filename) as file:
        data = file.read()
        return json.loads(data)


def write_schedule(data, filename):
    """

    :param filename:  output file
    :param data: data to write
    :return: no return value
    """
    dumped = json.dumps(data, indent=4)
    with open(filename, 'w') as file:
        file.write(dumped)


if __name__ == "__main__":
    data = create_schedule(parse_json("data.json"))
    write_schedule(data, "out.json")