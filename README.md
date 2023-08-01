Calculate how much money is worth in a different country. Uses data from World
Bank.

Note: Works on python3.4 and above.

### Installation Instructions
1. Clone the source code

        git clone https://github.com/nigelbabu/pppconverter.git

2. [Install](https://go.dev/doc/install) Golang for your computer

3. Build the server and the CLI tools

        go mod download
        go build
        go build -o pppcli cli/main.go

3. Create the sqlite database by running ppcli.

        ./ppcli dbInit

4. Import the CSV into the sqlite database.

        ./pppcli import -f data.csv
        ./pppcli importCountries -f countries.csv

5. Run the site.

        ./pppconverter

[wb]: http://data.worldbank.org/indicator/PA.NUS.PPP

PS: Some automation code is yet to be outsourced as I'm still working out some
minor bugs in the code.
