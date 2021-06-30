![OPSWAT](https://id.opswat.com/static/media/logo.8d40c232.svg)

# OPSWAT MetaDefender Scanner

---

This application receives takes a user provided file and checks to see if reports have already been made on OPSWAT MetaDefender. If there are no reports, the file is uploaded and scanned waits for a report to be generated. The report retrieved and output to the console as well as dumped to a reports.txt file.

### Installation

---

Before running the application:

1. Install Python 3.9.6 or above
2. In the project directory run:
   `pip install requirements.txt`
3. Place your apikey in a file apikeys.txt in the apikeys folder

### Usage

---

To scan a file, simply run the python code with the path to your file as an argument, e.g.
`python scan.py c:\Users\*username*\Documents\samplefile.txt`
The application will output the report to the console and print the report to report.txt
