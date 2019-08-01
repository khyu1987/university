# University 

To run the application localy you need:

1. Install and activate any of virtual container for python (python=3.7)
2. Run ./run_local.sh from project root directory


To test API use:

1. list courses: 
   - list:   GET http://localhost:8000/courses/

2. RUD course:
   - read:   GET http://localhost:8000/courses/<id>/
   - update: PUT/PATCH http://localhost:8000/courses/<id>/
   - delete: DELETE http://localhost:8000/courses/<id>/

3. assign/unassign students to/from course:
   - assign:   POST http://localhost:8000/courses/<id>/assign/  {"student": <id>}
   - unassign: POST http://localhost:8000/courses/<id>/unassign/  {"student": <id>}

4. report in csv format:
   - report CSV: GET http://localhost:8000/students/