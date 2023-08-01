Calculate how much money is worth in a different country. Uses data from [World
Bank][wb].

Note: Works on python3.4 and above.

### Installation Instructions
1. Clone the source code

        git clone https://github.com/nigelbabu/pppconverter.git

2. [Install](https://go.dev/doc/install) Golang for your computer

3. Build the server and the CLI tools

        go mod download
        go build
        go build -o pppcli cli/main.go

4. Create a config.yaml with the following parameters at minimum

        database: temp.db
        static: ./static
        templates: ./templates/*.html

5. Create the sqlite database by running pppcli.

        ./pppcli dbInit

6. Import the CSV into the sqlite database.

        ./pppcli import -f data.csv
        ./pppcli importCountries -f countries.csv

7. Insert a key into the SQLite DB by hand to indicate USD to GBP rate for 100 USD.

        sqlite3 temp.db "INSERT OR IGNORE INTO configs (key, value) VALUES ('gbp_rate', 77.75); UPDATE configs SET key='gbp_rate', value=77.75 WHERE key='gbp_rate';" 

8. Run the site.

        ./pppconverter

[wb]: http://data.worldbank.org/indicator/PA.NUS.PPP


### Notes
* The data.csv file in the repo will not be frequently updated, however, the
  site itself will fetch new data once a week.
* Some automation code is yet to be open sourced as I'm still working out some
  minor bugs in the code.
