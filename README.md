**Proxy - Face Recognition Attendance System**
---------
**Abstract** :

The Proxy Application presented in this paper is an attendance tracking application intended for use by universities to track attendance of the students. It allows the administrators to input the photographs of the class and record the attendance of the students based on the face recognition algorithm. This eliminates the issue of proxy in the universities, thereby saving time for the professor with no need to manually check for any issues in the attendance .

**Introduction**

The Proxy Application is a software product intended to be used by the universities to record the students’ attendance based on the photographs uploaded of the class. It uses face recognition algorithms to achieve the task. It allows students to input their photographs and the professors to upload the class photographs. The photographs uploaded by the students are used as initial training data for the application. The photographs uploaded by the professor, after resolving any issues that arise, are again used to train the application. This helps in achieving better recognition rate as the time progresses. Any issues that are raised by the students can be resolved by the corresponding course professor via an interface in the application itself.

**Project General Description**

The main purpose of PROXY application is to track attendance from a few photographs of the class. This application has 4 major modules:
> - First module is the **Professor/TA interface**. This interface lets professors upload images of the class, view attendance of any student of that class, answer queries raised by students about their attendance, and manually change the attendance in case the image recognition algorithm makes any error.
> - Second module is the **Student interface**. This interface lets students upload their photos in different angles which will only be used for recognising their face. Students should also enter their details like Name, Roll no, Phone no through this interface. This information will be used for administrative purposes.
> - Third module deals with the **Computer Vision** part. This is a very important module of this application. A good face recognition algorithm will be used here, so that very less number of errors are made.
> - This last module deals with **logging** every activity done by professors or TA’s or students on this application. This log helps in many purposes like recovery from a database crash, improvising this application, to find any malfunctioning part etc.

Check the folder **documentation** for documentation and installation instructions
