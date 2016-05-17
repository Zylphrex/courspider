# courspider
Web scraper for U of T courses writing in python3, tested on python 3.5.1

* Currently the only supported calendar is from the Faculty of Arts and Science.
* Calendars from 2011-2012 onwards should work just fine, any older calendars may not work.
* Using the Faculty Calendar, this API will crawl to all the Department calendars, and using each Department Calendar, report back the courses

`create_json.py` is the file used the generate the included `json` file, and shows how to use parts of the API

The included `courses.json` file contains all of the courses in `json` format.
It is in the form:

```
{
  "courses":[
    {
      "Course distribution requirement": "...",
      "Course name": "...",
      "Course preparation": "...",
      "Course exclusion": "...",
      "Course corequisite": "...",
      "Course prerequisite": "...",
      "Course code": "...",
      "Course breadth requirement": "...",
      "Course description": "...."
    },
    ...
  ]
}
```
Note that `None` will appear anywhere where the field does not have a value

## Installation:
```
pip3 install courspider
```

## Dependencies:
```
beautifulsoup4
```
