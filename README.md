Calculate how much money is worth in a different country. Uses data from World
Bank.

### Installation Instructions
1. Clone the source code

    https://github.com/nigelbabu/pppconverter.git

2. Create a virtual environments and install the dependencies

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

3. Create the sqlite database by running the website.py file.

    ./website.py

4. Import the CSV into the sqlite database.

    ./importcsv.py -f data.csv

5. Run the site.

    ./webiste.py


### Updating the data
1. Download the CSV data from the [world bank portal][wb] and unzip the file.

3. Run the parsecsv.py script to create a file called parsed\_data.csv.

    ./parsecsv.py -f /path/to/file

4. Replace data.csv file with the newly created parsed\_data.csv file.

5. Import the new CSV into the sqlite database.

    ./importcsv.py -f data.csv

6. PROFITT!!



[wb]: http://data.worldbank.org/indicator/PA.NUS.PPP
